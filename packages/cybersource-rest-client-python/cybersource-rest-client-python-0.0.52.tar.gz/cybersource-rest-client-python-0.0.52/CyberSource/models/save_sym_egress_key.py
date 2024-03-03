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


class SaveSymEgressKey(object):
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
        'client_reference_information': 'Kmsegressv2keyssymClientReferenceInformation',
        'client_request_action': 'str',
        'key_information': 'Kmsegressv2keyssymKeyInformation'
    }

    attribute_map = {
        'client_reference_information': 'clientReferenceInformation',
        'client_request_action': 'clientRequestAction',
        'key_information': 'keyInformation'
    }

    def __init__(self, client_reference_information=None, client_request_action=None, key_information=None):
        """
        SaveSymEgressKey - a model defined in Swagger
        """

        self._client_reference_information = None
        self._client_request_action = None
        self._key_information = None

        if client_reference_information is not None:
          self.client_reference_information = client_reference_information
        self.client_request_action = client_request_action
        self.key_information = key_information

    @property
    def client_reference_information(self):
        """
        Gets the client_reference_information of this SaveSymEgressKey.

        :return: The client_reference_information of this SaveSymEgressKey.
        :rtype: Kmsegressv2keyssymClientReferenceInformation
        """
        return self._client_reference_information

    @client_reference_information.setter
    def client_reference_information(self, client_reference_information):
        """
        Sets the client_reference_information of this SaveSymEgressKey.

        :param client_reference_information: The client_reference_information of this SaveSymEgressKey.
        :type: Kmsegressv2keyssymClientReferenceInformation
        """

        self._client_reference_information = client_reference_information

    @property
    def client_request_action(self):
        """
        Gets the client_request_action of this SaveSymEgressKey.
        Client request action. 

        :return: The client_request_action of this SaveSymEgressKey.
        :rtype: str
        """
        return self._client_request_action

    @client_request_action.setter
    def client_request_action(self, client_request_action):
        """
        Sets the client_request_action of this SaveSymEgressKey.
        Client request action. 

        :param client_request_action: The client_request_action of this SaveSymEgressKey.
        :type: str
        """
        if client_request_action is None:
            raise ValueError("Invalid value for `client_request_action`, must not be `None`")

        self._client_request_action = client_request_action

    @property
    def key_information(self):
        """
        Gets the key_information of this SaveSymEgressKey.

        :return: The key_information of this SaveSymEgressKey.
        :rtype: Kmsegressv2keyssymKeyInformation
        """
        return self._key_information

    @key_information.setter
    def key_information(self, key_information):
        """
        Sets the key_information of this SaveSymEgressKey.

        :param key_information: The key_information of this SaveSymEgressKey.
        :type: Kmsegressv2keyssymKeyInformation
        """
        if key_information is None:
            raise ValueError("Invalid value for `key_information`, must not be `None`")

        self._key_information = key_information

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
        if not isinstance(other, SaveSymEgressKey):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
