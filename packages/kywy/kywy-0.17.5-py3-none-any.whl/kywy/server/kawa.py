import pyarrow
import pandas
import polars


class AutomationData:
    def __init__(self, arrow_table: pyarrow.Table):
        self.arrow_table: pyarrow.Table = arrow_table

    def to_pandas(self) -> pandas.DataFrame:
        return self.arrow_table.to_pandas()

    def to_polars(self) -> polars.DataFrame:
        return polars.from_arrow(self.arrow_table)

    def row_count(self) -> int:
        return self.arrow_table.num_rows


class BaseAutomationScript:

    def metadata(self):
        print('Should return script metadata (parameters definition).')

    def execute(self, data: AutomationData):
        print('Should execute automation.')


class Types:
    TEXT = 'text'
    INTEGER = 'integer'
    DECIMAL = 'decimal'


