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


class ReportingV3ConversionDetailsGet200ResponseNotes(object):
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
        'time': 'datetime',
        'added_by': 'str',
        'comments': 'str'
    }

    attribute_map = {
        'time': 'time',
        'added_by': 'addedBy',
        'comments': 'comments'
    }

    def __init__(self, time=None, added_by=None, comments=None):
        """
        ReportingV3ConversionDetailsGet200ResponseNotes - a model defined in Swagger
        """

        self._time = None
        self._added_by = None
        self._comments = None

        if time is not None:
          self.time = time
        if added_by is not None:
          self.added_by = added_by
        if comments is not None:
          self.comments = comments

    @property
    def time(self):
        """
        Gets the time of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Time of the note added by reviewer

        :return: The time of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Time of the note added by reviewer

        :param time: The time of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :type: datetime
        """

        self._time = time

    @property
    def added_by(self):
        """
        Gets the added_by of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Note added by reviewer

        :return: The added_by of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :rtype: str
        """
        return self._added_by

    @added_by.setter
    def added_by(self, added_by):
        """
        Sets the added_by of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Note added by reviewer

        :param added_by: The added_by of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :type: str
        """

        self._added_by = added_by

    @property
    def comments(self):
        """
        Gets the comments of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Comments given by the reviewer

        :return: The comments of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this ReportingV3ConversionDetailsGet200ResponseNotes.
        Comments given by the reviewer

        :param comments: The comments of this ReportingV3ConversionDetailsGet200ResponseNotes.
        :type: str
        """

        self._comments = comments

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
        if not isinstance(other, ReportingV3ConversionDetailsGet200ResponseNotes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
