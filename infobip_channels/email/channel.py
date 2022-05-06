from http import HTTPStatus
from typing import Any, Dict, Type, Union

import requests

from infobip_channels.core.channel import Channel
from infobip_channels.core.models import PostHeaders, ResponseBase
from infobip_channels.email.models.body.send_email import EmailMessageBody
from infobip_channels.email.models.response.core import EmailResponseError
from infobip_channels.email.models.response.send_email import SendEmailResponse


class EmailChannel(Channel):
    """Class used for interaction with the Infobip's Email API."""

    EMAIL_URL_TEMPLATE = "/email/2/"

    def _get_custom_response_class(
        self,
        raw_response: Union[requests.Response, Any],
        response_class: Type[ResponseBase] = SendEmailResponse,
        *args,
        **kwargs
    ) -> Type[ResponseBase]:

        if raw_response.status_code == HTTPStatus.OK:
            return response_class
        elif raw_response.status_code in (
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.NOT_FOUND,
        ):
            return EmailResponseError

        raise ValueError

    def send_email_message(
        self, message: Union[EmailMessageBody, Dict]
    ) -> Union[ResponseBase, requests.Response, Any]:
        """Send an email or multiple emails to a recipient or multiple recipients
        with CC/BCC enabled.

        :param message: Body of the message to send
        :return: Received response
        """
        message = self.validate_message_body(message, EmailMessageBody)
        body, content_type = message.to_multipart()

        response = self._client.post(
            self.EMAIL_URL_TEMPLATE + "send",
            body,
            PostHeaders(
                content_type=content_type, authorization=self._client.auth.api_key
            ),
        )
        return self._construct_response(response, SendEmailResponse)