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


class Ptsv1pushfundstransferRecipientInformationPaymentInformationCard(object):
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
        'type': 'str',
        'security_code': 'str',
        'number': 'str',
        'expiration_month': 'str',
        'expiration_year': 'str',
        'customer': 'Ptsv1pushfundstransferRecipientInformationPaymentInformationCardCustomer',
        'payment_instrument': 'Ptsv1pushfundstransferRecipientInformationPaymentInformationCardPaymentInstrument',
        'instrument_identifier': 'Ptsv1pushfundstransferRecipientInformationPaymentInformationCardInstrumentIdentifier'
    }

    attribute_map = {
        'type': 'type',
        'security_code': 'securityCode',
        'number': 'number',
        'expiration_month': 'expirationMonth',
        'expiration_year': 'expirationYear',
        'customer': 'customer',
        'payment_instrument': 'paymentInstrument',
        'instrument_identifier': 'instrumentIdentifier'
    }

    def __init__(self, type=None, security_code=None, number=None, expiration_month=None, expiration_year=None, customer=None, payment_instrument=None, instrument_identifier=None):
        """
        Ptsv1pushfundstransferRecipientInformationPaymentInformationCard - a model defined in Swagger
        """

        self._type = None
        self._security_code = None
        self._number = None
        self._expiration_month = None
        self._expiration_year = None
        self._customer = None
        self._payment_instrument = None
        self._instrument_identifier = None

        if type is not None:
          self.type = type
        if security_code is not None:
          self.security_code = security_code
        if number is not None:
          self.number = number
        if expiration_month is not None:
          self.expiration_month = expiration_month
        if expiration_year is not None:
          self.expiration_year = expiration_year
        if customer is not None:
          self.customer = customer
        if payment_instrument is not None:
          self.payment_instrument = payment_instrument
        if instrument_identifier is not None:
          self.instrument_identifier = instrument_identifier

    @property
    def type(self):
        """
        Gets the type of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Three-digit value that indicates the card type. Mandatory if not present in a token.  Possible values:  Visa Platform Connect - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard. - `033`: Visa Electron - `024`: Maestro  Mastercard Send: - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard.  FDC Compass: - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard.  Chase Paymentech: - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard. 

        :return: The type of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Three-digit value that indicates the card type. Mandatory if not present in a token.  Possible values:  Visa Platform Connect - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard. - `033`: Visa Electron - `024`: Maestro  Mastercard Send: - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard.  FDC Compass: - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard.  Chase Paymentech: - `001`: Visa - `002`: Mastercard, Eurocard, which is a European regional brand of Mastercard. 

        :param type: The type of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: str
        """

        self._type = type

    @property
    def security_code(self):
        """
        Gets the security_code of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        3-digit value that indicates the cardCvv2Value. Values can be 0-9. 

        :return: The security_code of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: str
        """
        return self._security_code

    @security_code.setter
    def security_code(self, security_code):
        """
        Sets the security_code of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        3-digit value that indicates the cardCvv2Value. Values can be 0-9. 

        :param security_code: The security_code of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: str
        """

        self._security_code = security_code

    @property
    def number(self):
        """
        Gets the number of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        The customer's payment card number, also known as the Primary Account Number (PAN).  Conditional: this field is required if not using tokens. 

        :return: The number of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Sets the number of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        The customer's payment card number, also known as the Primary Account Number (PAN).  Conditional: this field is required if not using tokens. 

        :param number: The number of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: str
        """

        self._number = number

    @property
    def expiration_month(self):
        """
        Gets the expiration_month of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Two-digit month in which the payment card expires.  Format: MM.  Valid values: 01 through 12. Leading 0 is required. 

        :return: The expiration_month of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: str
        """
        return self._expiration_month

    @expiration_month.setter
    def expiration_month(self, expiration_month):
        """
        Sets the expiration_month of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Two-digit month in which the payment card expires.  Format: MM.  Valid values: 01 through 12. Leading 0 is required. 

        :param expiration_month: The expiration_month of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: str
        """

        self._expiration_month = expiration_month

    @property
    def expiration_year(self):
        """
        Gets the expiration_year of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Four-digit year in which the payment card expires.  Format: YYYY. 

        :return: The expiration_year of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: str
        """
        return self._expiration_year

    @expiration_year.setter
    def expiration_year(self, expiration_year):
        """
        Sets the expiration_year of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        Four-digit year in which the payment card expires.  Format: YYYY. 

        :param expiration_year: The expiration_year of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: str
        """

        self._expiration_year = expiration_year

    @property
    def customer(self):
        """
        Gets the customer of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :return: The customer of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardCustomer
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """
        Sets the customer of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :param customer: The customer of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardCustomer
        """

        self._customer = customer

    @property
    def payment_instrument(self):
        """
        Gets the payment_instrument of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :return: The payment_instrument of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardPaymentInstrument
        """
        return self._payment_instrument

    @payment_instrument.setter
    def payment_instrument(self, payment_instrument):
        """
        Sets the payment_instrument of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :param payment_instrument: The payment_instrument of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardPaymentInstrument
        """

        self._payment_instrument = payment_instrument

    @property
    def instrument_identifier(self):
        """
        Gets the instrument_identifier of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :return: The instrument_identifier of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :rtype: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardInstrumentIdentifier
        """
        return self._instrument_identifier

    @instrument_identifier.setter
    def instrument_identifier(self, instrument_identifier):
        """
        Sets the instrument_identifier of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.

        :param instrument_identifier: The instrument_identifier of this Ptsv1pushfundstransferRecipientInformationPaymentInformationCard.
        :type: Ptsv1pushfundstransferRecipientInformationPaymentInformationCardInstrumentIdentifier
        """

        self._instrument_identifier = instrument_identifier

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
        if not isinstance(other, Ptsv1pushfundstransferRecipientInformationPaymentInformationCard):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
