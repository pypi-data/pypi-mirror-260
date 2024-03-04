import os
import logging
import warnings
from io import BytesIO
from typing import Callable
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from ..y4a_credentials import get_credentials

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class GGMailUtils:
    """
    Utils for Google Mail

    :param sender_email: the email of sender
        defaults to None
        if not provide, the email of DA team will be used
    :param sender_password: the password email of sender
        defaults to None
        if not provide, the email of DA team will be used
    """

    def __init__(
        self,
        sender_email: str = None,
        sender_password: str = None,
    ) -> None:
        if not sender_email:
            da_auto_creds = get_credentials(
                'gmail',
                'da',
            )
            self.sender_email = da_auto_creds['email']
            self.sender_password = da_auto_creds['password']
        else:
            self.sender_email = sender_email
            self.sender_password = sender_password

    def _create_smtp_session(self) -> Callable:
        session = smtplib.SMTP(
            'smtp.gmail.com',
            587,
        )
        session.starttls()
        session.login(
            user=self.sender_email,
            password=self.sender_password,
        )

        return session

    def _create_base_message(
        self,
        receiver_email: list,
        content: str,
        cc_email: list = None,
        subject: str = None,
    ) -> Callable:
        message = MIMEMultipart()

        message['From'] = self.sender_email
        message['To'] = ', '.join(receiver_email)
        if cc_email:
            message['Cc'] = ', '.join(cc_email)
        if subject:
            message['Subject'] = subject

        message.attach(
            MIMEText(
                content,
                'html',
            )
        )

        return message

    def send_mail(
        self,
        receiver_email: list,
        content: str,
        cc_email: list = None,
        subject: str = None,
    ) -> None:
        """
        Send plain text email to group of people

        :param receiver_email: list of people to receive email
        :param content: the content of email
        :param cc_email: list of people to receive CC
            defaults to None
        :param subject: the subject of email
            defaults to None
        """

        session = self._create_smtp_session()
        message = self._create_base_message(
            receiver_email=receiver_email,
            cc_email=cc_email,
            content=content,
            subject=subject,
        )

        session.send_message(
            msg=message,
        )

        session.quit()

    def send_mail_w_attachments(
        self,
        receiver_email: list,
        content: str,
        attachment_path: list,
        cc_email: list = None,
        subject: str = None,
    ) -> None:
        """
        Send email with attachments to group of people

        :param receiver_email: list of people to receive email
        :param content: the content of email
        :param attachment_path: list of file path to attach
        :param cc_email: list of people to receive CC
            defaults to None
        :param subject: the subject of email
            defaults to None
        """

        session = self._create_smtp_session()
        message = self._create_base_message(
            receiver_email=receiver_email,
            cc_email=cc_email,
            content=content,
            subject=subject,
        )

        for path in attachment_path:
            attachment_read = open(
                path,
                'rb',
            ).read()

            attachment = MIMEBase(
                'application',
                'octet-stream',
            )
            attachment.set_payload(
                attachment_read
            )
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(path)}"'
            )

            message.attach(attachment)

        session.send_message(
            msg=message,
        )

        session.quit()

    def send_mail_w_pandas_df(
        self,
        receiver_email: list,
        content: str,
        data_list: list,
        file_name: list,
        cc_email: list = None,
        subject: str = None,
    ) -> None:
        """
        Send email with pandas dataframe as
            Excel file to group of people

        :param receiver_email: list of people to receive email
        :param content: the content of email
        :param data_list: list of dataframe to attach
        :param file_name: list of file name respectively to
            list of dataframe
        :param cc_email: list of people to receive CC
            defaults to None
        :param subject: the subject of email
            defaults to None
        """

        if len(data_list) != len(file_name):
            raise Exception(
                'Length of data_list must match length of file_name'
            )

        session = self._create_smtp_session()
        message = self._create_base_message(
            receiver_email=receiver_email,
            cc_email=cc_email,
            content=content,
            subject=subject,
        )

        for i in range(len(data_list)):
            df_output = BytesIO()
            data_list[i].to_excel(
                df_output,
                index=False,
            )
            df_output.seek(0)

            df_file = MIMEApplication(
                df_output.read()
            )
            df_file['Content-Disposition'] = \
                f'attachment; filename="{file_name[i]}"'

            message.attach(df_file)

        session.send_message(
            msg=message,
        )

        session.quit()
