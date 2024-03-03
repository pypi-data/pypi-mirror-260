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


class GetAllSubscriptionsResponseSubscriptionInformation(object):
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
        'code': 'str',
        'plan_id': 'str',
        'name': 'str',
        'start_date': 'str',
        'status': 'str'
    }

    attribute_map = {
        'code': 'code',
        'plan_id': 'planId',
        'name': 'name',
        'start_date': 'startDate',
        'status': 'status'
    }

    def __init__(self, code=None, plan_id=None, name=None, start_date=None, status=None):
        """
        GetAllSubscriptionsResponseSubscriptionInformation - a model defined in Swagger
        """

        self._code = None
        self._plan_id = None
        self._name = None
        self._start_date = None
        self._status = None

        if code is not None:
          self.code = code
        if plan_id is not None:
          self.plan_id = plan_id
        if name is not None:
          self.name = name
        if start_date is not None:
          self.start_date = start_date
        if status is not None:
          self.status = status

    @property
    def code(self):
        """
        Gets the code of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription code. 

        :return: The code of this GetAllSubscriptionsResponseSubscriptionInformation.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription code. 

        :param code: The code of this GetAllSubscriptionsResponseSubscriptionInformation.
        :type: str
        """

        self._code = code

    @property
    def plan_id(self):
        """
        Gets the plan_id of this GetAllSubscriptionsResponseSubscriptionInformation.
        Plan Id. 

        :return: The plan_id of this GetAllSubscriptionsResponseSubscriptionInformation.
        :rtype: str
        """
        return self._plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        """
        Sets the plan_id of this GetAllSubscriptionsResponseSubscriptionInformation.
        Plan Id. 

        :param plan_id: The plan_id of this GetAllSubscriptionsResponseSubscriptionInformation.
        :type: str
        """

        self._plan_id = plan_id

    @property
    def name(self):
        """
        Gets the name of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription Name 

        :return: The name of this GetAllSubscriptionsResponseSubscriptionInformation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription Name 

        :param name: The name of this GetAllSubscriptionsResponseSubscriptionInformation.
        :type: str
        """

        self._name = name

    @property
    def start_date(self):
        """
        Gets the start_date of this GetAllSubscriptionsResponseSubscriptionInformation.
        Start date of the Subscription  Start date will be in UTC. Format: YYYY-MM-DDThh:mm:ssZ The T separates the date and the time. The Z indicates UTC.  **Example** 2022-08-11T22:47:57Z equals August 11, 2022, at 22:47:57 (10:47:57 p.m.). 

        :return: The start_date of this GetAllSubscriptionsResponseSubscriptionInformation.
        :rtype: str
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this GetAllSubscriptionsResponseSubscriptionInformation.
        Start date of the Subscription  Start date will be in UTC. Format: YYYY-MM-DDThh:mm:ssZ The T separates the date and the time. The Z indicates UTC.  **Example** 2022-08-11T22:47:57Z equals August 11, 2022, at 22:47:57 (10:47:57 p.m.). 

        :param start_date: The start_date of this GetAllSubscriptionsResponseSubscriptionInformation.
        :type: str
        """

        self._start_date = start_date

    @property
    def status(self):
        """
        Gets the status of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription Status: - `PENDING` - `ACTIVE` - `FAILED` - `COMPLETED` - `DELINQUENT` - `SUSPENDED` - `CANCELLED` 

        :return: The status of this GetAllSubscriptionsResponseSubscriptionInformation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this GetAllSubscriptionsResponseSubscriptionInformation.
        Subscription Status: - `PENDING` - `ACTIVE` - `FAILED` - `COMPLETED` - `DELINQUENT` - `SUSPENDED` - `CANCELLED` 

        :param status: The status of this GetAllSubscriptionsResponseSubscriptionInformation.
        :type: str
        """

        self._status = status

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
        if not isinstance(other, GetAllSubscriptionsResponseSubscriptionInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
