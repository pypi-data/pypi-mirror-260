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


class Ptsv2payoutsPaymentInformation(object):
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
        'card': 'Ptsv2payoutsPaymentInformationCard',
        'customer': 'Ptsv2paymentsPaymentInformationCustomer',
        'payment_instrument': 'Ptsv2paymentsPaymentInformationPaymentInstrument',
        'instrument_identifier': 'PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier',
        'tokenized_card': 'Ptsv2paymentsPaymentInformationTokenizedCard'
    }

    attribute_map = {
        'card': 'card',
        'customer': 'customer',
        'payment_instrument': 'paymentInstrument',
        'instrument_identifier': 'instrumentIdentifier',
        'tokenized_card': 'tokenizedCard'
    }

    def __init__(self, card=None, customer=None, payment_instrument=None, instrument_identifier=None, tokenized_card=None):
        """
        Ptsv2payoutsPaymentInformation - a model defined in Swagger
        """

        self._card = None
        self._customer = None
        self._payment_instrument = None
        self._instrument_identifier = None
        self._tokenized_card = None

        if card is not None:
          self.card = card
        if customer is not None:
          self.customer = customer
        if payment_instrument is not None:
          self.payment_instrument = payment_instrument
        if instrument_identifier is not None:
          self.instrument_identifier = instrument_identifier
        if tokenized_card is not None:
          self.tokenized_card = tokenized_card

    @property
    def card(self):
        """
        Gets the card of this Ptsv2payoutsPaymentInformation.

        :return: The card of this Ptsv2payoutsPaymentInformation.
        :rtype: Ptsv2payoutsPaymentInformationCard
        """
        return self._card

    @card.setter
    def card(self, card):
        """
        Sets the card of this Ptsv2payoutsPaymentInformation.

        :param card: The card of this Ptsv2payoutsPaymentInformation.
        :type: Ptsv2payoutsPaymentInformationCard
        """

        self._card = card

    @property
    def customer(self):
        """
        Gets the customer of this Ptsv2payoutsPaymentInformation.

        :return: The customer of this Ptsv2payoutsPaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationCustomer
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """
        Sets the customer of this Ptsv2payoutsPaymentInformation.

        :param customer: The customer of this Ptsv2payoutsPaymentInformation.
        :type: Ptsv2paymentsPaymentInformationCustomer
        """

        self._customer = customer

    @property
    def payment_instrument(self):
        """
        Gets the payment_instrument of this Ptsv2payoutsPaymentInformation.

        :return: The payment_instrument of this Ptsv2payoutsPaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationPaymentInstrument
        """
        return self._payment_instrument

    @payment_instrument.setter
    def payment_instrument(self, payment_instrument):
        """
        Sets the payment_instrument of this Ptsv2payoutsPaymentInformation.

        :param payment_instrument: The payment_instrument of this Ptsv2payoutsPaymentInformation.
        :type: Ptsv2paymentsPaymentInformationPaymentInstrument
        """

        self._payment_instrument = payment_instrument

    @property
    def instrument_identifier(self):
        """
        Gets the instrument_identifier of this Ptsv2payoutsPaymentInformation.

        :return: The instrument_identifier of this Ptsv2payoutsPaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier
        """
        return self._instrument_identifier

    @instrument_identifier.setter
    def instrument_identifier(self, instrument_identifier):
        """
        Sets the instrument_identifier of this Ptsv2payoutsPaymentInformation.

        :param instrument_identifier: The instrument_identifier of this Ptsv2payoutsPaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier
        """

        self._instrument_identifier = instrument_identifier

    @property
    def tokenized_card(self):
        """
        Gets the tokenized_card of this Ptsv2payoutsPaymentInformation.

        :return: The tokenized_card of this Ptsv2payoutsPaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationTokenizedCard
        """
        return self._tokenized_card

    @tokenized_card.setter
    def tokenized_card(self, tokenized_card):
        """
        Sets the tokenized_card of this Ptsv2payoutsPaymentInformation.

        :param tokenized_card: The tokenized_card of this Ptsv2payoutsPaymentInformation.
        :type: Ptsv2paymentsPaymentInformationTokenizedCard
        """

        self._tokenized_card = tokenized_card

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
        if not isinstance(other, Ptsv2payoutsPaymentInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
