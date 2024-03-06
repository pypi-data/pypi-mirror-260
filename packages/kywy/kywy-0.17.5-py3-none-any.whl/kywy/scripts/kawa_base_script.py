import pandas as pd

from kywy.scripts.kawa_secrets import KawaSecrets


class BaseKawaScript:

    def __init__(self, secrets: KawaSecrets):
        self.__kawa_secrets = secrets

    def secret(self, key: str) -> str:
        return self.__kawa_secrets.get(key)

    def metadata(self):
        pass

    def execute(self, df: pd.DataFrame):
        pass
