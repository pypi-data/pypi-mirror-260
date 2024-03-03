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


class ECheckConfig(object):
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
        'common': 'ECheckConfigCommon',
        'underwriting': 'ECheckConfigUnderwriting',
        'features': 'ECheckConfigFeatures'
    }

    attribute_map = {
        'common': 'common',
        'underwriting': 'underwriting',
        'features': 'features'
    }

    def __init__(self, common=None, underwriting=None, features=None):
        """
        ECheckConfig - a model defined in Swagger
        """

        self._common = None
        self._underwriting = None
        self._features = None

        if common is not None:
          self.common = common
        if underwriting is not None:
          self.underwriting = underwriting
        if features is not None:
          self.features = features

    @property
    def common(self):
        """
        Gets the common of this ECheckConfig.

        :return: The common of this ECheckConfig.
        :rtype: ECheckConfigCommon
        """
        return self._common

    @common.setter
    def common(self, common):
        """
        Sets the common of this ECheckConfig.

        :param common: The common of this ECheckConfig.
        :type: ECheckConfigCommon
        """

        self._common = common

    @property
    def underwriting(self):
        """
        Gets the underwriting of this ECheckConfig.

        :return: The underwriting of this ECheckConfig.
        :rtype: ECheckConfigUnderwriting
        """
        return self._underwriting

    @underwriting.setter
    def underwriting(self, underwriting):
        """
        Sets the underwriting of this ECheckConfig.

        :param underwriting: The underwriting of this ECheckConfig.
        :type: ECheckConfigUnderwriting
        """

        self._underwriting = underwriting

    @property
    def features(self):
        """
        Gets the features of this ECheckConfig.

        :return: The features of this ECheckConfig.
        :rtype: ECheckConfigFeatures
        """
        return self._features

    @features.setter
    def features(self, features):
        """
        Sets the features of this ECheckConfig.

        :param features: The features of this ECheckConfig.
        :type: ECheckConfigFeatures
        """

        self._features = features

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
        if not isinstance(other, ECheckConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
