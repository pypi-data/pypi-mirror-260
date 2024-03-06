import pyarrow
import pandas as pd



class AutomationData:
    def __init__(self, arrow_table: pyarrow.Table = None, df=None):
        if arrow_table is not None:
            self.arrow_table: pyarrow.Table = arrow_table
        elif df is not None:
            self.arrow_table = pyarrow.Table.from_pandas(df=df)

    def to_pandas(self) -> pd.DataFrame:
        return self.arrow_table.to_pandas()

    def row_count(self) -> int:
        return self.arrow_table.num_rows


class BaseAutomationScript:

    def metadata(self):
        raise Exception('Must implement, to return script metadata (parameters definition).')

    def execute(self, data: AutomationData):
        raise Exception('Must implement, to execute automation.')


class Types:
    TEXT = 'text'
    INTEGER = 'integer'
    DECIMAL = 'decimal'
