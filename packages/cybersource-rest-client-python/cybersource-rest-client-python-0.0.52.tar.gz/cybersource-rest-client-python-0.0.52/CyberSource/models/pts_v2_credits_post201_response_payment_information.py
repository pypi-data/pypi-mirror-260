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


class PtsV2CreditsPost201ResponsePaymentInformation(object):
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
        'bank': 'PtsV2PaymentsPost201ResponsePaymentInformationBank',
        'customer': 'Ptsv2paymentsPaymentInformationCustomer',
        'payment_instrument': 'Ptsv2paymentsPaymentInformationPaymentInstrument',
        'instrument_identifier': 'PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier',
        'shipping_address': 'Ptsv2paymentsPaymentInformationShippingAddress'
    }

    attribute_map = {
        'bank': 'bank',
        'customer': 'customer',
        'payment_instrument': 'paymentInstrument',
        'instrument_identifier': 'instrumentIdentifier',
        'shipping_address': 'shippingAddress'
    }

    def __init__(self, bank=None, customer=None, payment_instrument=None, instrument_identifier=None, shipping_address=None):
        """
        PtsV2CreditsPost201ResponsePaymentInformation - a model defined in Swagger
        """

        self._bank = None
        self._customer = None
        self._payment_instrument = None
        self._instrument_identifier = None
        self._shipping_address = None

        if bank is not None:
          self.bank = bank
        if customer is not None:
          self.customer = customer
        if payment_instrument is not None:
          self.payment_instrument = payment_instrument
        if instrument_identifier is not None:
          self.instrument_identifier = instrument_identifier
        if shipping_address is not None:
          self.shipping_address = shipping_address

    @property
    def bank(self):
        """
        Gets the bank of this PtsV2CreditsPost201ResponsePaymentInformation.

        :return: The bank of this PtsV2CreditsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationBank
        """
        return self._bank

    @bank.setter
    def bank(self, bank):
        """
        Sets the bank of this PtsV2CreditsPost201ResponsePaymentInformation.

        :param bank: The bank of this PtsV2CreditsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationBank
        """

        self._bank = bank

    @property
    def customer(self):
        """
        Gets the customer of this PtsV2CreditsPost201ResponsePaymentInformation.

        :return: The customer of this PtsV2CreditsPost201ResponsePaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationCustomer
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """
        Sets the customer of this PtsV2CreditsPost201ResponsePaymentInformation.

        :param customer: The customer of this PtsV2CreditsPost201ResponsePaymentInformation.
        :type: Ptsv2paymentsPaymentInformationCustomer
        """

        self._customer = customer

    @property
    def payment_instrument(self):
        """
        Gets the payment_instrument of this PtsV2CreditsPost201ResponsePaymentInformation.

        :return: The payment_instrument of this PtsV2CreditsPost201ResponsePaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationPaymentInstrument
        """
        return self._payment_instrument

    @payment_instrument.setter
    def payment_instrument(self, payment_instrument):
        """
        Sets the payment_instrument of this PtsV2CreditsPost201ResponsePaymentInformation.

        :param payment_instrument: The payment_instrument of this PtsV2CreditsPost201ResponsePaymentInformation.
        :type: Ptsv2paymentsPaymentInformationPaymentInstrument
        """

        self._payment_instrument = payment_instrument

    @property
    def instrument_identifier(self):
        """
        Gets the instrument_identifier of this PtsV2CreditsPost201ResponsePaymentInformation.

        :return: The instrument_identifier of this PtsV2CreditsPost201ResponsePaymentInformation.
        :rtype: PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier
        """
        return self._instrument_identifier

    @instrument_identifier.setter
    def instrument_identifier(self, instrument_identifier):
        """
        Sets the instrument_identifier of this PtsV2CreditsPost201ResponsePaymentInformation.

        :param instrument_identifier: The instrument_identifier of this PtsV2CreditsPost201ResponsePaymentInformation.
        :type: PtsV2PaymentsPost201ResponsePaymentInformationInstrumentIdentifier
        """

        self._instrument_identifier = instrument_identifier

    @property
    def shipping_address(self):
        """
        Gets the shipping_address of this PtsV2CreditsPost201ResponsePaymentInformation.

        :return: The shipping_address of this PtsV2CreditsPost201ResponsePaymentInformation.
        :rtype: Ptsv2paymentsPaymentInformationShippingAddress
        """
        return self._shipping_address

    @shipping_address.setter
    def shipping_address(self, shipping_address):
        """
        Sets the shipping_address of this PtsV2CreditsPost201ResponsePaymentInformation.

        :param shipping_address: The shipping_address of this PtsV2CreditsPost201ResponsePaymentInformation.
        :type: Ptsv2paymentsPaymentInformationShippingAddress
        """

        self._shipping_address = shipping_address

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
        if not isinstance(other, PtsV2CreditsPost201ResponsePaymentInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
