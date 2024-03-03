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


class InlineResponse200EmbeddedReversal(object):
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
        'status': 'str',
        'links': 'InlineResponse200EmbeddedReversalLinks'
    }

    attribute_map = {
        'status': 'status',
        'links': '_links'
    }

    def __init__(self, status=None, links=None):
        """
        InlineResponse200EmbeddedReversal - a model defined in Swagger
        """

        self._status = None
        self._links = None

        if status is not None:
          self.status = status
        if links is not None:
          self.links = links

    @property
    def status(self):
        """
        Gets the status of this InlineResponse200EmbeddedReversal.
        The status of the reversal if the auth reversal is called. 

        :return: The status of this InlineResponse200EmbeddedReversal.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this InlineResponse200EmbeddedReversal.
        The status of the reversal if the auth reversal is called. 

        :param status: The status of this InlineResponse200EmbeddedReversal.
        :type: str
        """

        self._status = status

    @property
    def links(self):
        """
        Gets the links of this InlineResponse200EmbeddedReversal.

        :return: The links of this InlineResponse200EmbeddedReversal.
        :rtype: InlineResponse200EmbeddedReversalLinks
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this InlineResponse200EmbeddedReversal.

        :param links: The links of this InlineResponse200EmbeddedReversal.
        :type: InlineResponse200EmbeddedReversalLinks
        """

        self._links = links

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
        if not isinstance(other, InlineResponse200EmbeddedReversal):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
