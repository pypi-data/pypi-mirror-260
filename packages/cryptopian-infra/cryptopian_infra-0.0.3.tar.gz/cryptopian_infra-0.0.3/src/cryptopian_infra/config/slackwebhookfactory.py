from onepasswordconnectsdk.models import Item

from .secretmanagerbase import SecretManagerBase, SecretItem
from ..alert.slackwebhook import SlackWebhook


class SlackWebhookFactory(SecretManagerBase[SecretItem]):
    def __init__(self):
        super().__init__()

    def tag_filter(self):
        return 'Slack/LegacyWebhook'

    def process_item(self, item: Item):
        section_lookup = SecretManagerBase.get_section_lookup(item)

        webhook_config = {}
        for field in item.fields:
            if field.id == 'username':
                webhook_config['username'] = field.value
            elif field.section is not None:
                section_id = field.section.id
                if section_id in section_lookup:
                    section_label = section_lookup[section_id]
                    if section_label == 'WEBHOOK':
                        webhook_config[field.label] = field.value
        return SecretItem(webhook_config)

    def create_webhook(self, **kwargs):
        item = self.find_one(**kwargs)
        return SlackWebhook(**item.metadata())
