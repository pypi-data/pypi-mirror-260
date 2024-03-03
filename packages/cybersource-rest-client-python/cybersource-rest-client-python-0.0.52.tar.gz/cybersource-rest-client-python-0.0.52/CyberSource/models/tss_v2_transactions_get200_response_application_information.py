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


class TssV2TransactionsGet200ResponseApplicationInformation(object):
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
        'reason_code': 'str',
        'r_code': 'str',
        'r_flag': 'str',
        'applications': 'list[TssV2TransactionsGet200ResponseApplicationInformationApplications]'
    }

    attribute_map = {
        'status': 'status',
        'reason_code': 'reasonCode',
        'r_code': 'rCode',
        'r_flag': 'rFlag',
        'applications': 'applications'
    }

    def __init__(self, status=None, reason_code=None, r_code=None, r_flag=None, applications=None):
        """
        TssV2TransactionsGet200ResponseApplicationInformation - a model defined in Swagger
        """

        self._status = None
        self._reason_code = None
        self._r_code = None
        self._r_flag = None
        self._applications = None

        if status is not None:
          self.status = status
        if reason_code is not None:
          self.reason_code = reason_code
        if r_code is not None:
          self.r_code = r_code
        if r_flag is not None:
          self.r_flag = r_flag
        if applications is not None:
          self.applications = applications

    @property
    def status(self):
        """
        Gets the status of this TssV2TransactionsGet200ResponseApplicationInformation.
        The status of the submitted transaction.

        :return: The status of this TssV2TransactionsGet200ResponseApplicationInformation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this TssV2TransactionsGet200ResponseApplicationInformation.
        The status of the submitted transaction.

        :param status: The status of this TssV2TransactionsGet200ResponseApplicationInformation.
        :type: str
        """

        self._status = status

    @property
    def reason_code(self):
        """
        Gets the reason_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        Indicates the reason why a request succeeded or failed and possible action to take if a request fails.  For details, see the appendix of reason codes in the documentation for the relevant payment method. 

        :return: The reason_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        :rtype: str
        """
        return self._reason_code

    @reason_code.setter
    def reason_code(self, reason_code):
        """
        Sets the reason_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        Indicates the reason why a request succeeded or failed and possible action to take if a request fails.  For details, see the appendix of reason codes in the documentation for the relevant payment method. 

        :param reason_code: The reason_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        :type: str
        """

        self._reason_code = reason_code

    @property
    def r_code(self):
        """
        Gets the r_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        Indicates whether the service request was successful. Possible values:  - `-1`: An error occurred. - `0`: The request was declined. - `1`: The request was successful. 

        :return: The r_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        :rtype: str
        """
        return self._r_code

    @r_code.setter
    def r_code(self, r_code):
        """
        Sets the r_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        Indicates whether the service request was successful. Possible values:  - `-1`: An error occurred. - `0`: The request was declined. - `1`: The request was successful. 

        :param r_code: The r_code of this TssV2TransactionsGet200ResponseApplicationInformation.
        :type: str
        """

        self._r_code = r_code

    @property
    def r_flag(self):
        """
        Gets the r_flag of this TssV2TransactionsGet200ResponseApplicationInformation.
        One-word description of the result of the application. 

        :return: The r_flag of this TssV2TransactionsGet200ResponseApplicationInformation.
        :rtype: str
        """
        return self._r_flag

    @r_flag.setter
    def r_flag(self, r_flag):
        """
        Sets the r_flag of this TssV2TransactionsGet200ResponseApplicationInformation.
        One-word description of the result of the application. 

        :param r_flag: The r_flag of this TssV2TransactionsGet200ResponseApplicationInformation.
        :type: str
        """

        self._r_flag = r_flag

    @property
    def applications(self):
        """
        Gets the applications of this TssV2TransactionsGet200ResponseApplicationInformation.

        :return: The applications of this TssV2TransactionsGet200ResponseApplicationInformation.
        :rtype: list[TssV2TransactionsGet200ResponseApplicationInformationApplications]
        """
        return self._applications

    @applications.setter
    def applications(self, applications):
        """
        Sets the applications of this TssV2TransactionsGet200ResponseApplicationInformation.

        :param applications: The applications of this TssV2TransactionsGet200ResponseApplicationInformation.
        :type: list[TssV2TransactionsGet200ResponseApplicationInformationApplications]
        """

        self._applications = applications

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
        if not isinstance(other, TssV2TransactionsGet200ResponseApplicationInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
