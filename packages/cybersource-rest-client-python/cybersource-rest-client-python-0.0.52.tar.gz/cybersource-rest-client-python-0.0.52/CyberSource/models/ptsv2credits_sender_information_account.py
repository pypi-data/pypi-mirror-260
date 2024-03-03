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


class Ptsv2creditsSenderInformationAccount(object):
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
        'number': 'str',
        'funds_source': 'str'
    }

    attribute_map = {
        'number': 'number',
        'funds_source': 'fundsSource'
    }

    def __init__(self, number=None, funds_source=None):
        """
        Ptsv2creditsSenderInformationAccount - a model defined in Swagger
        """

        self._number = None
        self._funds_source = None

        if number is not None:
          self.number = number
        if funds_source is not None:
          self.funds_source = funds_source

    @property
    def number(self):
        """
        Gets the number of this Ptsv2creditsSenderInformationAccount.
        Account number of the sender of the funds. For Gaming Payment of Winnings transactions this is the merchant account number. * Required for Mastercard Payment of Winnings (POW) transactions. * Must contain only ASCII characters in range 32-122. * Must not be greater than 50 characters. * Required for POW on Barclays. 

        :return: The number of this Ptsv2creditsSenderInformationAccount.
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Sets the number of this Ptsv2creditsSenderInformationAccount.
        Account number of the sender of the funds. For Gaming Payment of Winnings transactions this is the merchant account number. * Required for Mastercard Payment of Winnings (POW) transactions. * Must contain only ASCII characters in range 32-122. * Must not be greater than 50 characters. * Required for POW on Barclays. 

        :param number: The number of this Ptsv2creditsSenderInformationAccount.
        :type: str
        """

        self._number = number

    @property
    def funds_source(self):
        """
        Gets the funds_source of this Ptsv2creditsSenderInformationAccount.
        Source of funds for the sender. For Gaming Payment of Winnings transactions this is the merchant account type. * Required for Mastercard Payment of Winnings (POW) transactions. * Valid values:   * 00 - Other   * 01 - RTN + Bank Account   * 02 - IBAN   * 03 - Card Account   * 04 - Email   * 05 - PhoneNumber   * 06 - Bank account number (BAN) + Bank Identification Code (BIC)   * 07 - Wallet ID   * 08 - Social Network ID 

        :return: The funds_source of this Ptsv2creditsSenderInformationAccount.
        :rtype: str
        """
        return self._funds_source

    @funds_source.setter
    def funds_source(self, funds_source):
        """
        Sets the funds_source of this Ptsv2creditsSenderInformationAccount.
        Source of funds for the sender. For Gaming Payment of Winnings transactions this is the merchant account type. * Required for Mastercard Payment of Winnings (POW) transactions. * Valid values:   * 00 - Other   * 01 - RTN + Bank Account   * 02 - IBAN   * 03 - Card Account   * 04 - Email   * 05 - PhoneNumber   * 06 - Bank account number (BAN) + Bank Identification Code (BIC)   * 07 - Wallet ID   * 08 - Social Network ID 

        :param funds_source: The funds_source of this Ptsv2creditsSenderInformationAccount.
        :type: str
        """

        self._funds_source = funds_source

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
        if not isinstance(other, Ptsv2creditsSenderInformationAccount):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
