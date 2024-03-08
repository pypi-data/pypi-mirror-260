import json
import logging
from socket import timeout
from urllib.error import URLError
from urllib.request import Request, urlopen

from .alert import Channel


class SlackWebhook(Channel):
    def __init__(self, **kwargs):
        """
        :param slack_config:
        {
            "url": "https://hooks.slack.com/services/T00/B00/XXX",
            "channel": "slack channel name",
            "username": "slack user name",
            "icon_emoji": ":warning:"
            ...
        }
        """
        super().__init__("slack")
        self.slack_config = kwargs.copy()
        self.url = self.slack_config['url']
        del self.slack_config['url']

        self.timeout_error = False

    def post_msg(self, msg, **kwargs):
        """

        :param msg:
        :param kwargs: override any parameters if necessary
        :return:
        """
        if self.timeout_error:
            return
        args = {
            "text": msg,
        }
        args.update(self.slack_config)
        args.update(kwargs)

        try:
            return self.__send(args)
        except URLError as ue:
            if isinstance(ue.reason, timeout):
                logging.warning("Timeout error detected! Disable sending slack messages.")
                self.timeout_error = True
            else:
                raise

    def __send(self, args):
        data = json.dumps(args).encode()
        req = Request(self.url, data=data, headers={"Content-type": "application/json"}, method="POST")
        return urlopen(req, timeout=1).read().decode()


def create_slack_webhook(slack_config, username, channel=None) -> SlackWebhook:
    slack_config['username'] = username
    if channel:
        slack_config['channel'] = channel
    return SlackWebhook(**slack_config)
