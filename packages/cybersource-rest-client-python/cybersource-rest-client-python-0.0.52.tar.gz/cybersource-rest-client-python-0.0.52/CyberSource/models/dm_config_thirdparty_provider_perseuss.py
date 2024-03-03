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


class DmConfigThirdpartyProviderPerseuss(object):
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
        'enabled': 'bool',
        'enable_real_time': 'bool',
        'credentials': 'DmConfigThirdpartyProviderAccurintCredentials'
    }

    attribute_map = {
        'enabled': 'enabled',
        'enable_real_time': 'enableRealTime',
        'credentials': 'credentials'
    }

    def __init__(self, enabled=None, enable_real_time=None, credentials=None):
        """
        DmConfigThirdpartyProviderPerseuss - a model defined in Swagger
        """

        self._enabled = None
        self._enable_real_time = None
        self._credentials = None

        if enabled is not None:
          self.enabled = enabled
        if enable_real_time is not None:
          self.enable_real_time = enable_real_time
        if credentials is not None:
          self.credentials = credentials

    @property
    def enabled(self):
        """
        Gets the enabled of this DmConfigThirdpartyProviderPerseuss.

        :return: The enabled of this DmConfigThirdpartyProviderPerseuss.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this DmConfigThirdpartyProviderPerseuss.

        :param enabled: The enabled of this DmConfigThirdpartyProviderPerseuss.
        :type: bool
        """

        self._enabled = enabled

    @property
    def enable_real_time(self):
        """
        Gets the enable_real_time of this DmConfigThirdpartyProviderPerseuss.

        :return: The enable_real_time of this DmConfigThirdpartyProviderPerseuss.
        :rtype: bool
        """
        return self._enable_real_time

    @enable_real_time.setter
    def enable_real_time(self, enable_real_time):
        """
        Sets the enable_real_time of this DmConfigThirdpartyProviderPerseuss.

        :param enable_real_time: The enable_real_time of this DmConfigThirdpartyProviderPerseuss.
        :type: bool
        """

        self._enable_real_time = enable_real_time

    @property
    def credentials(self):
        """
        Gets the credentials of this DmConfigThirdpartyProviderPerseuss.

        :return: The credentials of this DmConfigThirdpartyProviderPerseuss.
        :rtype: DmConfigThirdpartyProviderAccurintCredentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this DmConfigThirdpartyProviderPerseuss.

        :param credentials: The credentials of this DmConfigThirdpartyProviderPerseuss.
        :type: DmConfigThirdpartyProviderAccurintCredentials
        """

        self._credentials = credentials

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
        if not isinstance(other, DmConfigThirdpartyProviderPerseuss):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
