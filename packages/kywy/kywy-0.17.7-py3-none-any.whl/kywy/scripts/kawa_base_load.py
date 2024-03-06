import pandas as pd

from kywy.scripts.kawa_base_script import BaseKawaScript


class BaseLoadScript(BaseKawaScript):

    def metadata(self):
        raise Exception('Must implement, to return script metadata (parameters and outputs definition).')

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        raise Exception('Must implement, to return a pandas.DataFrame with new columns.')
