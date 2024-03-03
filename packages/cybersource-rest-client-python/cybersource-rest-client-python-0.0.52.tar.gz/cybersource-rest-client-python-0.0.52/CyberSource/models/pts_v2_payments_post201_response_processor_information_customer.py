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


class PtsV2PaymentsPost201ResponseProcessorInformationCustomer(object):
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
        'personal_id_result': 'str'
    }

    attribute_map = {
        'personal_id_result': 'personalIdResult'
    }

    def __init__(self, personal_id_result=None):
        """
        PtsV2PaymentsPost201ResponseProcessorInformationCustomer - a model defined in Swagger
        """

        self._personal_id_result = None

        if personal_id_result is not None:
          self.personal_id_result = personal_id_result

    @property
    def personal_id_result(self):
        """
        Gets the personal_id_result of this PtsV2PaymentsPost201ResponseProcessorInformationCustomer.
        Personal identifier result. This field is supported only for Redecard in Brazil for CyberSource Latin American Processing. If you included `buyerInformation.personalIdentification[].ID` in the request, this value indicates whether or not `buyerInformation.personalIdentification[].ID` matched a value in a record on file. Returned only when the personal ID result is returned by the processor.  Possible values:   - `Y`: Match  - `N`: No match  - `K`: Not supported  - `U`: Unknown  - `Z`: No response returned **Note** CyberSource Latin American Processing is the name of a specific processing connection that CyberSource supports. In the CyberSource API documentation, CyberSource Latin American Processing does not refer to the general topic of processing in Latin America.The information in this field description is for the specific processing connection called CyberSource Latin American Processing. It is not for any other Latin American processors that CyberSource supports. 

        :return: The personal_id_result of this PtsV2PaymentsPost201ResponseProcessorInformationCustomer.
        :rtype: str
        """
        return self._personal_id_result

    @personal_id_result.setter
    def personal_id_result(self, personal_id_result):
        """
        Sets the personal_id_result of this PtsV2PaymentsPost201ResponseProcessorInformationCustomer.
        Personal identifier result. This field is supported only for Redecard in Brazil for CyberSource Latin American Processing. If you included `buyerInformation.personalIdentification[].ID` in the request, this value indicates whether or not `buyerInformation.personalIdentification[].ID` matched a value in a record on file. Returned only when the personal ID result is returned by the processor.  Possible values:   - `Y`: Match  - `N`: No match  - `K`: Not supported  - `U`: Unknown  - `Z`: No response returned **Note** CyberSource Latin American Processing is the name of a specific processing connection that CyberSource supports. In the CyberSource API documentation, CyberSource Latin American Processing does not refer to the general topic of processing in Latin America.The information in this field description is for the specific processing connection called CyberSource Latin American Processing. It is not for any other Latin American processors that CyberSource supports. 

        :param personal_id_result: The personal_id_result of this PtsV2PaymentsPost201ResponseProcessorInformationCustomer.
        :type: str
        """

        self._personal_id_result = personal_id_result

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
        if not isinstance(other, PtsV2PaymentsPost201ResponseProcessorInformationCustomer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
