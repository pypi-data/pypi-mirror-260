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


class TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner(object):
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
        'solution_id': 'str'
    }

    attribute_map = {
        'solution_id': 'solutionId'
    }

    def __init__(self, solution_id=None):
        """
        TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner - a model defined in Swagger
        """

        self._solution_id = None

        if solution_id is not None:
          self.solution_id = solution_id

    @property
    def solution_id(self):
        """
        Gets the solution_id of this TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner.
        Identifier for the partner that is integrated to CyberSource.  Send this value in all requests that are sent through the partner solution. CyberSource assigns the ID to the partner.  **Note** When you see a solutionId of 999 in reports, the solutionId that was submitted is incorrect. 

        :return: The solution_id of this TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner.
        :rtype: str
        """
        return self._solution_id

    @solution_id.setter
    def solution_id(self, solution_id):
        """
        Sets the solution_id of this TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner.
        Identifier for the partner that is integrated to CyberSource.  Send this value in all requests that are sent through the partner solution. CyberSource assigns the ID to the partner.  **Note** When you see a solutionId of 999 in reports, the solutionId that was submitted is incorrect. 

        :param solution_id: The solution_id of this TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner.
        :type: str
        """

        self._solution_id = solution_id

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
        if not isinstance(other, TssV2TransactionsPost201ResponseEmbeddedClientReferenceInformationPartner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
