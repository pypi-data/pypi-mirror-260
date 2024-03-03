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


class Ptsv2paymentsidcapturesOrderInformationAmountDetails(object):
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
        'total_amount': 'str',
        'currency': 'str',
        'discount_amount': 'str',
        'duty_amount': 'str',
        'gratuity_amount': 'str',
        'tax_amount': 'str',
        'national_tax_included': 'str',
        'tax_applied_after_discount': 'str',
        'tax_applied_level': 'str',
        'tax_type_code': 'str',
        'freight_amount': 'str',
        'foreign_amount': 'str',
        'foreign_currency': 'str',
        'exchange_rate': 'str',
        'exchange_rate_time_stamp': 'str',
        'amex_additional_amounts': 'list[Ptsv2paymentsOrderInformationAmountDetailsAmexAdditionalAmounts]',
        'tax_details': 'list[Ptsv2paymentsOrderInformationAmountDetailsTaxDetails]',
        'service_fee_amount': 'str',
        'original_currency': 'str',
        'cashback_amount': 'str'
    }

    attribute_map = {
        'total_amount': 'totalAmount',
        'currency': 'currency',
        'discount_amount': 'discountAmount',
        'duty_amount': 'dutyAmount',
        'gratuity_amount': 'gratuityAmount',
        'tax_amount': 'taxAmount',
        'national_tax_included': 'nationalTaxIncluded',
        'tax_applied_after_discount': 'taxAppliedAfterDiscount',
        'tax_applied_level': 'taxAppliedLevel',
        'tax_type_code': 'taxTypeCode',
        'freight_amount': 'freightAmount',
        'foreign_amount': 'foreignAmount',
        'foreign_currency': 'foreignCurrency',
        'exchange_rate': 'exchangeRate',
        'exchange_rate_time_stamp': 'exchangeRateTimeStamp',
        'amex_additional_amounts': 'amexAdditionalAmounts',
        'tax_details': 'taxDetails',
        'service_fee_amount': 'serviceFeeAmount',
        'original_currency': 'originalCurrency',
        'cashback_amount': 'cashbackAmount'
    }

    def __init__(self, total_amount=None, currency=None, discount_amount=None, duty_amount=None, gratuity_amount=None, tax_amount=None, national_tax_included=None, tax_applied_after_discount=None, tax_applied_level=None, tax_type_code=None, freight_amount=None, foreign_amount=None, foreign_currency=None, exchange_rate=None, exchange_rate_time_stamp=None, amex_additional_amounts=None, tax_details=None, service_fee_amount=None, original_currency=None, cashback_amount=None):
        """
        Ptsv2paymentsidcapturesOrderInformationAmountDetails - a model defined in Swagger
        """

        self._total_amount = None
        self._currency = None
        self._discount_amount = None
        self._duty_amount = None
        self._gratuity_amount = None
        self._tax_amount = None
        self._national_tax_included = None
        self._tax_applied_after_discount = None
        self._tax_applied_level = None
        self._tax_type_code = None
        self._freight_amount = None
        self._foreign_amount = None
        self._foreign_currency = None
        self._exchange_rate = None
        self._exchange_rate_time_stamp = None
        self._amex_additional_amounts = None
        self._tax_details = None
        self._service_fee_amount = None
        self._original_currency = None
        self._cashback_amount = None

        if total_amount is not None:
          self.total_amount = total_amount
        if currency is not None:
          self.currency = currency
        if discount_amount is not None:
          self.discount_amount = discount_amount
        if duty_amount is not None:
          self.duty_amount = duty_amount
        if gratuity_amount is not None:
          self.gratuity_amount = gratuity_amount
        if tax_amount is not None:
          self.tax_amount = tax_amount
        if national_tax_included is not None:
          self.national_tax_included = national_tax_included
        if tax_applied_after_discount is not None:
          self.tax_applied_after_discount = tax_applied_after_discount
        if tax_applied_level is not None:
          self.tax_applied_level = tax_applied_level
        if tax_type_code is not None:
          self.tax_type_code = tax_type_code
        if freight_amount is not None:
          self.freight_amount = freight_amount
        if foreign_amount is not None:
          self.foreign_amount = foreign_amount
        if foreign_currency is not None:
          self.foreign_currency = foreign_currency
        if exchange_rate is not None:
          self.exchange_rate = exchange_rate
        if exchange_rate_time_stamp is not None:
          self.exchange_rate_time_stamp = exchange_rate_time_stamp
        if amex_additional_amounts is not None:
          self.amex_additional_amounts = amex_additional_amounts
        if tax_details is not None:
          self.tax_details = tax_details
        if service_fee_amount is not None:
          self.service_fee_amount = service_fee_amount
        if original_currency is not None:
          self.original_currency = original_currency
        if cashback_amount is not None:
          self.cashback_amount = cashback_amount

    @property
    def total_amount(self):
        """
        Gets the total_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Grand total for the order. This value cannot be negative. You can include a decimal point (.), but no other special characters. CyberSource truncates the amount to the correct number of decimal places.  **Note** For CTV, FDCCompass, Paymentech processors, the maximum length for this field is 12.  **Important** Some processors have specific requirements and limitations, such as maximum amounts and maximum field lengths. For details, see: - \"Authorization Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/). - \"Capture Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/). - \"Credit Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/).  If your processor supports zero amount authorizations, you can set this field to 0 for the authorization to check if the card is lost or stolen. For details, see \"Zero Amount Authorizations,\" \"Credit Information for Specific Processors\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### Card Present Required to include either this field or `orderInformation.lineItems[].unitPrice` for the order.  #### Invoicing Required for creating a new invoice.  #### PIN Debit Amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount.  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit; however, for all other processors, these fields are required.  #### DCC with a Third-Party Provider Set this field to the converted amount that was returned by the DCC provider. You must include either this field or the 1st line item in the order and the specific line-order amount in your request. For details, see `grand_total_amount` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### FDMS South If you accept IDR or CLP currencies, see the entry for FDMS South in \"Authorization Information for Specific Processors\" of the [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### DCC for First Data Not used. 

        :return: The total_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._total_amount

    @total_amount.setter
    def total_amount(self, total_amount):
        """
        Sets the total_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Grand total for the order. This value cannot be negative. You can include a decimal point (.), but no other special characters. CyberSource truncates the amount to the correct number of decimal places.  **Note** For CTV, FDCCompass, Paymentech processors, the maximum length for this field is 12.  **Important** Some processors have specific requirements and limitations, such as maximum amounts and maximum field lengths. For details, see: - \"Authorization Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/). - \"Capture Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/). - \"Credit Information for Specific Processors\" in the [Credit Card Services Using the SCMP API Guide](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/).  If your processor supports zero amount authorizations, you can set this field to 0 for the authorization to check if the card is lost or stolen. For details, see \"Zero Amount Authorizations,\" \"Credit Information for Specific Processors\" in [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### Card Present Required to include either this field or `orderInformation.lineItems[].unitPrice` for the order.  #### Invoicing Required for creating a new invoice.  #### PIN Debit Amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount.  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit; however, for all other processors, these fields are required.  #### DCC with a Third-Party Provider Set this field to the converted amount that was returned by the DCC provider. You must include either this field or the 1st line item in the order and the specific line-order amount in your request. For details, see `grand_total_amount` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### FDMS South If you accept IDR or CLP currencies, see the entry for FDMS South in \"Authorization Information for Specific Processors\" of the [Credit Card Services Using the SCMP API.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/)  #### DCC for First Data Not used. 

        :param total_amount: The total_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._total_amount = total_amount

    @property
    def currency(self):
        """
        Gets the currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Currency used for the order. Use the three-character [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  #### Used by **Authorization** Required field.  **Authorization Reversal** For an authorization reversal (`reversalInformation`) or a capture (`processingOptions.capture` is set to `true`), you must use the same currency that you used in your payment authorization request.  #### PIN Debit Currency for the amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf). Returned by PIN debit purchase.  For PIN debit reversal requests, you must use the same currency that was used for the PIN debit purchase or PIN debit credit that you are reversing. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf).  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit.  #### DCC for First Data Your local currency. For details, see the `currency` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### Tax Calculation Required for international tax and value added tax only. Optional for U.S. and Canadian taxes. Your local currency. 

        :return: The currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Currency used for the order. Use the three-character [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf)  #### Used by **Authorization** Required field.  **Authorization Reversal** For an authorization reversal (`reversalInformation`) or a capture (`processingOptions.capture` is set to `true`), you must use the same currency that you used in your payment authorization request.  #### PIN Debit Currency for the amount you requested for the PIN debit purchase. This value is returned for partial authorizations. The issuing bank can approve a partial amount if the balance on the debit card is less than the requested transaction amount. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf). Returned by PIN debit purchase.  For PIN debit reversal requests, you must use the same currency that was used for the PIN debit purchase or PIN debit credit that you are reversing. For the possible values, see the [ISO Standard Currency Codes](https://developer.cybersource.com/library/documentation/sbc/quickref/currencies.pdf).  Required field for PIN Debit purchase and PIN Debit credit requests. Optional field for PIN Debit reversal requests.  #### GPX This field is optional for reversing an authorization or credit.  #### DCC for First Data Your local currency. For details, see the `currency` field description in [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf).  #### Tax Calculation Required for international tax and value added tax only. Optional for U.S. and Canadian taxes. Your local currency. 

        :param currency: The currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._currency = currency

    @property
    def discount_amount(self):
        """
        Gets the discount_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total discount amount applied to the order. 

        :return: The discount_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._discount_amount

    @discount_amount.setter
    def discount_amount(self, discount_amount):
        """
        Sets the discount_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total discount amount applied to the order. 

        :param discount_amount: The discount_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._discount_amount = discount_amount

    @property
    def duty_amount(self):
        """
        Gets the duty_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total charges for any import or export duties included in the order. 

        :return: The duty_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._duty_amount

    @duty_amount.setter
    def duty_amount(self, duty_amount):
        """
        Sets the duty_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total charges for any import or export duties included in the order. 

        :param duty_amount: The duty_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._duty_amount = duty_amount

    @property
    def gratuity_amount(self):
        """
        Gets the gratuity_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Gratuity or tip amount for restaurants. Allowed only when industryDatatype=restaurant. When your customer uses a debit card or prepaid card, and you receive a partial authorization, the payment networks recommend that you do not submit a capture amount that is higher than the authorized amount. When the capture amount exceeds the partial amount that was approved, the issuer has chargeback rights for the excess amount.  Used by **Capture** Optional field.  #### CyberSource through VisaNet Restaurant data is supported only on CyberSource through VisaNet when card is present. 

        :return: The gratuity_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._gratuity_amount

    @gratuity_amount.setter
    def gratuity_amount(self, gratuity_amount):
        """
        Sets the gratuity_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Gratuity or tip amount for restaurants. Allowed only when industryDatatype=restaurant. When your customer uses a debit card or prepaid card, and you receive a partial authorization, the payment networks recommend that you do not submit a capture amount that is higher than the authorized amount. When the capture amount exceeds the partial amount that was approved, the issuer has chargeback rights for the excess amount.  Used by **Capture** Optional field.  #### CyberSource through VisaNet Restaurant data is supported only on CyberSource through VisaNet when card is present. 

        :param gratuity_amount: The gratuity_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._gratuity_amount = gratuity_amount

    @property
    def tax_amount(self):
        """
        Gets the tax_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total tax amount for all the items in the order. 

        :return: The tax_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._tax_amount

    @tax_amount.setter
    def tax_amount(self, tax_amount):
        """
        Sets the tax_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total tax amount for all the items in the order. 

        :param tax_amount: The tax_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._tax_amount = tax_amount

    @property
    def national_tax_included(self):
        """
        Gets the national_tax_included of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates whether a national tax is included in the order total.  Possible values:   - **0**: national tax not included  - **1**: national tax included 

        :return: The national_tax_included of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._national_tax_included

    @national_tax_included.setter
    def national_tax_included(self, national_tax_included):
        """
        Sets the national_tax_included of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates whether a national tax is included in the order total.  Possible values:   - **0**: national tax not included  - **1**: national tax included 

        :param national_tax_included: The national_tax_included of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._national_tax_included = national_tax_included

    @property
    def tax_applied_after_discount(self):
        """
        Gets the tax_applied_after_discount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates how the merchant manages discounts.  Possible values:   - **0**: no invoice level discount included  - **1**: tax calculated on the postdiscount invoice total  - **2**: tax calculated on the prediscount invoice total 

        :return: The tax_applied_after_discount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._tax_applied_after_discount

    @tax_applied_after_discount.setter
    def tax_applied_after_discount(self, tax_applied_after_discount):
        """
        Sets the tax_applied_after_discount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates how the merchant manages discounts.  Possible values:   - **0**: no invoice level discount included  - **1**: tax calculated on the postdiscount invoice total  - **2**: tax calculated on the prediscount invoice total 

        :param tax_applied_after_discount: The tax_applied_after_discount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._tax_applied_after_discount = tax_applied_after_discount

    @property
    def tax_applied_level(self):
        """
        Gets the tax_applied_level of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates how you calculate tax.  Possible values:   - **0**: net prices with tax calculated at line item level  - **1**: net prices with tax calculated at invoice level  - **2**: gross prices with tax provided at line item level  - **3**: gross prices with tax provided at invoice level  - **4**: no tax applies on the invoice for the transaction 

        :return: The tax_applied_level of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._tax_applied_level

    @tax_applied_level.setter
    def tax_applied_level(self, tax_applied_level):
        """
        Sets the tax_applied_level of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Flag that indicates how you calculate tax.  Possible values:   - **0**: net prices with tax calculated at line item level  - **1**: net prices with tax calculated at invoice level  - **2**: gross prices with tax provided at line item level  - **3**: gross prices with tax provided at invoice level  - **4**: no tax applies on the invoice for the transaction 

        :param tax_applied_level: The tax_applied_level of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._tax_applied_level = tax_applied_level

    @property
    def tax_type_code(self):
        """
        Gets the tax_type_code of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        For tax amounts that can be categorized as one tax type.  This field contains the tax type code that corresponds to the entry in the _lineItems.taxAmount_ field.  Possible values:   - **056**: sales tax (U.S only)  - **TX~**: all taxes (Canada only)   Note ~ = space. 

        :return: The tax_type_code of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._tax_type_code

    @tax_type_code.setter
    def tax_type_code(self, tax_type_code):
        """
        Sets the tax_type_code of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        For tax amounts that can be categorized as one tax type.  This field contains the tax type code that corresponds to the entry in the _lineItems.taxAmount_ field.  Possible values:   - **056**: sales tax (U.S only)  - **TX~**: all taxes (Canada only)   Note ~ = space. 

        :param tax_type_code: The tax_type_code of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._tax_type_code = tax_type_code

    @property
    def freight_amount(self):
        """
        Gets the freight_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total freight or shipping and handling charges for the order. When you include this field in your request, you must also include the **totalAmount** field.  For processor-specific information, see the freight_amount field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :return: The freight_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._freight_amount

    @freight_amount.setter
    def freight_amount(self, freight_amount):
        """
        Sets the freight_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Total freight or shipping and handling charges for the order. When you include this field in your request, you must also include the **totalAmount** field.  For processor-specific information, see the freight_amount field in [Level II and Level III Processing Using the SCMP API.](http://apps.cybersource.com/library/documentation/dev_guides/Level_2_3_SCMP_API/html) 

        :param freight_amount: The freight_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._freight_amount = freight_amount

    @property
    def foreign_amount(self):
        """
        Gets the foreign_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Set this field to the converted amount that was returned by the DCC provider. For processor-specific information, see the `foreign_amount` field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :return: The foreign_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._foreign_amount

    @foreign_amount.setter
    def foreign_amount(self, foreign_amount):
        """
        Sets the foreign_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Set this field to the converted amount that was returned by the DCC provider. For processor-specific information, see the `foreign_amount` field description in the [Credit Card Services Using the SCMP API Guide.](https://apps.cybersource.com/library/documentation/dev_guides/CC_Svcs_SCMP_API/html/) 

        :param foreign_amount: The foreign_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._foreign_amount = foreign_amount

    @property
    def foreign_currency(self):
        """
        Gets the foreign_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Set this field to the converted amount that was returned by the DCC provider. 

        :return: The foreign_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._foreign_currency

    @foreign_currency.setter
    def foreign_currency(self, foreign_currency):
        """
        Sets the foreign_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Set this field to the converted amount that was returned by the DCC provider. 

        :param foreign_currency: The foreign_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._foreign_currency = foreign_currency

    @property
    def exchange_rate(self):
        """
        Gets the exchange_rate of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Exchange rate returned by the DCC service. Includes a decimal point and a maximum of 4 decimal places.  For details, see `exchange_rate` request-level field description in the [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf) 

        :return: The exchange_rate of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, exchange_rate):
        """
        Sets the exchange_rate of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Exchange rate returned by the DCC service. Includes a decimal point and a maximum of 4 decimal places.  For details, see `exchange_rate` request-level field description in the [Dynamic Currency Conversion For First Data Using the SCMP API](http://apps.cybersource.com/library/documentation/dev_guides/DCC_FirstData_SCMP/DCC_FirstData_SCMP_API.pdf) 

        :param exchange_rate: The exchange_rate of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._exchange_rate = exchange_rate

    @property
    def exchange_rate_time_stamp(self):
        """
        Gets the exchange_rate_time_stamp of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Time stamp for the exchange rate. This value is returned by the DCC service.  Format: `YYYYMMDD~HH:MM`  where ~ denotes a space. 

        :return: The exchange_rate_time_stamp of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._exchange_rate_time_stamp

    @exchange_rate_time_stamp.setter
    def exchange_rate_time_stamp(self, exchange_rate_time_stamp):
        """
        Sets the exchange_rate_time_stamp of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Time stamp for the exchange rate. This value is returned by the DCC service.  Format: `YYYYMMDD~HH:MM`  where ~ denotes a space. 

        :param exchange_rate_time_stamp: The exchange_rate_time_stamp of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._exchange_rate_time_stamp = exchange_rate_time_stamp

    @property
    def amex_additional_amounts(self):
        """
        Gets the amex_additional_amounts of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.

        :return: The amex_additional_amounts of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: list[Ptsv2paymentsOrderInformationAmountDetailsAmexAdditionalAmounts]
        """
        return self._amex_additional_amounts

    @amex_additional_amounts.setter
    def amex_additional_amounts(self, amex_additional_amounts):
        """
        Sets the amex_additional_amounts of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.

        :param amex_additional_amounts: The amex_additional_amounts of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: list[Ptsv2paymentsOrderInformationAmountDetailsAmexAdditionalAmounts]
        """

        self._amex_additional_amounts = amex_additional_amounts

    @property
    def tax_details(self):
        """
        Gets the tax_details of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.

        :return: The tax_details of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: list[Ptsv2paymentsOrderInformationAmountDetailsTaxDetails]
        """
        return self._tax_details

    @tax_details.setter
    def tax_details(self, tax_details):
        """
        Sets the tax_details of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.

        :param tax_details: The tax_details of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: list[Ptsv2paymentsOrderInformationAmountDetailsTaxDetails]
        """

        self._tax_details = tax_details

    @property
    def service_fee_amount(self):
        """
        Gets the service_fee_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Service fee. Required for service fee transactions. 

        :return: The service_fee_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._service_fee_amount

    @service_fee_amount.setter
    def service_fee_amount(self, service_fee_amount):
        """
        Sets the service_fee_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Service fee. Required for service fee transactions. 

        :param service_fee_amount: The service_fee_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._service_fee_amount = service_fee_amount

    @property
    def original_currency(self):
        """
        Gets the original_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Your local pricing currency code.  For the possible values, see the [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf) 

        :return: The original_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._original_currency

    @original_currency.setter
    def original_currency(self, original_currency):
        """
        Sets the original_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Your local pricing currency code.  For the possible values, see the [ISO Standard Currency Codes.](http://apps.cybersource.com/library/documentation/sbc/quickref/currencies.pdf) 

        :param original_currency: The original_currency of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._original_currency = original_currency

    @property
    def cashback_amount(self):
        """
        Gets the cashback_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Cashback amount in the acquirer's currency. If a cashback amount is included in the request, it must be included in the `orderInformation.amountDetails.totalAmount` value.  This field is supported only on CyberSource through VisaNet.  #### Used by **Authorization** Optional. **Authorization Reversal** Optional.  #### PIN debit Optional field for PIN debit purchase, PIN debit credit or PIN debit reversal. 

        :return: The cashback_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :rtype: str
        """
        return self._cashback_amount

    @cashback_amount.setter
    def cashback_amount(self, cashback_amount):
        """
        Sets the cashback_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        Cashback amount in the acquirer's currency. If a cashback amount is included in the request, it must be included in the `orderInformation.amountDetails.totalAmount` value.  This field is supported only on CyberSource through VisaNet.  #### Used by **Authorization** Optional. **Authorization Reversal** Optional.  #### PIN debit Optional field for PIN debit purchase, PIN debit credit or PIN debit reversal. 

        :param cashback_amount: The cashback_amount of this Ptsv2paymentsidcapturesOrderInformationAmountDetails.
        :type: str
        """

        self._cashback_amount = cashback_amount

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
        if not isinstance(other, Ptsv2paymentsidcapturesOrderInformationAmountDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
