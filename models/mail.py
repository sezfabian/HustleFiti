#!/usr/bin/env python3
# Python SDK: https://github.com/sendinblue/APIv3-python-library
"""
Module to send confirmation email using brevo API
"""
from __future__ import print_function
from os import getenv
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

class Email:
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = getenv("ENV_HUSTLE_API")

    def send(self, params: dict):
        """
        creates an instance of the API class
        Sends a transactional email
        """
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))

        # SendSmtpEmail | Values to send a transactional email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":params["email"],"name":params["name"]}],
                                                       template_id=4, params=params,
                                                       headers={"X-Mailin-custom": "api-key:self.configuration.api_key['api-key']|\
                                                        content_type:application/json|accept:application/json",
                                                       "charset": "iso-8859-1"})

        try:
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    def __init__(self):
        pass