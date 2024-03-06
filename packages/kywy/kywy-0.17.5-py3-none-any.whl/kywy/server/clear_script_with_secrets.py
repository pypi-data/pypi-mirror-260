import json

from kywy.scripts.kawa_secrets import KawaSecrets
from kywy.server.aes_cipher import decrypt_script


class ClearScriptWithSecrets:

    def __init__(self, clear_script: str, secrets: dict):
        self.clear_script = clear_script
        self.kawa_secrets = KawaSecrets(secrets)

    @staticmethod
    def decrypt(encrypted: str,
                aes_key: str):
        # Serialized by Java server as a JSON object (with keys 'script' and 'secrets') before encryption
        decrypted = decrypt_script(encrypted, aes_key)
        print('### Decrypted', decrypted)
        deserialized_json = json.loads(decrypted)
        clear_script = deserialized_json["script"]
        secrets = deserialized_json["secrets"]
        return ClearScriptWithSecrets(clear_script, secrets)
