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
class PaymentsApi(object):
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



    def create_payment(self, create_payment_request, **kwargs):
        """
        Process a Payment
        A payment authorizes the amount for the transaction. There are a number of supported payment features, such as E-commerce and Card Present - Credit Card/Debit Card, Echeck, e-Wallets, Level II/III Data, etc..  A payment response includes the status of the request. It also includes processor-specific information when the request is successful and errors if unsuccessful. See the [Payments Developer Guides Page](https://developer.cybersource.com/docs/cybs/en-us/payments/developer/ctv/rest/payments/payments-intro.html).  Authorization can be requested with Capture, Decision Manager, Payer Authentication(3ds), and Token Creation. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_payment(create_payment_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param CreatePaymentRequest create_payment_request: (required)
        :return: PtsV2PaymentsPost201Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        if self.api_client.mconfig.log_config.enable_log:
            self.logger.info("CALL TO METHOD `create_payment` STARTED")

        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_payment_with_http_info(create_payment_request, **kwargs)
        else:
            (data) = self.create_payment_with_http_info(create_payment_request, **kwargs)
            return data

    def create_payment_with_http_info(self, create_payment_request, **kwargs):
        """
        Process a Payment
        A payment authorizes the amount for the transaction. There are a number of supported payment features, such as E-commerce and Card Present - Credit Card/Debit Card, Echeck, e-Wallets, Level II/III Data, etc..  A payment response includes the status of the request. It also includes processor-specific information when the request is successful and errors if unsuccessful. See the [Payments Developer Guides Page](https://developer.cybersource.com/docs/cybs/en-us/payments/developer/ctv/rest/payments/payments-intro.html).  Authorization can be requested with Capture, Decision Manager, Payer Authentication(3ds), and Token Creation. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_payment_with_http_info(create_payment_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param CreatePaymentRequest create_payment_request: (required)
        :return: PtsV2PaymentsPost201Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['create_payment_request']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_payment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'create_payment_request' is set
        if ('create_payment_request' not in params) or (params['create_payment_request'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `create_payment_request` when calling `create_payment`")
            raise ValueError("Missing the required parameter `create_payment_request` when calling `create_payment`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_payment_request' in params:
            body_params = params['create_payment_request']
        
            sdkTracker = SdkTracker()
            body_params = sdkTracker.insert_developer_id_tracker(body_params, 'create_payment_request', self.api_client.mconfig.run_environment)
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/hal+json;charset=utf-8'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(f'/pts/v2/payments', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PtsV2PaymentsPost201Response',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def increment_auth(self, id, increment_auth_request, **kwargs):
        """
        Increment an Authorization
        Use this service to authorize additional charges in a lodging or autorental transaction. Include the ID returned from the original authorization in the PATCH request to add additional charges to that authorization. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.increment_auth(id, increment_auth_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: The ID returned from the original authorization request. (required)
        :param IncrementAuthRequest increment_auth_request: (required)
        :return: PtsV2IncrementalAuthorizationPatch201Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        if self.api_client.mconfig.log_config.enable_log:
            self.logger.info("CALL TO METHOD `increment_auth` STARTED")

        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.increment_auth_with_http_info(id, increment_auth_request, **kwargs)
        else:
            (data) = self.increment_auth_with_http_info(id, increment_auth_request, **kwargs)
            return data

    def increment_auth_with_http_info(self, id, increment_auth_request, **kwargs):
        """
        Increment an Authorization
        Use this service to authorize additional charges in a lodging or autorental transaction. Include the ID returned from the original authorization in the PATCH request to add additional charges to that authorization. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.increment_auth_with_http_info(id, increment_auth_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: The ID returned from the original authorization request. (required)
        :param IncrementAuthRequest increment_auth_request: (required)
        :return: PtsV2IncrementalAuthorizationPatch201Response
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'increment_auth_request']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method increment_auth" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `id` when calling `increment_auth`")
            raise ValueError("Missing the required parameter `id` when calling `increment_auth`")
        # verify the required parameter 'increment_auth_request' is set
        if ('increment_auth_request' not in params) or (params['increment_auth_request'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `increment_auth_request` when calling `increment_auth`")
            raise ValueError("Missing the required parameter `increment_auth_request` when calling `increment_auth`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']
            id=id

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'increment_auth_request' in params:
            body_params = params['increment_auth_request']
        
            sdkTracker = SdkTracker()
            body_params = sdkTracker.insert_developer_id_tracker(body_params, 'increment_auth_request', self.api_client.mconfig.run_environment)
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/hal+json;charset=utf-8'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(f'/pts/v2/payments/{id}', 'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PtsV2IncrementalAuthorizationPatch201Response',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def refresh_payment_status(self, id, refresh_payment_status_request, **kwargs):
        """
        Check a Payment Status
        Checks and updates the payment status 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.refresh_payment_status(id, refresh_payment_status_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: The payment id whose status needs to be checked and updated. (required)
        :param RefreshPaymentStatusRequest refresh_payment_status_request: (required)
        :return: PtsV2PaymentsPost201Response1
                 If the method is called asynchronously,
                 returns the request thread.
        """

        if self.api_client.mconfig.log_config.enable_log:
            self.logger.info("CALL TO METHOD `refresh_payment_status` STARTED")

        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.refresh_payment_status_with_http_info(id, refresh_payment_status_request, **kwargs)
        else:
            (data) = self.refresh_payment_status_with_http_info(id, refresh_payment_status_request, **kwargs)
            return data

    def refresh_payment_status_with_http_info(self, id, refresh_payment_status_request, **kwargs):
        """
        Check a Payment Status
        Checks and updates the payment status 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.refresh_payment_status_with_http_info(id, refresh_payment_status_request, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: The payment id whose status needs to be checked and updated. (required)
        :param RefreshPaymentStatusRequest refresh_payment_status_request: (required)
        :return: PtsV2PaymentsPost201Response1
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'refresh_payment_status_request']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method refresh_payment_status" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `id` when calling `refresh_payment_status`")
            raise ValueError("Missing the required parameter `id` when calling `refresh_payment_status`")
        # verify the required parameter 'refresh_payment_status_request' is set
        if ('refresh_payment_status_request' not in params) or (params['refresh_payment_status_request'] is None):
            if self.api_client.mconfig.log_config.enable_log:
                self.logger.error("InvalidArgumentException : Missing the required parameter `refresh_payment_status_request` when calling `refresh_payment_status`")
            raise ValueError("Missing the required parameter `refresh_payment_status_request` when calling `refresh_payment_status`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']
            id=id

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'refresh_payment_status_request' in params:
            body_params = params['refresh_payment_status_request']
        
            sdkTracker = SdkTracker()
            body_params = sdkTracker.insert_developer_id_tracker(body_params, 'refresh_payment_status_request', self.api_client.mconfig.run_environment)
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/hal+json;charset=utf-8'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/json;charset=utf-8'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(f'/pts/v2/refresh-payment-status/{id}', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='PtsV2PaymentsPost201Response1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
