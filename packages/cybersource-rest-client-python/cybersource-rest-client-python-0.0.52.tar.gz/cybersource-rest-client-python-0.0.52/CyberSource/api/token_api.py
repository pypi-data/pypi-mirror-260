# coding: utf-8

"""
    CyberSource Merged Spec

    All CyberSource API specs merged together. These are available at https://developer.cybersource.com/api/reference/api-reference.html

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient
import CyberSource.logging.log_factory as LogFactory

from ..utilities.tracking.sdk_tracker import SdkTracker
class TokenApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """
	
    def __init__(self, merchant_config, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client
        self.api_client.set_configuration(merchant_config)
        self.logger = LogFactory.setup_logger(self.__class__.__name__, self.api_client.mconfig.log_config)



    def post_token_payment_credentials(self, token_id, post_payment_credentials_request, **kwargs):
        """
        Generate Payment Credentials for a TMS Token
        |  |  |  |     | --- | --- | --- |     |**Token**<br>A Token can represent your tokenized Customer, Payment Instrument or Instrument Identifier information.|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|**Payment Credentials**<br>Contains payment information such as the network token, generated cryptogram for Visa & MasterCard or dynamic CVV for Amex in a JSON Web Encryption (JWE) response.<br>Your system can use this API to retrieve the Payment Credentials for an existing Customer, Payment Instrument or Instrument Identifier. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_token_payment_credentials(token_id, post_payment_credentials_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str token_id: The Id of a token representing a Customer, Payment Instrument or Instrument Identifier. (required)
        :param PostPaymentCredentialsRequest post_payment_credentials_request: (required)
        :param str profile_id: The Id of a profile containing user specific TMS configuration.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        if self.api_client.mconfig.log_config.enable_log:
            self.logger.info("CALL TO METHOD `post_token_payment_credentials` STARTED")

        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.post_token_payment_credentials_with_http_info(token_id, post_payment_credentials_request, **kwargs)
        else:
            (data) = self.post_token_payment_credentials_with_http_info(token_id, post_payment_credentials_request, **kwargs)
            return data

    def post_token_payment_credentials_with_http_info(self, token_id, post_payment_credentials_request, **kwargs):
        """
        Generate Payment Credentials for a TMS Token
        |  |  |  |     | --- | --- | --- |     |**Token**<br>A Token can represent your tokenized Customer, Payment Instrument or Instrument Identifier information.|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|**Payment Credentials**<br>Contains payment information such as the network token, generated cryptogram for Visa & MasterCard or dynamic CVV for Amex in a JSON Web Encryption (JWE) response.<br>Your system can use this API to retrieve the Payment Credentials for an existing Customer, Payment Instrument or Instrument Identifier. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_token_payment_credentials_with_http_info(token_id, post_payment_credentials_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str token_id: The Id of a token representing a Customer, Payment Instrument or Instrument Identifier. (required)
        :param PostPaymentCredentialsRequest post_payment_credentials_request: (required)
        :param str profile_id: The Id of a profile containing user specific TMS configuration.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['token_id', 'post_payment_credentials_request', 'profile_id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_token_payment_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'token_id' is set
        if ('token_id' not in params) or (params['token_id'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `token_id` when calling `post_token_payment_credentials`")
            raise ValueError("Missing the required parameter `token_id` when calling `post_token_payment_credentials`")
        # verify the required parameter 'post_payment_credentials_request' is set
        if ('post_payment_credentials_request' not in params) or (params['post_payment_credentials_request'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `post_payment_credentials_request` when calling `post_token_payment_credentials`")
            raise ValueError("Missing the required parameter `post_payment_credentials_request` when calling `post_token_payment_credentials`")


        collection_formats = {}

        path_params = {}
        if 'token_id' in params:
            path_params['tokenId'] = params['token_id']
            tokenId=token_id

        query_params = []

        header_params = {}
        if 'profile_id' in params:
            header_params['profile-id'] = params['profile_id']

        form_params = []
        local_var_files = {}

        body_params = None
        if 'post_payment_credentials_request' in params:
            body_params = params['post_payment_credentials_request']
        
            sdkTracker = SdkTracker()
            body_params = sdkTracker.insert_developer_id_tracker(body_params, 'post_payment_credentials_request', self.api_client.mconfig.run_environment)
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/jose;charset=utf-8'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(f'/tms/v2/tokens/{tokenId}/payment-credentials', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='str',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
