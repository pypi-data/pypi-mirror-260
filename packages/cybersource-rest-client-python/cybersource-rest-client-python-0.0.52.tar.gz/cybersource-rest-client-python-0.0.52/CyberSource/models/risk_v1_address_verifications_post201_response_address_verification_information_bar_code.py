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


class RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode(object):
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
        'value': 'str',
        'check_digit': 'float'
    }

    attribute_map = {
        'value': 'value',
        'check_digit': 'checkDigit'
    }

    def __init__(self, value=None, check_digit=None):
        """
        RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode - a model defined in Swagger
        """

        self._value = None
        self._check_digit = None

        if value is not None:
          self.value = value
        if check_digit is not None:
          self.check_digit = check_digit

    @property
    def value(self):
        """
        Gets the value of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        Delivery point bar code determined from the input address.

        :return: The value of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        Delivery point bar code determined from the input address.

        :param value: The value of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        :type: str
        """

        self._value = value

    @property
    def check_digit(self):
        """
        Gets the check_digit of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        Check digit for the 11-digit delivery point bar code.

        :return: The check_digit of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        :rtype: float
        """
        return self._check_digit

    @check_digit.setter
    def check_digit(self, check_digit):
        """
        Sets the check_digit of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        Check digit for the 11-digit delivery point bar code.

        :param check_digit: The check_digit of this RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode.
        :type: float
        """

        self._check_digit = check_digit

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
        if not isinstance(other, RiskV1AddressVerificationsPost201ResponseAddressVerificationInformationBarCode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
