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


class TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures(object):
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
        'balance_amount': 'str',
        'previous_balance_amount': 'str',
        'currency': 'str'
    }

    attribute_map = {
        'balance_amount': 'balanceAmount',
        'previous_balance_amount': 'previousBalanceAmount',
        'currency': 'currency'
    }

    def __init__(self, balance_amount=None, previous_balance_amount=None, currency=None):
        """
        TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures - a model defined in Swagger
        """

        self._balance_amount = None
        self._previous_balance_amount = None
        self._currency = None

        if balance_amount is not None:
          self.balance_amount = balance_amount
        if previous_balance_amount is not None:
          self.previous_balance_amount = previous_balance_amount
        if currency is not None:
          self.currency = currency

    @property
    def balance_amount(self):
        """
        Gets the balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Remaining balance on the account.  Returned by authorization service.  #### PIN debit Remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :return: The balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :rtype: str
        """
        return self._balance_amount

    @balance_amount.setter
    def balance_amount(self, balance_amount):
        """
        Sets the balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Remaining balance on the account.  Returned by authorization service.  #### PIN debit Remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :param balance_amount: The balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :type: str
        """

        self._balance_amount = balance_amount

    @property
    def previous_balance_amount(self):
        """
        Gets the previous_balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Remaining balance on the account.  Returned by authorization service.  #### PIN debit Remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :return: The previous_balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :rtype: str
        """
        return self._previous_balance_amount

    @previous_balance_amount.setter
    def previous_balance_amount(self, previous_balance_amount):
        """
        Sets the previous_balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Remaining balance on the account.  Returned by authorization service.  #### PIN debit Remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :param previous_balance_amount: The previous_balance_amount of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :type: str
        """

        self._previous_balance_amount = previous_balance_amount

    @property
    def currency(self):
        """
        Gets the currency of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Currency of the remaining balance on the account. For the possible values, see the [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  Returned by authorization service.  #### PIN debit Currency of the remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :return: The currency of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        Currency of the remaining balance on the account. For the possible values, see the [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  Returned by authorization service.  #### PIN debit Currency of the remaining balance on the prepaid card.  Returned by PIN debit purchase. 

        :param currency: The currency of this TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures.
        :type: str
        """

        self._currency = currency

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
        if not isinstance(other, TssV2TransactionsGet200ResponsePaymentInformationAccountFeatures):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
