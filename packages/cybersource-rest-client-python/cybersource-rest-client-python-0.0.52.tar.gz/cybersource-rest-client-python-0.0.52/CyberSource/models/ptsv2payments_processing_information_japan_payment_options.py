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


class Ptsv2paymentsProcessingInformationJapanPaymentOptions(object):
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
        'payment_method': 'str',
        'bonuses': 'str',
        'bonus_month': 'str',
        'second_bonus_month': 'str',
        'bonus_amount': 'str',
        'second_bonus_amount': 'str',
        'preapproval_type': 'str',
        'installments': 'str',
        'terminal_id': 'str',
        'first_billing_month': 'str',
        'business_name': 'str',
        'business_name_katakana': 'str',
        'jis2_track_data': 'str',
        'business_name_alpha_numeric': 'str'
    }

    attribute_map = {
        'payment_method': 'paymentMethod',
        'bonuses': 'bonuses',
        'bonus_month': 'bonusMonth',
        'second_bonus_month': 'secondBonusMonth',
        'bonus_amount': 'bonusAmount',
        'second_bonus_amount': 'secondBonusAmount',
        'preapproval_type': 'preapprovalType',
        'installments': 'installments',
        'terminal_id': 'terminalId',
        'first_billing_month': 'firstBillingMonth',
        'business_name': 'businessName',
        'business_name_katakana': 'businessNameKatakana',
        'jis2_track_data': 'jis2TrackData',
        'business_name_alpha_numeric': 'businessNameAlphaNumeric'
    }

    def __init__(self, payment_method=None, bonuses=None, bonus_month=None, second_bonus_month=None, bonus_amount=None, second_bonus_amount=None, preapproval_type=None, installments=None, terminal_id=None, first_billing_month=None, business_name=None, business_name_katakana=None, jis2_track_data=None, business_name_alpha_numeric=None):
        """
        Ptsv2paymentsProcessingInformationJapanPaymentOptions - a model defined in Swagger
        """

        self._payment_method = None
        self._bonuses = None
        self._bonus_month = None
        self._second_bonus_month = None
        self._bonus_amount = None
        self._second_bonus_amount = None
        self._preapproval_type = None
        self._installments = None
        self._terminal_id = None
        self._first_billing_month = None
        self._business_name = None
        self._business_name_katakana = None
        self._jis2_track_data = None
        self._business_name_alpha_numeric = None

        if payment_method is not None:
          self.payment_method = payment_method
        if bonuses is not None:
          self.bonuses = bonuses
        if bonus_month is not None:
          self.bonus_month = bonus_month
        if second_bonus_month is not None:
          self.second_bonus_month = second_bonus_month
        if bonus_amount is not None:
          self.bonus_amount = bonus_amount
        if second_bonus_amount is not None:
          self.second_bonus_amount = second_bonus_amount
        if preapproval_type is not None:
          self.preapproval_type = preapproval_type
        if installments is not None:
          self.installments = installments
        if terminal_id is not None:
          self.terminal_id = terminal_id
        if first_billing_month is not None:
          self.first_billing_month = first_billing_month
        if business_name is not None:
          self.business_name = business_name
        if business_name_katakana is not None:
          self.business_name_katakana = business_name_katakana
        if jis2_track_data is not None:
          self.jis2_track_data = jis2_track_data
        if business_name_alpha_numeric is not None:
          self.business_name_alpha_numeric = business_name_alpha_numeric

    @property
    def payment_method(self):
        """
        Gets the payment_method of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the payment method. Use Payment Method Code value that applies to the tranasction. - 10 (One-time payment) - 21, 22, 23, 24  (Bonus(one-time)payment) - 61 (Installment payment) - 31, 32, 33, 34  (Integrated (Bonus + Installment)payment) - 80 (Revolving payment) 

        :return: The payment_method of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        """
        Sets the payment_method of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the payment method. Use Payment Method Code value that applies to the tranasction. - 10 (One-time payment) - 21, 22, 23, 24  (Bonus(one-time)payment) - 61 (Installment payment) - 31, 32, 33, 34  (Integrated (Bonus + Installment)payment) - 80 (Revolving payment) 

        :param payment_method: The payment_method of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._payment_method = payment_method

    @property
    def bonuses(self):
        """
        Gets the bonuses of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the Number of Bonuses. Valid value from 1 to 6. 

        :return: The bonuses of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._bonuses

    @bonuses.setter
    def bonuses(self, bonuses):
        """
        Sets the bonuses of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the Number of Bonuses. Valid value from 1 to 6. 

        :param bonuses: The bonuses of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._bonuses = bonuses

    @property
    def bonus_month(self):
        """
        Gets the bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the first bonus month. Valid value from 1 to 12. 

        :return: The bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._bonus_month

    @bonus_month.setter
    def bonus_month(self, bonus_month):
        """
        Sets the bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the first bonus month. Valid value from 1 to 12. 

        :param bonus_month: The bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._bonus_month = bonus_month

    @property
    def second_bonus_month(self):
        """
        Gets the second_bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the second bonus month. Valid value from 1 to 12. 

        :return: The second_bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._second_bonus_month

    @second_bonus_month.setter
    def second_bonus_month(self, second_bonus_month):
        """
        Sets the second_bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value is a 2-digit code indicating the second bonus month. Valid value from 1 to 12. 

        :param second_bonus_month: The second_bonus_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._second_bonus_month = second_bonus_month

    @property
    def bonus_amount(self):
        """
        Gets the bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value contains the bonus amount of the first month. Maximum value without decimal 99999999. 

        :return: The bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._bonus_amount

    @bonus_amount.setter
    def bonus_amount(self, bonus_amount):
        """
        Sets the bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value contains the bonus amount of the first month. Maximum value without decimal 99999999. 

        :param bonus_amount: The bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._bonus_amount = bonus_amount

    @property
    def second_bonus_amount(self):
        """
        Gets the second_bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value contains the bonus amount of the second month. Maximum value without decimal 99999999. 

        :return: The second_bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._second_bonus_amount

    @second_bonus_amount.setter
    def second_bonus_amount(self, second_bonus_amount):
        """
        Sets the second_bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This value contains the bonus amount of the second month. Maximum value without decimal 99999999. 

        :param second_bonus_amount: The second_bonus_amount of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._second_bonus_amount = second_bonus_amount

    @property
    def preapproval_type(self):
        """
        Gets the preapproval_type of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This will contain the details of the kind of transaction that has been processe. Used only for Japan. Possible Values: - 0 = Normal (authorization with amount and clearing/settlement; data capture or paper draft) - 1 = Negative card authorization (authorization-only with 0 or 1 amount) - 2 = Reservation of authorization (authorization-only with amount) - 3 = Cancel transaction - 4 = Merchant-initiated reversal/refund transactions - 5 = Cancel reservation of authorization - 6 = Post authorization 

        :return: The preapproval_type of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._preapproval_type

    @preapproval_type.setter
    def preapproval_type(self, preapproval_type):
        """
        Sets the preapproval_type of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        This will contain the details of the kind of transaction that has been processe. Used only for Japan. Possible Values: - 0 = Normal (authorization with amount and clearing/settlement; data capture or paper draft) - 1 = Negative card authorization (authorization-only with 0 or 1 amount) - 2 = Reservation of authorization (authorization-only with amount) - 3 = Cancel transaction - 4 = Merchant-initiated reversal/refund transactions - 5 = Cancel reservation of authorization - 6 = Post authorization 

        :param preapproval_type: The preapproval_type of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._preapproval_type = preapproval_type

    @property
    def installments(self):
        """
        Gets the installments of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Number of Installments. 

        :return: The installments of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._installments

    @installments.setter
    def installments(self, installments):
        """
        Sets the installments of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Number of Installments. 

        :param installments: The installments of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._installments = installments

    @property
    def terminal_id(self):
        """
        Gets the terminal_id of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Unique Japan Credit Card Association (JCCA) terminal identifier.  The difference between this field and the `pointOfSaleInformation.terminalID` field is that you can define `pointOfSaleInformation.terminalID`, but `processingInformation.japanPaymentOptions.terminalId` is defined by the JCCA and is used only in Japan.  This field is supported only on CyberSource through VisaNet and JCN Gateway.  Optional field. 

        :return: The terminal_id of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._terminal_id

    @terminal_id.setter
    def terminal_id(self, terminal_id):
        """
        Sets the terminal_id of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Unique Japan Credit Card Association (JCCA) terminal identifier.  The difference between this field and the `pointOfSaleInformation.terminalID` field is that you can define `pointOfSaleInformation.terminalID`, but `processingInformation.japanPaymentOptions.terminalId` is defined by the JCCA and is used only in Japan.  This field is supported only on CyberSource through VisaNet and JCN Gateway.  Optional field. 

        :param terminal_id: The terminal_id of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._terminal_id = terminal_id

    @property
    def first_billing_month(self):
        """
        Gets the first_billing_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Billing month in MM format. 

        :return: The first_billing_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._first_billing_month

    @first_billing_month.setter
    def first_billing_month(self, first_billing_month):
        """
        Sets the first_billing_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Billing month in MM format. 

        :param first_billing_month: The first_billing_month of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._first_billing_month = first_billing_month

    @property
    def business_name(self):
        """
        Gets the business_name of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in Japanese characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :return: The business_name of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._business_name

    @business_name.setter
    def business_name(self, business_name):
        """
        Sets the business_name of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in Japanese characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :param business_name: The business_name of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._business_name = business_name

    @property
    def business_name_katakana(self):
        """
        Gets the business_name_katakana of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in Katakana characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :return: The business_name_katakana of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._business_name_katakana

    @business_name_katakana.setter
    def business_name_katakana(self, business_name_katakana):
        """
        Sets the business_name_katakana of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in Katakana characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :param business_name_katakana: The business_name_katakana of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._business_name_katakana = business_name_katakana

    @property
    def jis2_track_data(self):
        """
        Gets the jis2_track_data of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Japanese Industrial Standard Type 2 (JIS2) track data from the front of the card.  This field is supported only on CyberSource through VisaNet and JCN Gateway.  Optional field. 

        :return: The jis2_track_data of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._jis2_track_data

    @jis2_track_data.setter
    def jis2_track_data(self, jis2_track_data):
        """
        Sets the jis2_track_data of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Japanese Industrial Standard Type 2 (JIS2) track data from the front of the card.  This field is supported only on CyberSource through VisaNet and JCN Gateway.  Optional field. 

        :param jis2_track_data: The jis2_track_data of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._jis2_track_data = jis2_track_data

    @property
    def business_name_alpha_numeric(self):
        """
        Gets the business_name_alpha_numeric of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in alphanumeric characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :return: The business_name_alpha_numeric of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :rtype: str
        """
        return self._business_name_alpha_numeric

    @business_name_alpha_numeric.setter
    def business_name_alpha_numeric(self, business_name_alpha_numeric):
        """
        Sets the business_name_alpha_numeric of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        Business name in alphanumeric characters. This field is supported only on JCN Gateway and for the Sumitomo Mitsui Card Co. acquirer on CyberSource through VisaNet. 

        :param business_name_alpha_numeric: The business_name_alpha_numeric of this Ptsv2paymentsProcessingInformationJapanPaymentOptions.
        :type: str
        """

        self._business_name_alpha_numeric = business_name_alpha_numeric

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
        if not isinstance(other, Ptsv2paymentsProcessingInformationJapanPaymentOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
