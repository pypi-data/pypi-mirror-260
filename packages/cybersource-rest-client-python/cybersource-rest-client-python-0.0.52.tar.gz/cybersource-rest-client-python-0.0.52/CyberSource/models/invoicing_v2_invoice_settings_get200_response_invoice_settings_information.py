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


class InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation(object):
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
        'merchant_logo': 'str',
        'merchant_display_name': 'str',
        'custom_email_message': 'str',
        'enable_reminders': 'bool',
        'header_style': 'InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformationHeaderStyle',
        'delivery_language': 'str',
        'default_currency_code': 'str',
        'payer_authentication3_ds_version': 'bool',
        'show_vat_number': 'bool',
        'vat_registration_number': 'str'
    }

    attribute_map = {
        'merchant_logo': 'merchantLogo',
        'merchant_display_name': 'merchantDisplayName',
        'custom_email_message': 'customEmailMessage',
        'enable_reminders': 'enableReminders',
        'header_style': 'headerStyle',
        'delivery_language': 'deliveryLanguage',
        'default_currency_code': 'defaultCurrencyCode',
        'payer_authentication3_ds_version': 'payerAuthentication3DSVersion',
        'show_vat_number': 'showVatNumber',
        'vat_registration_number': 'vatRegistrationNumber'
    }

    def __init__(self, merchant_logo=None, merchant_display_name=None, custom_email_message=None, enable_reminders=None, header_style=None, delivery_language=None, default_currency_code=None, payer_authentication3_ds_version=False, show_vat_number=False, vat_registration_number=None):
        """
        InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation - a model defined in Swagger
        """

        self._merchant_logo = None
        self._merchant_display_name = None
        self._custom_email_message = None
        self._enable_reminders = None
        self._header_style = None
        self._delivery_language = None
        self._default_currency_code = None
        self._payer_authentication3_ds_version = None
        self._show_vat_number = None
        self._vat_registration_number = None

        if merchant_logo is not None:
          self.merchant_logo = merchant_logo
        if merchant_display_name is not None:
          self.merchant_display_name = merchant_display_name
        if custom_email_message is not None:
          self.custom_email_message = custom_email_message
        if enable_reminders is not None:
          self.enable_reminders = enable_reminders
        if header_style is not None:
          self.header_style = header_style
        if delivery_language is not None:
          self.delivery_language = delivery_language
        if default_currency_code is not None:
          self.default_currency_code = default_currency_code
        if payer_authentication3_ds_version is not None:
          self.payer_authentication3_ds_version = payer_authentication3_ds_version
        if show_vat_number is not None:
          self.show_vat_number = show_vat_number
        if vat_registration_number is not None:
          self.vat_registration_number = vat_registration_number

    @property
    def merchant_logo(self):
        """
        Gets the merchant_logo of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The image file, which must be encoded in Base64 format. Supported file formats are `png`, `jpg`, and `gif`. The image file size restriction is 1 MB.

        :return: The merchant_logo of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._merchant_logo

    @merchant_logo.setter
    def merchant_logo(self, merchant_logo):
        """
        Sets the merchant_logo of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The image file, which must be encoded in Base64 format. Supported file formats are `png`, `jpg`, and `gif`. The image file size restriction is 1 MB.

        :param merchant_logo: The merchant_logo of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._merchant_logo = merchant_logo

    @property
    def merchant_display_name(self):
        """
        Gets the merchant_display_name of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The merchant's display name shown on the invoice.

        :return: The merchant_display_name of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._merchant_display_name

    @merchant_display_name.setter
    def merchant_display_name(self, merchant_display_name):
        """
        Sets the merchant_display_name of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The merchant's display name shown on the invoice.

        :param merchant_display_name: The merchant_display_name of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._merchant_display_name = merchant_display_name

    @property
    def custom_email_message(self):
        """
        Gets the custom_email_message of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The content of the email message that we send to your customers.

        :return: The custom_email_message of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._custom_email_message

    @custom_email_message.setter
    def custom_email_message(self, custom_email_message):
        """
        Sets the custom_email_message of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The content of the email message that we send to your customers.

        :param custom_email_message: The custom_email_message of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._custom_email_message = custom_email_message

    @property
    def enable_reminders(self):
        """
        Gets the enable_reminders of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Whether you would like us to send an auto-generated reminder email to your invoice recipients. Currently, this reminder email is sent five days before the invoice is due and one day after it is past due.

        :return: The enable_reminders of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: bool
        """
        return self._enable_reminders

    @enable_reminders.setter
    def enable_reminders(self, enable_reminders):
        """
        Sets the enable_reminders of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Whether you would like us to send an auto-generated reminder email to your invoice recipients. Currently, this reminder email is sent five days before the invoice is due and one day after it is past due.

        :param enable_reminders: The enable_reminders of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: bool
        """

        self._enable_reminders = enable_reminders

    @property
    def header_style(self):
        """
        Gets the header_style of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.

        :return: The header_style of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformationHeaderStyle
        """
        return self._header_style

    @header_style.setter
    def header_style(self, header_style):
        """
        Sets the header_style of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.

        :param header_style: The header_style of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformationHeaderStyle
        """

        self._header_style = header_style

    @property
    def delivery_language(self):
        """
        Gets the delivery_language of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The language of the email that we send to your customers. Possible values are `zh-CN`, `zh-TW`, `en-US`, `fr-FR`, `de-DE`, `ja-JP`, `pt-BR`, `ru-RU` and `es-419`.

        :return: The delivery_language of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._delivery_language

    @delivery_language.setter
    def delivery_language(self, delivery_language):
        """
        Sets the delivery_language of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The language of the email that we send to your customers. Possible values are `zh-CN`, `zh-TW`, `en-US`, `fr-FR`, `de-DE`, `ja-JP`, `pt-BR`, `ru-RU` and `es-419`.

        :param delivery_language: The delivery_language of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._delivery_language = delivery_language

    @property
    def default_currency_code(self):
        """
        Gets the default_currency_code of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Currency used for the order. Use the three-character [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  #### Used by **Authorization** Required field.  **Authorization Reversal** For an authorization reversal (`reversalInformation`) or a capture (`processingOptions.capture` is set to `true`), you must use the same currency that you used in your payment authorization request.  #### PIN Debit Currency for the amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf). Returned by PIN debit purchase.  For PIN debit reversal requests, you must use the same currency that was used for the PIN debit purchase or PIN debit credit that you are reversing. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf).  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit.  #### DCC for First Data Your local currency. For details, see the `currency` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### Tax Calculation Required for international tax and value added tax only. Optional for U.S. and Canadian taxes. Your local currency. 

        :return: The default_currency_code of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._default_currency_code

    @default_currency_code.setter
    def default_currency_code(self, default_currency_code):
        """
        Sets the default_currency_code of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Currency used for the order. Use the three-character [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  #### Used by **Authorization** Required field.  **Authorization Reversal** For an authorization reversal (`reversalInformation`) or a capture (`processingOptions.capture` is set to `true`), you must use the same currency that you used in your payment authorization request.  #### PIN Debit Currency for the amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf). Returned by PIN debit purchase.  For PIN debit reversal requests, you must use the same currency that was used for the PIN debit purchase or PIN debit credit that you are reversing. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf).  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit.  #### DCC for First Data Your local currency. For details, see the `currency` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### Tax Calculation Required for international tax and value added tax only. Optional for U.S. and Canadian taxes. Your local currency. 

        :param default_currency_code: The default_currency_code of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._default_currency_code = default_currency_code

    @property
    def payer_authentication3_ds_version(self):
        """
        Gets the payer_authentication3_ds_version of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The 3D Secure payer authentication status for a merchant's invoice payments.

        :return: The payer_authentication3_ds_version of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: bool
        """
        return self._payer_authentication3_ds_version

    @payer_authentication3_ds_version.setter
    def payer_authentication3_ds_version(self, payer_authentication3_ds_version):
        """
        Sets the payer_authentication3_ds_version of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        The 3D Secure payer authentication status for a merchant's invoice payments.

        :param payer_authentication3_ds_version: The payer_authentication3_ds_version of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: bool
        """

        self._payer_authentication3_ds_version = payer_authentication3_ds_version

    @property
    def show_vat_number(self):
        """
        Gets the show_vat_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Display VAT number on Invoice.

        :return: The show_vat_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: bool
        """
        return self._show_vat_number

    @show_vat_number.setter
    def show_vat_number(self, show_vat_number):
        """
        Sets the show_vat_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Display VAT number on Invoice.

        :param show_vat_number: The show_vat_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: bool
        """

        self._show_vat_number = show_vat_number

    @property
    def vat_registration_number(self):
        """
        Gets the vat_registration_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Your government-assigned tax identification number.  #### Tax Calculation Required field for value added tax only. Not applicable to U.S. and Canadian taxes.       

        :return: The vat_registration_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :rtype: str
        """
        return self._vat_registration_number

    @vat_registration_number.setter
    def vat_registration_number(self, vat_registration_number):
        """
        Sets the vat_registration_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        Your government-assigned tax identification number.  #### Tax Calculation Required field for value added tax only. Not applicable to U.S. and Canadian taxes.       

        :param vat_registration_number: The vat_registration_number of this InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation.
        :type: str
        """

        self._vat_registration_number = vat_registration_number

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
        if not isinstance(other, InvoicingV2InvoiceSettingsGet200ResponseInvoiceSettingsInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
