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


class SAConfigPaymentMethods(object):
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
        'enabled_payment_methods': 'list[str]'
    }

    attribute_map = {
        'enabled_payment_methods': 'enabledPaymentMethods'
    }

    def __init__(self, enabled_payment_methods=None):
        """
        SAConfigPaymentMethods - a model defined in Swagger
        """

        self._enabled_payment_methods = None

        if enabled_payment_methods is not None:
          self.enabled_payment_methods = enabled_payment_methods

    @property
    def enabled_payment_methods(self):
        """
        Gets the enabled_payment_methods of this SAConfigPaymentMethods.

        :return: The enabled_payment_methods of this SAConfigPaymentMethods.
        :rtype: list[str]
        """
        return self._enabled_payment_methods

    @enabled_payment_methods.setter
    def enabled_payment_methods(self, enabled_payment_methods):
        """
        Sets the enabled_payment_methods of this SAConfigPaymentMethods.

        :param enabled_payment_methods: The enabled_payment_methods of this SAConfigPaymentMethods.
        :type: list[str]
        """
        allowed_values = ["CARD", "ECHECK", "VISACHECKOUT", "PAYPAL"]
        if not set(enabled_payment_methods).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `enabled_payment_methods` [{0}], must be a subset of [{1}]"
                .format(", ".join(map(str, set(enabled_payment_methods)-set(allowed_values))),
                        ", ".join(map(str, allowed_values)))
            )

        self._enabled_payment_methods = enabled_payment_methods

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
        if not isinstance(other, SAConfigPaymentMethods):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
