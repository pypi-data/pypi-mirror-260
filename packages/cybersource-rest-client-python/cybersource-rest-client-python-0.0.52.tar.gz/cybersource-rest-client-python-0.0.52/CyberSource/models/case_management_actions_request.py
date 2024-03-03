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


class CaseManagementActionsRequest(object):
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
        'decision_information': 'Riskv1decisionsidactionsDecisionInformation',
        'processing_information': 'Riskv1decisionsidactionsProcessingInformation'
    }

    attribute_map = {
        'decision_information': 'decisionInformation',
        'processing_information': 'processingInformation'
    }

    def __init__(self, decision_information=None, processing_information=None):
        """
        CaseManagementActionsRequest - a model defined in Swagger
        """

        self._decision_information = None
        self._processing_information = None

        self.decision_information = decision_information
        if processing_information is not None:
          self.processing_information = processing_information

    @property
    def decision_information(self):
        """
        Gets the decision_information of this CaseManagementActionsRequest.

        :return: The decision_information of this CaseManagementActionsRequest.
        :rtype: Riskv1decisionsidactionsDecisionInformation
        """
        return self._decision_information

    @decision_information.setter
    def decision_information(self, decision_information):
        """
        Sets the decision_information of this CaseManagementActionsRequest.

        :param decision_information: The decision_information of this CaseManagementActionsRequest.
        :type: Riskv1decisionsidactionsDecisionInformation
        """
        if decision_information is None:
            raise ValueError("Invalid value for `decision_information`, must not be `None`")

        self._decision_information = decision_information

    @property
    def processing_information(self):
        """
        Gets the processing_information of this CaseManagementActionsRequest.

        :return: The processing_information of this CaseManagementActionsRequest.
        :rtype: Riskv1decisionsidactionsProcessingInformation
        """
        return self._processing_information

    @processing_information.setter
    def processing_information(self, processing_information):
        """
        Sets the processing_information of this CaseManagementActionsRequest.

        :param processing_information: The processing_information of this CaseManagementActionsRequest.
        :type: Riskv1decisionsidactionsProcessingInformation
        """

        self._processing_information = processing_information

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
        if not isinstance(other, CaseManagementActionsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
