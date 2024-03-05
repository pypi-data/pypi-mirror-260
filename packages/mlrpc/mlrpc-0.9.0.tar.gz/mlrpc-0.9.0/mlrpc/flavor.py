import functools
import hashlib
import io
import json
import os
import random
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Optional, Dict, List

import mlflow
import pandas as pd
from dotenv import dotenv_values
from mlflow.models import infer_signature
from starlette.testclient import TestClient

from mlrpc.proto import base64_to_dir, ResponseObject, RequestObject, RequestObjectEncoded, KeyGenerator, \
    EncryptDecrypt, DataFileChunkWriter, Chunk

MLRPC_ENV_VARS_PRELOAD_KEY = "MLRPC_ENV_VARS_PRELOAD"


def request_to_df(request: RequestObject):
    return pd.DataFrame([request.encode().dict()])


def response_to_df(response: ResponseObject):
    return pd.DataFrame([response.encode().dict()])


def make_request_from_input_df(input_df: pd.DataFrame) -> List['RequestObject']:
    request_objs_enc = [RequestObjectEncoded(**row) for row in input_df.to_dict(orient='records')]
    return [RequestObject.from_request_enc(enc) for enc in request_objs_enc]


def load_mlrpc_env_vars() -> None:
    env_vars = os.getenv(MLRPC_ENV_VARS_PRELOAD_KEY, "")
    buff = io.StringIO(env_vars)
    loaded_env_vars = dotenv_values(stream=buff)
    for k, v in loaded_env_vars.items():
        os.environ[k] = v


def pack_env_file_into_preload(envfile: Path, env_dict: Dict[str, str] = None):
    env_dict = env_dict or os.environ
    if envfile.exists() is True:
        with envfile.open("r") as f:
            env_vars = f.read()
        env_dict[MLRPC_ENV_VARS_PRELOAD_KEY] = env_vars


def get_iso_datetime_timezone() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def debug_msg(msg: str, msg_type: str = "DEFAULT", level: str = "INFO"):
    ts = get_iso_datetime_timezone()
    level = f'[{level}]'
    msg_type = f'[{msg_type}]'.ljust(18)
    worker = f"[WID:{os.getpid()}]"
    print(f"[{ts}] {level} {msg_type} - {worker} {msg}", flush=True)


def copy_files(src: Path, dest: Path, check_dest_empty: bool = True):
    # copying due to not wanting requirements for pathspec
    src_dir = str(src)
    dest_dir = str(dest)

    if dest.exists() and any(dest.iterdir()) and check_dest_empty is True:
        debug_msg("Destination directory is not empty. Skipping file copy.", msg_type="COPY_FILES", level="INFO")
        return

    # clean the destination directory
    if dest.exists():
        shutil.rmtree(dest)

    for root, dirs, files in os.walk(src_dir):
        for directory in dirs:
            dest_subdir = dest_dir / Path(root).relative_to(src_dir) / directory
            dest_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_path = str(os.path.join(root, file))
            dest_file_path = str(dest_dir / Path(root).relative_to(src_dir) / file)
            debug_msg(f"Copying {file_path} to {dest_file_path}", msg_type="COPY_FILES", level="INFO")
            shutil.copy(file_path, dest_file_path)


class AppClientProxy:

    def __init__(self, app):
        self._app = app
        self._client = TestClient(app)

    @property
    def app(self):
        return self._app

    @property
    def client(self):
        return self._client

    def update_app(self, app):
        self._app = app
        self._client = TestClient(app)


class ReloadIndicator:

    def __init__(self, reload_indicator_location: str = None, reload_indicator_file: str = None):
        self._reload_indicator_file = Path(reload_indicator_file or "reload-indicator.txt")
        self._reload_indicator_dir = Path(reload_indicator_location or "/tmp/mlrpc-reload-indicator")
        self._reload_indicator = Path(self._reload_indicator_dir) / self._reload_indicator_file
        self._last_reload_info = None
        # make sure to boot up if the reload indicator exists
        if self.does_reload_indicator_exist() is True:
            self._last_reload_info = self.read_reload_indicator()

    def does_reload_indicator_exist(self) -> bool:
        return self._reload_indicator.exists()

    def _attempt_write(self, content: Optional[str] = None, attempts: int = 3) -> None:
        while attempts > 0:
            try:
                with self._reload_indicator.open("w") as f:
                    current_timestamp = get_iso_datetime_timezone()
                    f.write(content or current_timestamp)
                break
            except Exception as e:
                debug_msg(f"Failed to write to reload indicator: {e}", msg_type="RELOAD_INDICATOR", level="ERROR")
                attempts -= 1
                # random wait time to avoid multiple threads writing at the same time
                time.sleep(random.uniform(1, 3))

    def signal_reload(self, content: Optional[str] = None) -> None:
        debug_msg("Signaling reload", msg_type="RELOAD_INDICATOR", level="INFO")
        if self._reload_indicator_dir.exists() is False:
            self._reload_indicator_dir.mkdir(parents=True, exist_ok=True)

        self._attempt_write(content)

    def read_reload_indicator(self) -> Optional[str]:
        if self.does_reload_indicator_exist() is False:
            return None
        with self._reload_indicator.open("r") as f:
            return f.read()

    def should_i_reload(self) -> bool:
        if self._last_reload_info is None and self.does_reload_indicator_exist() is False:
            return False
        if self.does_reload_indicator_exist() is True and self._last_reload_info != self.read_reload_indicator():
            return True

        return False

    def update_last_reload_info(self):
        self._last_reload_info = self.read_reload_indicator()
        return self._last_reload_info


