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


class Ptsv2paymentsMerchantDefinedInformation(object):
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
        'key': 'str',
        'value': 'str'
    }

    attribute_map = {
        'key': 'key',
        'value': 'value'
    }

    def __init__(self, key=None, value=None):
        """
        Ptsv2paymentsMerchantDefinedInformation - a model defined in Swagger
        """

        self._key = None
        self._value = None

        if key is not None:
          self.key = key
        if value is not None:
          self.value = value

    @property
    def key(self):
        """
        Gets the key of this Ptsv2paymentsMerchantDefinedInformation.
        The number you assign for as the key for your merchant-defined data field. Valid values are 0 to 100.  For example, to set or access the key for the 2nd merchant-defined data field in the array, you would reference `merchantDefinedInformation[1].key`.  #### CyberSource through VisaNet For installment payments with Mastercard in Brazil, use `merchantDefinedInformation[0].key` and `merchantDefinedInformation[1].key` for data that you want to provide to the issuer to identify the transaction.  For details, see the `merchant_defined_data1` request-level field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :return: The key of this Ptsv2paymentsMerchantDefinedInformation.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this Ptsv2paymentsMerchantDefinedInformation.
        The number you assign for as the key for your merchant-defined data field. Valid values are 0 to 100.  For example, to set or access the key for the 2nd merchant-defined data field in the array, you would reference `merchantDefinedInformation[1].key`.  #### CyberSource through VisaNet For installment payments with Mastercard in Brazil, use `merchantDefinedInformation[0].key` and `merchantDefinedInformation[1].key` for data that you want to provide to the issuer to identify the transaction.  For details, see the `merchant_defined_data1` request-level field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :param key: The key of this Ptsv2paymentsMerchantDefinedInformation.
        :type: str
        """

        self._key = key

    @property
    def value(self):
        """
        Gets the value of this Ptsv2paymentsMerchantDefinedInformation.
        The value you assign for your merchant-defined data field.  For details, see `merchant_defined_data1` field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  **Warning** Merchant-defined data fields are not intended to and must not be used to capture personally identifying information. Accordingly, merchants are prohibited from capturing, obtaining, and/or transmitting any personally identifying information in or via the merchant-defined data fields. Personally identifying information includes, but is not limited to, address, credit card number, social security number, driver's license number, state-issued identification number, passport number, and card verification numbers (CVV, CVC2, CVV2, CID, CVN). In the event CyberSource discovers that a merchant is capturing and/or transmitting personally identifying information via the merchant-defined data fields, whether or not intentionally, CyberSource will immediately suspend the merchant's account, which will result in a rejection of any and all transaction requests submitted by the merchant after the point of suspension.  #### CyberSource through VisaNet For installment payments with Mastercard in Brazil, use `merchantDefinedInformation[0].value` and `merchantDefinedInformation[1].value` for data that you want to provide to the issuer to identify the transaction. For details, see \"Installment Payments on CyberSource through VisaNet\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  For details, see \"Installment Payments on CyberSource through VisaNet\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  For installment payments with Mastercard in Brazil: - The value for merchantDefinedInformation[0].value corresponds to the following data in the TC 33 capture file5:   - Record: CP07 TCR5   - Position: 25-44   - Field: Reference Field 2 - The value for merchantDefinedInformation[1].value corresponds to the following data in the TC 33 capture file5:   - Record: CP07 TCR5   - Position: 45-64   - Field: Reference Field 3 

        :return: The value of this Ptsv2paymentsMerchantDefinedInformation.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this Ptsv2paymentsMerchantDefinedInformation.
        The value you assign for your merchant-defined data field.  For details, see `merchant_defined_data1` field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  **Warning** Merchant-defined data fields are not intended to and must not be used to capture personally identifying information. Accordingly, merchants are prohibited from capturing, obtaining, and/or transmitting any personally identifying information in or via the merchant-defined data fields. Personally identifying information includes, but is not limited to, address, credit card number, social security number, driver's license number, state-issued identification number, passport number, and card verification numbers (CVV, CVC2, CVV2, CID, CVN). In the event CyberSource discovers that a merchant is capturing and/or transmitting personally identifying information via the merchant-defined data fields, whether or not intentionally, CyberSource will immediately suspend the merchant's account, which will result in a rejection of any and all transaction requests submitted by the merchant after the point of suspension.  #### CyberSource through VisaNet For installment payments with Mastercard in Brazil, use `merchantDefinedInformation[0].value` and `merchantDefinedInformation[1].value` for data that you want to provide to the issuer to identify the transaction. For details, see \"Installment Payments on CyberSource through VisaNet\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  For details, see \"Installment Payments on CyberSource through VisaNet\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  For installment payments with Mastercard in Brazil: - The value for merchantDefinedInformation[0].value corresponds to the following data in the TC 33 capture file5:   - Record: CP07 TCR5   - Position: 25-44   - Field: Reference Field 2 - The value for merchantDefinedInformation[1].value corresponds to the following data in the TC 33 capture file5:   - Record: CP07 TCR5   - Position: 45-64   - Field: Reference Field 3 

        :param value: The value of this Ptsv2paymentsMerchantDefinedInformation.
        :type: str
        """

        self._value = value

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
        if not isinstance(other, Ptsv2paymentsMerchantDefinedInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
