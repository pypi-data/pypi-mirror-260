import logging
import warnings
import json
import pandas as pd
import numpy as np
from httplib2 import Http

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def send_message(
    webhook_url: str,
    message: str,
):
    """
    Send message to a chat space of Google

    :param webhook_url: url of the webhook that is registered in the chat space
    :param message: the content to send to the chat space
    """

    message_body = {
        'text': message,
    }
    message_headers = {
        'Content-Type': 'application/json; charset=UTF-8',
    }

    http = Http()
    response = http.request(
        uri=webhook_url,
        method='POST',
        headers=message_headers,
        body=json.dumps(message_body),
    )
    status_code = response[0]['status']

    if status_code == '200':
        logging.info('Message sent successfully!')
    else:
        logging.info('Failed to send message!')
        logging.error(
            json.loads(
                response[1].decode('utf-8')
            )['error']
        )


def send_data(
    webhook_url: str,
    data: pd.DataFrame,
    title: str = None,
):
    """
    Send data to a chat space of Google

    :param webhook_url: url of the webhook that is registered in the chat space
    :param data: the data to send
    :param title: the title of the message
    """

    df = data.copy()

    df = df.rename(
        columns=lambda x: x.replace(':', ' ')
        .replace('_', ' ')
        .replace('/', ' ')
        .replace('-', ' ')
        .strip().lower()
    )
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.replace('_', ' ')
            if isinstance(x, str)
            else x
        )
    df = df.replace(np.nan, 'None')
    df_txt = df.to_markdown(
        headers='keys',
        tablefmt='psql',
        index=False,
    )
    if title:
        df_txt = f'*{title}*\n\n' + df_txt

    send_message(
        webhook_url=webhook_url,
        message=df_txt,
    )