def make_reload_thread(reload_indicator: ReloadIndicator,
                       hot_reload_dispatcher: 'HotReloadEventHandler') -> threading.Thread:
    def reload_checker():
        debug_msg("Starting reload checker", msg_type="RELOAD_CHECKER", level="INFO")
        while True:
            if reload_indicator.should_i_reload() is True:
                debug_msg(f"Found reload indicator. Reloading app", msg_type="RELOAD_CHECKER",
                          level="INFO")
                try:
                    hot_reload_dispatcher.reload_app()
                except Exception as e:
                    debug_msg(f"Failed to reload app: {e}", msg_type="RELOAD_CHECKER", level="ERROR")
                finally:
                    reload_indicator.update_last_reload_info()
            time.sleep(5)

    return threading.Thread(target=reload_checker, daemon=True)


class HotReloadEventHandler:
    PATH_PREFIX = "__INTERNAL__"
    VALID_EVENTS = ["FULL_SYNC", "RELOAD", "REINSTALL", "RESET", "GET_PUBLIC_KEY", "UPLOAD_LARGE_FILE"]

    def __init__(self,
                 *,
                 app_client_proxy: AppClientProxy,
                 reload_code_path: str,
                 file_in_code_path: str,
                 obj_name: str,
                 reset_code_path: Optional[str] = None,
                 temp_key_dir: Optional[str] = "/tmp/mlrpc-hot-reload",
                 ):
        self._reset_code_path = reset_code_path
        self._obj_name = obj_name
        self._file_in_code_path = file_in_code_path
        self._app_client_proxy = app_client_proxy
        self._reload_code_path = reload_code_path
        self._key_generator = KeyGenerator(temp_key_dir,
                                           debug_msg=functools.partial(debug_msg, msg_type="RSA_KEYGEN"))
        self._encrypt_decrypt = EncryptDecrypt(key_generator=self._key_generator)
        self._reload_indicator = ReloadIndicator()
        self._reload_thread = make_reload_thread(self._reload_indicator, self)
        self._reload_thread.start()
        self._data_chunk_writer = DataFileChunkWriter(
            root_dir=self._reload_code_path,
        )

    def validate(self):
        debug_msg(
            f"Validating hot reload dispatcher with {self._app_client_proxy.app} {self._reload_code_path} "
            f"{self._file_in_code_path} {self._obj_name}",
            msg_type="HOT_RELOAD_VALIDATION",
            level="INFO")
        if not self._app_client_proxy.app:
            raise ValueError("app_proxy must be set")
        if not self._reload_code_path:
            raise ValueError("code_path must be set")
        if not self._file_in_code_path:
            raise ValueError("file_in_code_path must be set")
        if not self._obj_name:
            raise ValueError("obj_name must be set")

    def _is_valid_event(self, path: str) -> bool:
        normalized_req_path = path.lstrip("/").rstrip("/")
        valid_events = [f"{self.PATH_PREFIX}/{event}" for event in self.VALID_EVENTS]
        return normalized_req_path in valid_events

    def reload_app(self):
        import site
        import importlib
        site.addsitedir(self._reload_code_path)
        app_module = __import__(self._file_in_code_path.replace('.py', '').replace('/', '.'),
                                fromlist=[self._obj_name])
        importlib.reload(app_module)
        app_obj = getattr(app_module, self._obj_name)
        self._app_client_proxy.update_app(app_obj)
        debug_msg("Reloaded App!", msg_type="HOT_RELOAD", level="INFO")

    @staticmethod
    def _validate_checksum(content: str, checksum: str) -> bool:
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        debug_msg("Valid checksum", msg_type="HOT_RELOAD", level="INFO")
        return content_hash == checksum

    def _do_full_sync(self, request: RequestObject):
        payload = json.loads(request.content)
        content = self._try_decrypt(payload['content'])
        checksum = payload['checksum']
        if self._validate_checksum(content, checksum) is False:
            return ResponseObject(
                status_code=400,
                content="Checksum validation failed"
            )
        base64_to_dir(content, self._reload_code_path)
        # send reload signal after files get moved
        self._reload_indicator.signal_reload()
        return ResponseObject(
            status_code=200,
            content="SUCCESS"
        )

    def _large_file_save(self, request: RequestObject):
        payload = json.loads(request.content)
        chunk = Chunk(**payload['chunk'])
        # TODO: get checksum from payload in future
        if chunk.start_of_file:
            debug_msg(f"Starting new file: {chunk.relative_file_path}", msg_type="UPLOAD_LARGE_FILE", level="INFO")
        if chunk.eof:
            debug_msg(f"Ending file: {chunk.relative_file_path}", msg_type="UPLOAD_LARGE_FILE", level="INFO")
        self._data_chunk_writer.write_chunk(chunk)
        return ResponseObject(
            status_code=200,
            content="SUCCESS"
        )

    @staticmethod
    def _install_packages(package_names: List[str]):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *package_names])
            return f"Packages {','.join(package_names)} installed successfully"
        except subprocess.CalledProcessError:
            raise ValueError(f"Failed to install packages {','.join(package_names)}")

    @staticmethod
    def _uninstall_package(package_name: str):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name])
            return f"Package {package_name} uninstalled successfully"
        except subprocess.CalledProcessError:
            f"Failed to uninstall package {package_name}"

    def _do_install(self, request: RequestObject):
        payload = json.loads(request.content)
        requirements = payload['requirements']
        install_message = self._install_packages(requirements)
        # send reload signal after python libs are installed
        self._reload_indicator.signal_reload()
        return ResponseObject(
            status_code=200,
            content=json.dumps(install_message)
        )

    def _try_decrypt(self, something: Optional[str]) -> Optional[str]:
        if something is None:
            return None
        if isinstance(something, str) is True:
            try:
                return self._encrypt_decrypt.decrypt(something)
            except Exception as e:
                debug_msg(f"Failed to decrypt: {str(e)}", msg_type="CONTENT_DECRYPTION", level="ERROR")
                return something
        return something

    def dispatch(self, request: RequestObject) -> Optional[ResponseObject]:
        if request.method != "POST":
            return None

        if self._is_valid_event(request.path) is False:
            return None

        if request.path == f"/{self.PATH_PREFIX}/FULL_SYNC":
            debug_msg("Dispatching full sync event", msg_type="FULL_SYNC", level="INFO")
            self._do_full_sync(request)
            return ResponseObject(
                status_code=200,
                content="SUCCESS"
            )

        if request.path == f"/{self.PATH_PREFIX}/REINSTALL":
            debug_msg("Dispatching reinstall event", msg_type="REINSTALL_REQS", level="INFO")
            return self._do_install(request)

        if request.path == f"/{self.PATH_PREFIX}/GET_PUBLIC_KEY":
            debug_msg("Dispatching get public key event", msg_type="GET_PUBLIC_KEY", level="INFO")
            return ResponseObject(
                status_code=200,
                content=json.dumps({
                    "public_key": self._key_generator.get_public_key()
                })
            )

        if request.path == f"/{self.PATH_PREFIX}/UPLOAD_LARGE_FILE":
            debug_msg("Dispatching large file upload event", msg_type="UPLOAD_LARGE_FILE", level="INFO")
            return self._large_file_save(request)


