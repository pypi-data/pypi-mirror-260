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


class PaymentsProductsSecureAcceptanceConfigurationInformation(object):
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
        'template_id': 'str',
        'configurations': 'SAConfig'
    }

    attribute_map = {
        'template_id': 'templateId',
        'configurations': 'configurations'
    }

    def __init__(self, template_id=None, configurations=None):
        """
        PaymentsProductsSecureAcceptanceConfigurationInformation - a model defined in Swagger
        """

        self._template_id = None
        self._configurations = None

        if template_id is not None:
          self.template_id = template_id
        if configurations is not None:
          self.configurations = configurations

    @property
    def template_id(self):
        """
        Gets the template_id of this PaymentsProductsSecureAcceptanceConfigurationInformation.

        :return: The template_id of this PaymentsProductsSecureAcceptanceConfigurationInformation.
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """
        Sets the template_id of this PaymentsProductsSecureAcceptanceConfigurationInformation.

        :param template_id: The template_id of this PaymentsProductsSecureAcceptanceConfigurationInformation.
        :type: str
        """

        self._template_id = template_id

    @property
    def configurations(self):
        """
        Gets the configurations of this PaymentsProductsSecureAcceptanceConfigurationInformation.

        :return: The configurations of this PaymentsProductsSecureAcceptanceConfigurationInformation.
        :rtype: SAConfig
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """
        Sets the configurations of this PaymentsProductsSecureAcceptanceConfigurationInformation.

        :param configurations: The configurations of this PaymentsProductsSecureAcceptanceConfigurationInformation.
        :type: SAConfig
        """

        self._configurations = configurations

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
        if not isinstance(other, PaymentsProductsSecureAcceptanceConfigurationInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
