import logging
import json
import requests
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)

HEADERS = {
    "Content-type": "application/json"
}


def send_message_to_slack_channel(web_hook_url, payload):
    """
    Send a chat message using an incoming WebHook on
    Slack to the Slack channel specified.
    :param web_hook_url: The destination URL
    :param payload: JSON payload
    """
    try:
        slack_message_body = {"text": json.dumps(payload)}
        response = requests.post(web_hook_url, json=slack_message_body, headers=HEADERS)
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        logger.error(f'Other error occurred: {err}')  # Python 3.6
    else:
        logger.info(response.status_code)
