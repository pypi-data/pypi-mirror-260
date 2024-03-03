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


class Ptsv2voidsProcessingInformation(object):
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
        'payment_id': 'str'
    }

    attribute_map = {
        'payment_id': 'paymentId'
    }

    def __init__(self, payment_id=None):
        """
        Ptsv2voidsProcessingInformation - a model defined in Swagger
        """

        self._payment_id = None

        if payment_id is not None:
          self.payment_id = payment_id

    @property
    def payment_id(self):
        """
        Gets the payment_id of this Ptsv2voidsProcessingInformation.
        This field is to accept the id of credit/capture in the body of L1 requests so the type of void can be identified and processed correctly downstream.

        :return: The payment_id of this Ptsv2voidsProcessingInformation.
        :rtype: str
        """
        return self._payment_id

    @payment_id.setter
    def payment_id(self, payment_id):
        """
        Sets the payment_id of this Ptsv2voidsProcessingInformation.
        This field is to accept the id of credit/capture in the body of L1 requests so the type of void can be identified and processed correctly downstream.

        :param payment_id: The payment_id of this Ptsv2voidsProcessingInformation.
        :type: str
        """

        self._payment_id = payment_id

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
        if not isinstance(other, Ptsv2voidsProcessingInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
