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


class PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds(object):
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
        'acquirer_organization_id': 'str',
        'acquiring_bin': 'int',
        'allow_crypto_currency_purchase': 'bool',
        'card_acceptor_id': 'str',
        'originator_mvv': 'str',
        'originator_name_abbreviation': 'str',
        'card_terminal_id': 'str'
    }

    attribute_map = {
        'acquirer_organization_id': 'acquirerOrganizationId',
        'acquiring_bin': 'acquiringBIN',
        'allow_crypto_currency_purchase': 'allowCryptoCurrencyPurchase',
        'card_acceptor_id': 'cardAcceptorId',
        'originator_mvv': 'originatorMvv',
        'originator_name_abbreviation': 'originatorNameAbbreviation',
        'card_terminal_id': 'cardTerminalId'
    }

    def __init__(self, acquirer_organization_id=None, acquiring_bin=None, allow_crypto_currency_purchase=None, card_acceptor_id=None, originator_mvv=None, originator_name_abbreviation=None, card_terminal_id=None):
        """
        PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds - a model defined in Swagger
        """

        self._acquirer_organization_id = None
        self._acquiring_bin = None
        self._allow_crypto_currency_purchase = None
        self._card_acceptor_id = None
        self._originator_mvv = None
        self._originator_name_abbreviation = None
        self._card_terminal_id = None

        if acquirer_organization_id is not None:
          self.acquirer_organization_id = acquirer_organization_id
        self.acquiring_bin = acquiring_bin
        if allow_crypto_currency_purchase is not None:
          self.allow_crypto_currency_purchase = allow_crypto_currency_purchase
        self.card_acceptor_id = card_acceptor_id
        if originator_mvv is not None:
          self.originator_mvv = originator_mvv
        if originator_name_abbreviation is not None:
          self.originator_name_abbreviation = originator_name_abbreviation
        self.card_terminal_id = card_terminal_id

    @property
    def acquirer_organization_id(self):
        """
        Gets the acquirer_organization_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        Valid organization in OMS with an organizationInformation.type as \"acquirer\".

        :return: The acquirer_organization_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: str
        """
        return self._acquirer_organization_id

    @acquirer_organization_id.setter
    def acquirer_organization_id(self, acquirer_organization_id):
        """
        Sets the acquirer_organization_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        Valid organization in OMS with an organizationInformation.type as \"acquirer\".

        :param acquirer_organization_id: The acquirer_organization_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: str
        """

        self._acquirer_organization_id = acquirer_organization_id

    @property
    def acquiring_bin(self):
        """
        Gets the acquiring_bin of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This code identifies the financial institution acting as the acquirer of this transaction. The acquirer is the client or system user that signed the originator or installed the unattended cardholder- activated environment. When a processing center operates for multiple acquirers, this code is for the individual client or system user, not a code for the center.

        :return: The acquiring_bin of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: int
        """
        return self._acquiring_bin

    @acquiring_bin.setter
    def acquiring_bin(self, acquiring_bin):
        """
        Sets the acquiring_bin of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This code identifies the financial institution acting as the acquirer of this transaction. The acquirer is the client or system user that signed the originator or installed the unattended cardholder- activated environment. When a processing center operates for multiple acquirers, this code is for the individual client or system user, not a code for the center.

        :param acquiring_bin: The acquiring_bin of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: int
        """
        if acquiring_bin is None:
            raise ValueError("Invalid value for `acquiring_bin`, must not be `None`")

        self._acquiring_bin = acquiring_bin

    @property
    def allow_crypto_currency_purchase(self):
        """
        Gets the allow_crypto_currency_purchase of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This configuration allows a transaction to be flagged for cryptocurrency funds transfer.

        :return: The allow_crypto_currency_purchase of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: bool
        """
        return self._allow_crypto_currency_purchase

    @allow_crypto_currency_purchase.setter
    def allow_crypto_currency_purchase(self, allow_crypto_currency_purchase):
        """
        Sets the allow_crypto_currency_purchase of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This configuration allows a transaction to be flagged for cryptocurrency funds transfer.

        :param allow_crypto_currency_purchase: The allow_crypto_currency_purchase of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: bool
        """

        self._allow_crypto_currency_purchase = allow_crypto_currency_purchase

    @property
    def card_acceptor_id(self):
        """
        Gets the card_acceptor_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        A unique identifier number for the originator of transfers that is unique to the processor or acquirer.

        :return: The card_acceptor_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: str
        """
        return self._card_acceptor_id

    @card_acceptor_id.setter
    def card_acceptor_id(self, card_acceptor_id):
        """
        Sets the card_acceptor_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        A unique identifier number for the originator of transfers that is unique to the processor or acquirer.

        :param card_acceptor_id: The card_acceptor_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: str
        """
        if card_acceptor_id is None:
            raise ValueError("Invalid value for `card_acceptor_id`, must not be `None`")

        self._card_acceptor_id = card_acceptor_id

    @property
    def originator_mvv(self):
        """
        Gets the originator_mvv of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        Merchant Verification Value (MVV) is used to identify originators that participate in a variety of programs. The MVV is unique to the merchant.

        :return: The originator_mvv of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: str
        """
        return self._originator_mvv

    @originator_mvv.setter
    def originator_mvv(self, originator_mvv):
        """
        Sets the originator_mvv of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        Merchant Verification Value (MVV) is used to identify originators that participate in a variety of programs. The MVV is unique to the merchant.

        :param originator_mvv: The originator_mvv of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: str
        """

        self._originator_mvv = originator_mvv

    @property
    def originator_name_abbreviation(self):
        """
        Gets the originator_name_abbreviation of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        A 4 character max name abbreviation for the originator.

        :return: The originator_name_abbreviation of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: str
        """
        return self._originator_name_abbreviation

    @originator_name_abbreviation.setter
    def originator_name_abbreviation(self, originator_name_abbreviation):
        """
        Sets the originator_name_abbreviation of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        A 4 character max name abbreviation for the originator.

        :param originator_name_abbreviation: The originator_name_abbreviation of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: str
        """

        self._originator_name_abbreviation = originator_name_abbreviation

    @property
    def card_terminal_id(self):
        """
        Gets the card_terminal_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This field contains a code that identifies a terminal at the card acceptor location. This field is used in all messages related to a transaction. If sending transactions from a card not present environment, use the same value for all transactions.

        :return: The card_terminal_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :rtype: str
        """
        return self._card_terminal_id

    @card_terminal_id.setter
    def card_terminal_id(self, card_terminal_id):
        """
        Sets the card_terminal_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        This field contains a code that identifies a terminal at the card acceptor location. This field is used in all messages related to a transaction. If sending transactions from a card not present environment, use the same value for all transactions.

        :param card_terminal_id: The card_terminal_id of this PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds.
        :type: str
        """
        if card_terminal_id is None:
            raise ValueError("Invalid value for `card_terminal_id`, must not be `None`")

        self._card_terminal_id = card_terminal_id

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
        if not isinstance(other, PaymentsProductsPayoutsConfigurationInformationConfigurationsPullfunds):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
