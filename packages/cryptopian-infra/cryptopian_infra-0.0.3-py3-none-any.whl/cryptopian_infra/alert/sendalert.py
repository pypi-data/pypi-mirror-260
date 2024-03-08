import json
import logging
from typing import Optional

from .slackwebhook import SlackWebhook
from ..config.slackwebhookfactory import SlackWebhookFactory
from ..threading import MessagePump


class AlertWrapper(MessagePump):
    def __init__(self, alias, slack_bot: SlackWebhook, thread_name=None):
        super().__init__('AlertWrapper' if thread_name is None else thread_name)
        self.alias = alias
        self.slack_bot = slack_bot
        self.last_error = ''

    @staticmethod
    def log_msg_error(alias, message, error, type_):
        if alias is not None:
            print_msg = f"[{alias}]: {message}"
        else:
            print_msg = f"{message}"

        # handle common error formatting
        if error:
            try:
                print_msg += '\n' + json.dumps(error)
            except:
                print_msg += '\n' + repr(error)

        if type_.upper() == 'ERROR':
            logging.error(print_msg)
        else:
            logging.info(type_ + ': ' + print_msg)
        return print_msg

    def handle_message(self, message):
        try:
            self.slack_bot.post_msg(message)
        except:
            logging.exception('Error sending alert')

            try:
                self.slack_bot.post_msg(message)
            except:
                logging.exception('Give up sending slack messages...')

    def send_alert(self, message, error=None, type_='ERROR', alias=None):
        should_send_alert = True
        if alias is None:
            alias = self.alias
        print_msg = self.log_msg_error(alias, message, error, type_)

        if self.last_error == print_msg:
            should_send_alert = False
        else:
            self.last_error = print_msg

        if should_send_alert:
            self.post_message(print_msg)


alert_wrapper: Optional[AlertWrapper] = None


def setup_alert(alias, channel):
    global alert_wrapper
    slack_factory = SlackWebhookFactory()
    slack_bot = slack_factory.create_webhook(channel=channel)

    if not slack_bot:
        raise Exception('Could not create slack webhook')
    alert_wrapper = AlertWrapper(alias, slack_bot)
    alert_wrapper.send_alert(f'{alias} {channel} started.', type_='INFO')


def send_alert(message, error=None, type_='ERROR', alias=None):
    global alert_wrapper
    if alert_wrapper:
        alert_wrapper.send_alert(message, error, type_, alias)
    else:
        AlertWrapper.log_msg_error(alias, message, error, type_)
