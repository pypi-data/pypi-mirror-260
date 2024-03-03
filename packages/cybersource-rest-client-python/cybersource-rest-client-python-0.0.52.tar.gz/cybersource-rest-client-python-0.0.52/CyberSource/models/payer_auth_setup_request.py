# coding: utf-8

"""
    CyberSource Merged Spec

    All CyberSource API specs merged together. These are available at https://developer.cybersource.com/api/reference/api-reference.html

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class PayerAuthSetupRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'client_reference_information': 'Riskv1decisionsClientReferenceInformation',
        'payment_information': 'Riskv1authenticationsetupsPaymentInformation',
        'processing_information': 'Riskv1authenticationsetupsProcessingInformation',
        'token_information': 'Riskv1authenticationsetupsTokenInformation'
    }

    attribute_map = {
        'client_reference_information': 'clientReferenceInformation',
        'payment_information': 'paymentInformation',
        'processing_information': 'processingInformation',
        'token_information': 'tokenInformation'
    }

    def __init__(self, client_reference_information=None, payment_information=None, processing_information=None, token_information=None):
        """
        PayerAuthSetupRequest - a model defined in Swagger
        """

        self._client_reference_information = None
        self._payment_information = None
        self._processing_information = None
        self._token_information = None

        if client_reference_information is not None:
          self.client_reference_information = client_reference_information
        if payment_information is not None:
          self.payment_information = payment_information
        if processing_information is not None:
          self.processing_information = processing_information
        if token_information is not None:
          self.token_information = token_information

    @property
    def client_reference_information(self):
        """
        Gets the client_reference_information of this PayerAuthSetupRequest.

        :return: The client_reference_information of this PayerAuthSetupRequest.
        :rtype: Riskv1decisionsClientReferenceInformation
        """
        return self._client_reference_information

    @client_reference_information.setter
    def client_reference_information(self, client_reference_information):
        """
        Sets the client_reference_information of this PayerAuthSetupRequest.

        :param client_reference_information: The client_reference_information of this PayerAuthSetupRequest.
        :type: Riskv1decisionsClientReferenceInformation
        """

        self._client_reference_information = client_reference_information

    @property
    def payment_information(self):
        """
        Gets the payment_information of this PayerAuthSetupRequest.

        :return: The payment_information of this PayerAuthSetupRequest.
        :rtype: Riskv1authenticationsetupsPaymentInformation
        """
        return self._payment_information

    @payment_information.setter
    def payment_information(self, payment_information):
        """
        Sets the payment_information of this PayerAuthSetupRequest.

        :param payment_information: The payment_information of this PayerAuthSetupRequest.
        :type: Riskv1authenticationsetupsPaymentInformation
        """

        self._payment_information = payment_information

    @property
    def processing_information(self):
        """
        Gets the processing_information of this PayerAuthSetupRequest.

        :return: The processing_information of this PayerAuthSetupRequest.
        :rtype: Riskv1authenticationsetupsProcessingInformation
        """
        return self._processing_information

    @processing_information.setter
    def processing_information(self, processing_information):
        """
        Sets the processing_information of this PayerAuthSetupRequest.

        :param processing_information: The processing_information of this PayerAuthSetupRequest.
        :type: Riskv1authenticationsetupsProcessingInformation
        """

        self._processing_information = processing_information

    @property
    def token_information(self):
        """
        Gets the token_information of this PayerAuthSetupRequest.

        :return: The token_information of this PayerAuthSetupRequest.
        :rtype: Riskv1authenticationsetupsTokenInformation
        """
        return self._token_information

    @token_information.setter
    def token_information(self, token_information):
        """
        Sets the token_information of this PayerAuthSetupRequest.

        :param token_information: The token_information of this PayerAuthSetupRequest.
        :type: Riskv1authenticationsetupsTokenInformation
        """

        self._token_information = token_information

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, PayerAuthSetupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
