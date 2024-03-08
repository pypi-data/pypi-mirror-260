from onepasswordconnectsdk.models import Item

from .secretmanagerbase import SecretManagerBase, SecretItem
from ..encryption import DocEncryption


class DocEncryptionFactory(SecretManagerBase[SecretItem]):
    def __init__(self):
        super().__init__()

    def tag_filter(self):
        return 'aes'

    def process_item(self, item: Item):
        credential_config = {}
        for field in item.fields:
            if field.label == 'aes256ctr':
                credential_config[field.label] = field.value
            if field.label == 'aes256cbc':
                credential_config[field.label] = field.value
        if len(credential_config) > 0:
            return SecretItem(credential_config)

    def create_aes256ctr(self):
        item = self.find_one().metadata()
        return DocEncryption({"aes256ctr": {'password': item['aes256ctr']}, "aes256cbc": {'key': item['aes256cbc']}})