class FastAPIFlavor(mlflow.pyfunc.PythonModel):

    def __init__(self,
                 *,
                 local_app_dir_abs: Optional[str],
                 local_app_path_in_dir: Optional[str] = "app.py",
                 app_obj: Optional[str] = "app",
                 artifact_code_key="code",
                 reloadable: Optional[bool] = False):
        self._reloadable = reloadable
        self.local_app_dir = local_app_dir_abs
        self.code_key = artifact_code_key
        self.local_app_dir = self.local_app_dir.rstrip("/")
        self.app_path_in_dir = local_app_path_in_dir
        self.app_obj = app_obj
        self._app_proxy = None
        self._hot_reload_dispatcher: Optional[HotReloadEventHandler] = None

    def load_module(self, app_dir_mlflow_artifacts: Optional[str] = None):
        import site
        app_dir = app_dir_mlflow_artifacts or self.local_app_dir
        # only add if it's not already there
        site.addsitedir(app_dir)
        debug_msg(f"Loading code from path {app_dir}", msg_type="LOAD_MODULE", level="INFO")
        app_module = __import__(self.app_path_in_dir.replace('.py', '').replace('/', '.'), fromlist=[self.app_obj])
        debug_msg(f"Loaded module successfully for {self.app_path_in_dir} from {app_dir}",
                  msg_type="LOAD_MODULE", level="INFO")
        app_obj = getattr(app_module, self.app_obj)
        debug_msg(f"Loaded app object successfully for {self.app_obj}",
                  msg_type="LOAD_MODULE", level="INFO")
        return app_obj

    def validate(self):
        if not self.local_app_dir:
            raise ValueError("local_app_dir_abs must be set")
        if not self.app_path_in_dir:
            raise ValueError("app_path_in_dir must be set")
        if not self.app_obj:
            raise ValueError("app_obj must be set")
        try:
            self.load_module()
        except Exception as e:
            raise ValueError(f"Failed to load app module: {e} in {self.local_app_dir}/{self.app_path_in_dir}")

    def load_context(self, context):
        debug_msg("Loading preloaded env vars",
                  msg_type="LOAD_CONTEXT", level="INFO")
        load_mlrpc_env_vars()
        code_path = self.local_app_dir
        if context is not None:
            code_path = context.artifacts[self.code_key]

        self._app_proxy = AppClientProxy(None)

        # add the app_path to the pythonpath to load modules
        # only if it's not already there
        # update site packages to include this app dir

        def boot_app(_temp_code_dir, _temp_key_dir):
            Path(_temp_code_dir).mkdir(parents=True, exist_ok=True)
            Path(_temp_key_dir).mkdir(parents=True, exist_ok=True)
            debug_msg("Hot reload dir being created at /tmp/mlrpc-hot-reload",
                      msg_type="HOT_RELOAD_SETUP", level="INFO")

            copy_files(Path(code_path), Path(_temp_code_dir), check_dest_empty=True)
            debug_msg(f"Copying files from {code_path} to {_temp_code_dir}",
                      msg_type="HOT_RELOAD_SETUP", level="INFO")
            self._hot_reload_dispatcher = HotReloadEventHandler(
                app_client_proxy=self._app_proxy,
                reload_code_path=_temp_code_dir,
                file_in_code_path=self.app_path_in_dir,
                obj_name=self.app_obj,
                reset_code_path=code_path,
                temp_key_dir=_temp_key_dir
            )
            debug_msg(f"Hot reload dispatcher created for {self.app_obj} in {self.app_path_in_dir}",
                      msg_type="HOT_RELOAD_SETUP", level="INFO")
            self._app_proxy.update_app(self.load_module(app_dir_mlflow_artifacts=_temp_code_dir))

        if os.getenv("MLRPC_HOT_RELOAD", str(self._reloadable)).lower() == "true":
            temp_code_dir = "/tmp/mlrpc-hot-reload"
            temp_key_dir = "/tmp/mlrpc-hot-reload-keys"
            attempts = 5
            while True:
                try:
                    boot_app(temp_code_dir, temp_key_dir)
                    break
                except Exception as e:
                    debug_msg(f"Error occurred while booting app: {e}",
                              msg_type="LOAD_CONTEXT", level="ERROR")
                    attempts -= 1
                    wait_time = random.uniform(1, 5)
                    time.sleep(wait_time)
                    if attempts == 0:
                        raise
                    debug_msg(f"Retrying in 5 seconds",
                              msg_type="LOAD_CONTEXT", level="INFO")
        else:
            self._app_proxy.update_app(self.load_module(app_dir_mlflow_artifacts=code_path))

    def predict(self, context, model_input: pd.DataFrame, params=None):
        if self._app_proxy is None:
            self._app_proxy = AppClientProxy(None)

        if self._app_proxy.app is None or self._app_proxy.client is None:
            self.load_context(context)

        requests = make_request_from_input_df(model_input)
        responses = []

        try:
            # happy path things can go wrong :-)
            if self._hot_reload_dispatcher is not None and len(requests) == 1:
                event_resp = self._hot_reload_dispatcher.dispatch(requests[0])
                if event_resp is not None:
                    return response_to_df(event_resp)

            for req in requests:
                resp = self._app_proxy.client.request(
                    method=req.method,
                    url=req.path,
                    headers=req.headers,
                    params=req.query_params,
                    data=req.content,
                    timeout=req.timeout
                )
                responses.append(ResponseObject.from_httpx_resp(resp).encode())
            return pd.DataFrame([resp.dict() for resp in responses])
        except Exception as e:
            return response_to_df(ResponseObject(
                status_code=500,
                content=f"Error occurred: {str(e)}"
            ))

    @staticmethod
    def signature():
        full_request = request_to_df(RequestObject(
            method='GET',
            headers=[('Host', 'example.org')],
            path='/',
            query_params="",
            content="",
            timeout=10
        ))
        optional_request = request_to_df(RequestObject(
            method='GET',
            path='/'
        ))
        full_response = response_to_df(ResponseObject(
            status_code=200,
            headers=[('Content-Type', 'application/json')],
            content=""
        ))
        optional_response = response_to_df(ResponseObject(
            status_code=200,
        ))
        return infer_signature(
            model_input=pd.concat([full_request, optional_request]),
            model_output=pd.concat([full_response, optional_response])
        )
