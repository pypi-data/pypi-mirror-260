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


class Riskv1decisionsProcessorInformationCardVerification(object):
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
        'result_code': 'str'
    }

    attribute_map = {
        'result_code': 'resultCode'
    }

    def __init__(self, result_code=None):
        """
        Riskv1decisionsProcessorInformationCardVerification - a model defined in Swagger
        """

        self._result_code = None

        if result_code is not None:
          self.result_code = result_code

    @property
    def result_code(self):
        """
        Gets the result_code of this Riskv1decisionsProcessorInformationCardVerification.
        CVN result code.  For details, see the `auth_cv_result` reply field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :return: The result_code of this Riskv1decisionsProcessorInformationCardVerification.
        :rtype: str
        """
        return self._result_code

    @result_code.setter
    def result_code(self, result_code):
        """
        Sets the result_code of this Riskv1decisionsProcessorInformationCardVerification.
        CVN result code.  For details, see the `auth_cv_result` reply field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :param result_code: The result_code of this Riskv1decisionsProcessorInformationCardVerification.
        :type: str
        """

        self._result_code = result_code

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
        if not isinstance(other, Riskv1decisionsProcessorInformationCardVerification):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
