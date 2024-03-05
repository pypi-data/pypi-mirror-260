from airflow.models import Connection, Variable
from airflow.hooks.base import BaseHook

from cuscom.utils import flatten_dict, mask
from cuscom.exceptions import CuscomException

from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults

import logging
import json
from typing import Any, Dict, Optional


class MSTeamsWebhookHook(HttpHook):
    """
    This hook allows you to post messages to MS Teams using the Incoming Webhook connector.

    Takes both MS Teams webhook token directly and connection that has MS Teams webhook token.
    If both supplied, the webhook token will be appended to the host in the connection.

    :param http_conn_id: connection that has MS Teams webhook URL
    :type http_conn_id: str
    :param webhook_token: MS Teams webhook token
    :type webhook_token: str
    :param message: The message you want to send on MS Teams
    :type message: str
    :param subtitle: The subtitle of the message to send
    :type subtitle: str
    :param button_text: The text of the action button
    :type button_text: str
    :param button_url: The URL for the action button click
    :type button_url : str
    :param theme_color: Hex code of the card theme, without the #
    :type message: str
    :param proxy: Proxy to use when making the webhook request
    :type proxy: str

    """
    def __init__(self,
                 http_conn_id=None,
                 webhook_token=None,
                 message="",
                 subtitle="",
                 button_text="",
                 button_url="",
                 theme_color="00FF00",
                 proxy=None,
                 *args,
                 **kwargs
                 ):
        super(MSTeamsWebhookHook, self).__init__(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_token = self.get_token(webhook_token, http_conn_id)
        self.message = message
        self.subtitle = subtitle
        self.button_text = button_text
        self.button_url = button_url
        self.theme_color = theme_color
        self.proxy = proxy

    def get_proxy(self, http_conn_id):
        conn = self.get_connection(http_conn_id)
        extra = conn.extra_dejson
        return extra.get("proxy", '')

    def get_token(self, token, http_conn_id):
        """
        Given either a manually set token or a conn_id, return the webhook_token to use
        :param token: The manually provided token
        :param conn_id: The conn_id provided
        :return: webhook_token (str) to use
        """
        if token:
            return token
        elif http_conn_id:
            conn = self.get_connection(http_conn_id)
            extra = conn.extra_dejson
            return extra.get('webhook_token', '')
        else:
            raise AirflowException('Cannot get URL: No valid MS Teams '
                                   'webhook URL nor conn_id supplied')

    def build_message(self):
        cardjson = {
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'themeColor': self.theme_color,
            'summary': self.message,
            'sections': [
                {
                    'activityTitle': self.message,
                    'activitySubtitle': self.subtitle,
                    'markdown': 'true',
                    'potentialAction': [
                        {
                            '@type': 'OpenUri',
                            'name': self.button_text,
                            'targets': [{'os': 'default', 'uri': self.button_url}],
                        }
                    ],
                }
            ],
        }
        return json.dumps(cardjson)

    def execute(self):
        """
        Remote Popen (actually execute the webhook call)

        :param cmd: command to remotely execute
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        """
        proxies = {}
        proxy_url = self.get_proxy(self.http_conn_id)
        print("Proxy is : " + proxy_url)
        if len(proxy_url) > 5:
            proxies = {'https': proxy_url}

        self.run(endpoint=self.webhook_token,
                 data=self.build_message(),
                 headers={'Content-type': 'application/json'},
                 extra_options={'proxies': proxies})



class MSTeamsWebhookOperator(SimpleHttpOperator):
    """
    This operator allows you to post messages to MS Teams using the Incoming Webhooks connector.
    Takes both MS Teams webhook token directly and connection that has MS Teams webhook token.
    If both supplied, the webhook token will be appended to the host in the connection.

    :param http_conn_id: connection that has MS Teams webhook URL
    :type http_conn_id: str
    :param webhook_token: MS Teams webhook token
    :type webhook_token: str
    :param message: The message you want to send on MS Teams
    :type message: str
    :param subtitle: The subtitle of the message to send
    :type subtitle: str
    :param button_text: The text of the action button
    :type button_text: str
    :param button_url: The URL for the action button click
    :type button_url : str
    :param theme_color: Hex code of the card theme, without the #
    :type message: str
    :param proxy: Proxy to use when making the webhook request
    :type proxy: str
    """

    template_fields = ('message', 'subtitle',)

    @apply_defaults
    def __init__(self,
                 http_conn_id=None,
                 webhook_token=None,
                 message="",
                 subtitle="",
                 button_text="",
                 button_url="",
                 theme_color="00FF00",
                 proxy=None,
                 *args,
                 **kwargs):

        super(MSTeamsWebhookOperator, self).__init__(endpoint=webhook_token, *args, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_token = webhook_token
        self.message = message
        self.subtitle = subtitle
        self.button_text = button_text
        self.button_url = button_url
        self.theme_color = theme_color
        self.proxy = proxy

    @property
    def hook(self) -> MSTeamsWebhookHook:
        return MSTeamsWebhookHook(
            self.http_conn_id,
            self.webhook_token,
            self.message,
            self.subtitle,
            self.button_text,
            self.button_url,
            self.theme_color,
            self.proxy
        )

    def execute(self, context):
        """
        Call the webhook with the required parameters
        """
        self.hook.execute()
        logging.info("Webhook request sent to MS Teams")


def on_failure(connection: Optional[Connection] = None, msg_template: Optional[str] = None):
    connection = connection or BaseHook.get_connection("teams")
    msg_template = msg_template or Variable.get("TEAMS_MESSAGE_TEMPLATE", "")
    if connection is None:
        raise CuscomException("No teams connection configured")

    if msg_template is None:
        raise CuscomException("No teams message template available")

    def fn(context: Dict[str, Any]):
        arguments = {
            "task_id": "teams_alert",
            "webhook_token": connection.password,  # type: ignore
            "message": msg_template.format_map(flatten_dict(context)),
            "button_text": "Logs",
            "button_link": context.get('task_instance').log_url
        }
               
        failed_alert = MSTeamsWebhookOperator(**arguments)
        return failed_alert.execute(context=context)

    return fn
