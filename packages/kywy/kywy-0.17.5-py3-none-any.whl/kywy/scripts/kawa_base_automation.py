import pandas as pd

from kywy.scripts.kawa_base_script import BaseKawaScript


class BaseAutomationScript(BaseKawaScript):

    def metadata(self):
        raise Exception('Must implement, to return script metadata (parameters definition).')

    def execute(self, df: pd.DataFrame):
        raise Exception('Must implement, to execute automation.')
