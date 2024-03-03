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


class VTConfigCardNotPresentReceiptInformationOrderInformation(object):
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
        'email_alias_name': 'str',
        'custom_reply_to_email_address': 'str'
    }

    attribute_map = {
        'email_alias_name': 'emailAliasName',
        'custom_reply_to_email_address': 'customReplyToEmailAddress'
    }

    def __init__(self, email_alias_name=None, custom_reply_to_email_address=None):
        """
        VTConfigCardNotPresentReceiptInformationOrderInformation - a model defined in Swagger
        """

        self._email_alias_name = None
        self._custom_reply_to_email_address = None

        if email_alias_name is not None:
          self.email_alias_name = email_alias_name
        if custom_reply_to_email_address is not None:
          self.custom_reply_to_email_address = custom_reply_to_email_address

    @property
    def email_alias_name(self):
        """
        Gets the email_alias_name of this VTConfigCardNotPresentReceiptInformationOrderInformation.

        :return: The email_alias_name of this VTConfigCardNotPresentReceiptInformationOrderInformation.
        :rtype: str
        """
        return self._email_alias_name

    @email_alias_name.setter
    def email_alias_name(self, email_alias_name):
        """
        Sets the email_alias_name of this VTConfigCardNotPresentReceiptInformationOrderInformation.

        :param email_alias_name: The email_alias_name of this VTConfigCardNotPresentReceiptInformationOrderInformation.
        :type: str
        """

        self._email_alias_name = email_alias_name

    @property
    def custom_reply_to_email_address(self):
        """
        Gets the custom_reply_to_email_address of this VTConfigCardNotPresentReceiptInformationOrderInformation.

        :return: The custom_reply_to_email_address of this VTConfigCardNotPresentReceiptInformationOrderInformation.
        :rtype: str
        """
        return self._custom_reply_to_email_address

    @custom_reply_to_email_address.setter
    def custom_reply_to_email_address(self, custom_reply_to_email_address):
        """
        Sets the custom_reply_to_email_address of this VTConfigCardNotPresentReceiptInformationOrderInformation.

        :param custom_reply_to_email_address: The custom_reply_to_email_address of this VTConfigCardNotPresentReceiptInformationOrderInformation.
        :type: str
        """

        self._custom_reply_to_email_address = custom_reply_to_email_address

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
        if not isinstance(other, VTConfigCardNotPresentReceiptInformationOrderInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
