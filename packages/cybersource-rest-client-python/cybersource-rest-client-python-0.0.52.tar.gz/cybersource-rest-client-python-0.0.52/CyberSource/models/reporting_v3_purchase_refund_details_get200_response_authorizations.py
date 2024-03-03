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


class ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations(object):
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
        'request_id': 'str',
        'transaction_reference_number': 'str',
        'time': 'datetime',
        'authorization_request_id': 'str',
        'amount': 'str',
        'currency_code': 'str',
        'code': 'str',
        'rcode': 'str'
    }

    attribute_map = {
        'request_id': 'requestId',
        'transaction_reference_number': 'transactionReferenceNumber',
        'time': 'time',
        'authorization_request_id': 'authorizationRequestId',
        'amount': 'amount',
        'currency_code': 'currencyCode',
        'code': 'code',
        'rcode': 'rcode'
    }

    def __init__(self, request_id=None, transaction_reference_number=None, time=None, authorization_request_id=None, amount=None, currency_code=None, code=None, rcode=None):
        """
        ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations - a model defined in Swagger
        """

        self._request_id = None
        self._transaction_reference_number = None
        self._time = None
        self._authorization_request_id = None
        self._amount = None
        self._currency_code = None
        self._code = None
        self._rcode = None

        if request_id is not None:
          self.request_id = request_id
        if transaction_reference_number is not None:
          self.transaction_reference_number = transaction_reference_number
        if time is not None:
          self.time = time
        if authorization_request_id is not None:
          self.authorization_request_id = authorization_request_id
        if amount is not None:
          self.amount = amount
        if currency_code is not None:
          self.currency_code = currency_code
        if code is not None:
          self.code = code
        if rcode is not None:
          self.rcode = rcode

    @property
    def request_id(self):
        """
        Gets the request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        An unique identification number assigned by CyberSource to identify the submitted request.

        :return: The request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        An unique identification number assigned by CyberSource to identify the submitted request.

        :param request_id: The request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._request_id = request_id

    @property
    def transaction_reference_number(self):
        """
        Gets the transaction_reference_number of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Transaction Reference Number

        :return: The transaction_reference_number of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._transaction_reference_number

    @transaction_reference_number.setter
    def transaction_reference_number(self, transaction_reference_number):
        """
        Sets the transaction_reference_number of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Transaction Reference Number

        :param transaction_reference_number: The transaction_reference_number of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._transaction_reference_number = transaction_reference_number

    @property
    def time(self):
        """
        Gets the time of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Date

        :return: The time of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Date

        :param time: The time of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: datetime
        """

        self._time = time

    @property
    def authorization_request_id(self):
        """
        Gets the authorization_request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Request Id

        :return: The authorization_request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._authorization_request_id

    @authorization_request_id.setter
    def authorization_request_id(self, authorization_request_id):
        """
        Sets the authorization_request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Request Id

        :param authorization_request_id: The authorization_request_id of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._authorization_request_id = authorization_request_id

    @property
    def amount(self):
        """
        Gets the amount of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Amount

        :return: The amount of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """
        Sets the amount of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Amount

        :param amount: The amount of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._amount = amount

    @property
    def currency_code(self):
        """
        Gets the currency_code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Valid ISO 4217 ALPHA-3 currency code

        :return: The currency_code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """
        Sets the currency_code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Valid ISO 4217 ALPHA-3 currency code

        :param currency_code: The currency_code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._currency_code = currency_code

    @property
    def code(self):
        """
        Gets the code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Code

        :return: The code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization Code

        :param code: The code of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._code = code

    @property
    def rcode(self):
        """
        Gets the rcode of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization RCode

        :return: The rcode of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :rtype: str
        """
        return self._rcode

    @rcode.setter
    def rcode(self, rcode):
        """
        Sets the rcode of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        Authorization RCode

        :param rcode: The rcode of this ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations.
        :type: str
        """

        self._rcode = rcode

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
        if not isinstance(other, ReportingV3PurchaseRefundDetailsGet200ResponseAuthorizations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
