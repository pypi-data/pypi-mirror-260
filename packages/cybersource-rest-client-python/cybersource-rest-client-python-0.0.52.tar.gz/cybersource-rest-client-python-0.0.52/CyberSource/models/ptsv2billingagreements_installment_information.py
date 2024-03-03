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


class Ptsv2billingagreementsInstallmentInformation(object):
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
        'alert_preference': 'str',
        'first_installment_date': 'str',
        'identifier': 'str',
        'last_installment_date': 'str',
        'max_amount': 'str',
        'min_amount': 'str',
        'payment_type': 'str',
        'preferred_day': 'str',
        'sequence': 'int'
    }

    attribute_map = {
        'alert_preference': 'alertPreference',
        'first_installment_date': 'firstInstallmentDate',
        'identifier': 'identifier',
        'last_installment_date': 'lastInstallmentDate',
        'max_amount': 'maxAmount',
        'min_amount': 'minAmount',
        'payment_type': 'paymentType',
        'preferred_day': 'preferredDay',
        'sequence': 'sequence'
    }

    def __init__(self, alert_preference=None, first_installment_date=None, identifier=None, last_installment_date=None, max_amount=None, min_amount=None, payment_type=None, preferred_day=None, sequence=None):
        """
        Ptsv2billingagreementsInstallmentInformation - a model defined in Swagger
        """

        self._alert_preference = None
        self._first_installment_date = None
        self._identifier = None
        self._last_installment_date = None
        self._max_amount = None
        self._min_amount = None
        self._payment_type = None
        self._preferred_day = None
        self._sequence = None

        if alert_preference is not None:
          self.alert_preference = alert_preference
        if first_installment_date is not None:
          self.first_installment_date = first_installment_date
        if identifier is not None:
          self.identifier = identifier
        if last_installment_date is not None:
          self.last_installment_date = last_installment_date
        if max_amount is not None:
          self.max_amount = max_amount
        if min_amount is not None:
          self.min_amount = min_amount
        if payment_type is not None:
          self.payment_type = payment_type
        if preferred_day is not None:
          self.preferred_day = preferred_day
        if sequence is not None:
          self.sequence = sequence

    @property
    def alert_preference(self):
        """
        Gets the alert_preference of this Ptsv2billingagreementsInstallmentInformation.
        Applicable only for SI. Required in case the authentication is initiated for SI registration. Valid Values: - `SMS` - `EMAIL` - `BOTH` 

        :return: The alert_preference of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._alert_preference

    @alert_preference.setter
    def alert_preference(self, alert_preference):
        """
        Sets the alert_preference of this Ptsv2billingagreementsInstallmentInformation.
        Applicable only for SI. Required in case the authentication is initiated for SI registration. Valid Values: - `SMS` - `EMAIL` - `BOTH` 

        :param alert_preference: The alert_preference of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._alert_preference = alert_preference

    @property
    def first_installment_date(self):
        """
        Gets the first_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        Date of the first installment payment. Format: YYMMDD. When you do not include this field, CyberSource sends a string of six zeros (000000) to the processor. For details, see \"Installment Payments on CyberSource through VisaNet\" in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  This field is supported only for Crediario installment payments in Brazil on CyberSource through VisaNet.  The value for this field corresponds to the following data in the TC 33 capture file: - Record: CP01 TCR9 - Position: 42-47 - Field: Date of First Installment 

        :return: The first_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._first_installment_date

    @first_installment_date.setter
    def first_installment_date(self, first_installment_date):
        """
        Sets the first_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        Date of the first installment payment. Format: YYMMDD. When you do not include this field, CyberSource sends a string of six zeros (000000) to the processor. For details, see \"Installment Payments on CyberSource through VisaNet\" in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  This field is supported only for Crediario installment payments in Brazil on CyberSource through VisaNet.  The value for this field corresponds to the following data in the TC 33 capture file: - Record: CP01 TCR9 - Position: 42-47 - Field: Date of First Installment 

        :param first_installment_date: The first_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._first_installment_date = first_installment_date

    @property
    def identifier(self):
        """
        Gets the identifier of this Ptsv2billingagreementsInstallmentInformation.
        Standing Instruction/Installment identifier. 

        :return: The identifier of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this Ptsv2billingagreementsInstallmentInformation.
        Standing Instruction/Installment identifier. 

        :param identifier: The identifier of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._identifier = identifier

    @property
    def last_installment_date(self):
        """
        Gets the last_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        End date of the SI transactions. Cannot be later than card expiry date. Ideally this can be set to expiry date. Required in case the authentication is initiated for SI registration. 

        :return: The last_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._last_installment_date

    @last_installment_date.setter
    def last_installment_date(self, last_installment_date):
        """
        Sets the last_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        End date of the SI transactions. Cannot be later than card expiry date. Ideally this can be set to expiry date. Required in case the authentication is initiated for SI registration. 

        :param last_installment_date: The last_installment_date of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._last_installment_date = last_installment_date

    @property
    def max_amount(self):
        """
        Gets the max_amount of this Ptsv2billingagreementsInstallmentInformation.
        Maximum Amount for which SI can be initiated. Required in case the authentication is initiated for SI registration. 

        :return: The max_amount of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._max_amount

    @max_amount.setter
    def max_amount(self, max_amount):
        """
        Sets the max_amount of this Ptsv2billingagreementsInstallmentInformation.
        Maximum Amount for which SI can be initiated. Required in case the authentication is initiated for SI registration. 

        :param max_amount: The max_amount of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._max_amount = max_amount

    @property
    def min_amount(self):
        """
        Gets the min_amount of this Ptsv2billingagreementsInstallmentInformation.
        Minimum Amount for which SI can be initiated. Required in case the authentication is initiated for SI registration. 

        :return: The min_amount of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._min_amount

    @min_amount.setter
    def min_amount(self, min_amount):
        """
        Sets the min_amount of this Ptsv2billingagreementsInstallmentInformation.
        Minimum Amount for which SI can be initiated. Required in case the authentication is initiated for SI registration. 

        :param min_amount: The min_amount of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._min_amount = min_amount

    @property
    def payment_type(self):
        """
        Gets the payment_type of this Ptsv2billingagreementsInstallmentInformation.
        Payment plan for the installments.  Possible values: - 0 (default): Regular installment. This value is not allowed for airline transactions. - 1: Installment payment with down payment. - 2: Installment payment without down payment. This value is supported only for airline transactions. - 3: Installment payment; down payment and boarding fee will follow. This value is supported only for airline transactions. - 4: Down payment only; regular installment payment will follow. - 5: Boarding fee only. This value is supported only for airline transactions.  This field is supported only for installment payments with Visa on CyberSource through VisaNet in Brazil.  For details, see \"Installment Payments on CyberSource through VisaNet\" in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP07 TCR1 - Position: 9 - Field: Merchant Installment Supporting Information 

        :return: The payment_type of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._payment_type

    @payment_type.setter
    def payment_type(self, payment_type):
        """
        Sets the payment_type of this Ptsv2billingagreementsInstallmentInformation.
        Payment plan for the installments.  Possible values: - 0 (default): Regular installment. This value is not allowed for airline transactions. - 1: Installment payment with down payment. - 2: Installment payment without down payment. This value is supported only for airline transactions. - 3: Installment payment; down payment and boarding fee will follow. This value is supported only for airline transactions. - 4: Down payment only; regular installment payment will follow. - 5: Boarding fee only. This value is supported only for airline transactions.  This field is supported only for installment payments with Visa on CyberSource through VisaNet in Brazil.  For details, see \"Installment Payments on CyberSource through VisaNet\" in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  The value for this field corresponds to the following data in the TC 33 capture file5: - Record: CP07 TCR1 - Position: 9 - Field: Merchant Installment Supporting Information 

        :param payment_type: The payment_type of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._payment_type = payment_type

    @property
    def preferred_day(self):
        """
        Gets the preferred_day of this Ptsv2billingagreementsInstallmentInformation.
        Preferred date for initiating the SI transaction every month. This field need not be sent in case the SI has to be initiated as and when required, e.g., topping up the wallet, etc. 

        :return: The preferred_day of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: str
        """
        return self._preferred_day

    @preferred_day.setter
    def preferred_day(self, preferred_day):
        """
        Sets the preferred_day of this Ptsv2billingagreementsInstallmentInformation.
        Preferred date for initiating the SI transaction every month. This field need not be sent in case the SI has to be initiated as and when required, e.g., topping up the wallet, etc. 

        :param preferred_day: The preferred_day of this Ptsv2billingagreementsInstallmentInformation.
        :type: str
        """

        self._preferred_day = preferred_day

    @property
    def sequence(self):
        """
        Gets the sequence of this Ptsv2billingagreementsInstallmentInformation.
        Installment number when making payments in installments. Used along with `totalCount` to track which payment is being processed.  For example, the second of 5 payments would be passed to CyberSource as `sequence` = 2 and `totalCount` = 5.  For details, see \"Installment Payments\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### Chase Paymentech Solutions and FDC Compass This field is optional because this value is required in the merchant descriptors. For details, see \"Chase Paymentech Solutions Merchant Descriptors\" and \"FDC Compass Merchant Descriptors\" in the [Merchant Descriptors Using the SCMP API] (https://apps.cybersource.com/library/documentation/dev_guides/Merchant_Descriptors_SCMP_API/html/)  #### CyberSource through VisaNet When you do not include this field in a request for a Crediario installment payment, CyberSource sends a value of 0 to the processor.  For Crediario installment payments, the value for this field corresponds to the following data in the TC 33 capture file*: - Record: CP01 TCR9 - Position: 38-40 - Field: Installment Payment Number  * The TC 33 Capture file contains information about the purchases and refunds that a merchant submits to CyberSource. CyberSource through VisaNet creates the TC 33 Capture file at the end of the day and sends it to the merchant's acquirer, who uses this information to facilitate end-of-day clearing processing with payment card companies. 

        :return: The sequence of this Ptsv2billingagreementsInstallmentInformation.
        :rtype: int
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """
        Sets the sequence of this Ptsv2billingagreementsInstallmentInformation.
        Installment number when making payments in installments. Used along with `totalCount` to track which payment is being processed.  For example, the second of 5 payments would be passed to CyberSource as `sequence` = 2 and `totalCount` = 5.  For details, see \"Installment Payments\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### Chase Paymentech Solutions and FDC Compass This field is optional because this value is required in the merchant descriptors. For details, see \"Chase Paymentech Solutions Merchant Descriptors\" and \"FDC Compass Merchant Descriptors\" in the [Merchant Descriptors Using the SCMP API] (https://apps.cybersource.com/library/documentation/dev_guides/Merchant_Descriptors_SCMP_API/html/)  #### CyberSource through VisaNet When you do not include this field in a request for a Crediario installment payment, CyberSource sends a value of 0 to the processor.  For Crediario installment payments, the value for this field corresponds to the following data in the TC 33 capture file*: - Record: CP01 TCR9 - Position: 38-40 - Field: Installment Payment Number  * The TC 33 Capture file contains information about the purchases and refunds that a merchant submits to CyberSource. CyberSource through VisaNet creates the TC 33 Capture file at the end of the day and sends it to the merchant's acquirer, who uses this information to facilitate end-of-day clearing processing with payment card companies. 

        :param sequence: The sequence of this Ptsv2billingagreementsInstallmentInformation.
        :type: int
        """

        self._sequence = sequence

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
        if not isinstance(other, Ptsv2billingagreementsInstallmentInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
