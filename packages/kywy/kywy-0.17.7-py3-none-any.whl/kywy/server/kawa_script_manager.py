import concurrent.futures
import inspect

import pandas as pd
import pyarrow as pa
import json

from kywy.client.kawa_client import KawaClient
from kywy.scripts.kawa_base_script import BaseKawaScript
from kywy.scripts.kawa_loader_callback import LoaderCallback
from kywy.server.clear_script_with_secrets import ClearScriptWithSecrets
from kywy.server.interpreter_error import InterpreterError
from kywy.server.kawa_error_manager import KawaErrorManager


def _create_script_instance(clear_script_with_secrets: ClearScriptWithSecrets):
    scope = {}
    exec(clear_script_with_secrets.clear_script, scope, scope)
    cls = scope.get('KawaScript')
    if inspect.isclass(cls) and issubclass(cls, BaseKawaScript):
        print(cls)
        # TODO set secrets
        return cls(clear_script_with_secrets.kawa_secrets)
    else:
        raise InterpreterError('The script must define a class named KawaScript which inherits the right base class')


def _execute_script(clear_script_with_secrets: ClearScriptWithSecrets,
                    arrow_table: pa.Table,
                    callback: LoaderCallback):
    # This function is executed as a separated process.
    # It must be an independent function (not an object method), and its parameters must be serializable.
    # The instantiated script can't be serialized, hence the function is called with the script source code (str).
    print('>>> execute script.', 'callback: ', callback)
    print('>>> script: ', clear_script_with_secrets.clear_script)
    if callback:
        output_df = _create_script_instance(clear_script_with_secrets).execute(arrow_table.to_pandas())
        if isinstance(output_df, pd.DataFrame):
            callback.load(output_df)
        else:
            raise InterpreterError('Script must return a pandas.DataFrame')
    else:
        _create_script_instance(clear_script_with_secrets).execute(arrow_table.to_pandas())
    return True


class KawaScriptManager:

    def __init__(self,
                 kawa_url,
                 kawa_error_manager: KawaErrorManager):
        self.error_manager = kawa_error_manager
        self.kawa_url = kawa_url
        self.executor = concurrent.futures.ProcessPoolExecutor()

    def get_script_metadata(self, clear_script_with_secrets: ClearScriptWithSecrets):
        try:
            script_meta = self.__execute_metadata(clear_script_with_secrets)
            json_meta = json.dumps(script_meta)
            print('json_meta', json_meta)
            return json_meta
        except Exception as err:
            self.error_manager.rethrow(err)

    def submit_script_for_execution(self,
                                    clear_script_with_secrets: ClearScriptWithSecrets,
                                    action_payload,
                                    arrow_table: pa.Table) -> concurrent.futures.Future:
        callback = self.__create_callback(action_payload)
        return self.executor.submit(_execute_script, clear_script_with_secrets, arrow_table, callback)

    def __execute_metadata(self, clear_script_with_secrets: ClearScriptWithSecrets):
        return _create_script_instance(clear_script_with_secrets).metadata()

    def __create_callback(self, action_payload):
        if action_payload.get('pythonPrivateJoinId'):
            python_private_join_id = action_payload.get('pythonPrivateJoinId')
            pk_params = action_payload.get('pkParams')
            pk_mapping_indicator_ids = action_payload.get('pkMappingIndicatorIds')
            workspace_id = action_payload.get('workspaceId')
            api_key = action_payload.get('apiKey')
            print('KAWA url: ', self.kawa_url)
            kawa_client = KawaClient(kawa_api_url=self.kawa_url)
            kawa_client.set_api_key(api_key=api_key)
            kawa_client.set_active_workspace_id(workspace_id=workspace_id)
            return LoaderCallback(python_private_join_id, pk_params,
                                  pk_mapping_indicator_ids,
                                  kawa_client)
        else:
            return None
