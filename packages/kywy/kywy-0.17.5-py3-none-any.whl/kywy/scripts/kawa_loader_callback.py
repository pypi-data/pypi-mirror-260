from kywy.client.data_loader import KawaDataLoader
from kywy.client.kawa_client import KawaClient


class LoaderCallback:
    def __init__(self, python_private_join_id: str, pk_params, pk_mapping_indicator_ids, kawa_client: KawaClient):
        self.kawa_client = kawa_client
        self.python_private_join_id = python_private_join_id
        self.rename_columns = {}
        for i in range(len(pk_params)):
            self.rename_columns[pk_params[i]] = pk_mapping_indicator_ids[i]

    def load(self, df):
        datasource = self.__before_load_python_private_join_data_source(self.python_private_join_id)
        self.__load_python_private_join_data_source(datasource, df)
        self.__after_load_python_private_join_data_source(self.python_private_join_id)

    def __before_load_python_private_join_data_source(self, python_private_join_id: str):
        return self.kawa_client.commands._run_command(command_name='BeforeLoadPythonPrivateJoinDataSource',
                                                      command_parameters={
                                                          "pythonPrivateJoinId": python_private_join_id
                                                      })

    def __load_python_private_join_data_source(self, datasource, df):
        # rename dataframe columns
        print('=== rename: ', self.rename_columns)
        renamed_df = df.copy(deep=True).rename(columns=self.rename_columns)
        print(renamed_df)
        date_source_id = datasource['id']
        data_loader = KawaDataLoader(self.kawa_client, renamed_df, None, datasource_id=date_source_id)
        data_loader.load_data(reset_before_insert=True)

    def __after_load_python_private_join_data_source(self, python_private_join_id):
        self.kawa_client.commands._run_command(command_name='AfterLoadPythonPrivateJoinDataSource',
                                               command_parameters={
                                                   "pythonPrivateJoinId": python_private_join_id
                                               })
