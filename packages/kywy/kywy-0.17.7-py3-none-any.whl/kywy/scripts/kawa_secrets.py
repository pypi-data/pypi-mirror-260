class KawaSecrets:

    def __init__(self, secrets: dict):
        self.__secrets = secrets

    def get(self, key: str) -> str:
        return self.__secrets.get(key)
