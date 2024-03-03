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


class Ptsv2paymentsTravelInformationVehicleData(object):
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
        'connector_type': 'str',
        'charging_reason_code': 'str'
    }

    attribute_map = {
        'connector_type': 'connectorType',
        'charging_reason_code': 'chargingReasonCode'
    }

    def __init__(self, connector_type=None, charging_reason_code=None):
        """
        Ptsv2paymentsTravelInformationVehicleData - a model defined in Swagger
        """

        self._connector_type = None
        self._charging_reason_code = None

        if connector_type is not None:
          self.connector_type = connector_type
        if charging_reason_code is not None:
          self.charging_reason_code = charging_reason_code

    @property
    def connector_type(self):
        """
        Gets the connector_type of this Ptsv2paymentsTravelInformationVehicleData.
        This field will contain connector type values for electric vehicle transactions.  Possible Values: 001 (AC - J1772 Type 1) 002 (AC - Mennekes - Type 2) 003 (AC - GB/T) 100 (DC - CCS1) 101 (DC - CHAdeMO) 102 (DC - CCS2) 103 (DC - GB/T) 200 (NACS – Tesla) 

        :return: The connector_type of this Ptsv2paymentsTravelInformationVehicleData.
        :rtype: str
        """
        return self._connector_type

    @connector_type.setter
    def connector_type(self, connector_type):
        """
        Sets the connector_type of this Ptsv2paymentsTravelInformationVehicleData.
        This field will contain connector type values for electric vehicle transactions.  Possible Values: 001 (AC - J1772 Type 1) 002 (AC - Mennekes - Type 2) 003 (AC - GB/T) 100 (DC - CCS1) 101 (DC - CHAdeMO) 102 (DC - CCS2) 103 (DC - GB/T) 200 (NACS – Tesla) 

        :param connector_type: The connector_type of this Ptsv2paymentsTravelInformationVehicleData.
        :type: str
        """

        self._connector_type = connector_type

    @property
    def charging_reason_code(self):
        """
        Gets the charging_reason_code of this Ptsv2paymentsTravelInformationVehicleData.
        This field will contain charging reason code values for electric vehicle transactions.  Possible Values: 010 (Other Error) 011 (Connector Lock Failure) 012 (EV Communication Error) 013 (Ground Failure) 014 (High Temperature) 015 (Internal Error) 016 (Over Current Failure) 017 (Over Voltage) 018 (Power Meter Failure) 019 (Power Switch Failure) 020 (Reader Failure) 021 (Reset Failure) 022 (Under Voltage) 023 (Weak Signal) 100 (No Error) 200 (Payment Related Error) 

        :return: The charging_reason_code of this Ptsv2paymentsTravelInformationVehicleData.
        :rtype: str
        """
        return self._charging_reason_code

    @charging_reason_code.setter
    def charging_reason_code(self, charging_reason_code):
        """
        Sets the charging_reason_code of this Ptsv2paymentsTravelInformationVehicleData.
        This field will contain charging reason code values for electric vehicle transactions.  Possible Values: 010 (Other Error) 011 (Connector Lock Failure) 012 (EV Communication Error) 013 (Ground Failure) 014 (High Temperature) 015 (Internal Error) 016 (Over Current Failure) 017 (Over Voltage) 018 (Power Meter Failure) 019 (Power Switch Failure) 020 (Reader Failure) 021 (Reset Failure) 022 (Under Voltage) 023 (Weak Signal) 100 (No Error) 200 (Payment Related Error) 

        :param charging_reason_code: The charging_reason_code of this Ptsv2paymentsTravelInformationVehicleData.
        :type: str
        """

        self._charging_reason_code = charging_reason_code

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
        if not isinstance(other, Ptsv2paymentsTravelInformationVehicleData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
