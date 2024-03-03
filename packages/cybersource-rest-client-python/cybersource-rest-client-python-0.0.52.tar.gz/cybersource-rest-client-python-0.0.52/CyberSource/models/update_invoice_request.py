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


class UpdateInvoiceRequest(object):
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
        'customer_information': 'Invoicingv2invoicesCustomerInformation',
        'invoice_information': 'Invoicingv2invoicesidInvoiceInformation',
        'order_information': 'Invoicingv2invoicesOrderInformation'
    }

    attribute_map = {
        'customer_information': 'customerInformation',
        'invoice_information': 'invoiceInformation',
        'order_information': 'orderInformation'
    }

    def __init__(self, customer_information=None, invoice_information=None, order_information=None):
        """
        UpdateInvoiceRequest - a model defined in Swagger
        """

        self._customer_information = None
        self._invoice_information = None
        self._order_information = None

        if customer_information is not None:
          self.customer_information = customer_information
        if invoice_information is not None:
          self.invoice_information = invoice_information
        if order_information is not None:
          self.order_information = order_information

    @property
    def customer_information(self):
        """
        Gets the customer_information of this UpdateInvoiceRequest.

        :return: The customer_information of this UpdateInvoiceRequest.
        :rtype: Invoicingv2invoicesCustomerInformation
        """
        return self._customer_information

    @customer_information.setter
    def customer_information(self, customer_information):
        """
        Sets the customer_information of this UpdateInvoiceRequest.

        :param customer_information: The customer_information of this UpdateInvoiceRequest.
        :type: Invoicingv2invoicesCustomerInformation
        """

        self._customer_information = customer_information

    @property
    def invoice_information(self):
        """
        Gets the invoice_information of this UpdateInvoiceRequest.

        :return: The invoice_information of this UpdateInvoiceRequest.
        :rtype: Invoicingv2invoicesidInvoiceInformation
        """
        return self._invoice_information

    @invoice_information.setter
    def invoice_information(self, invoice_information):
        """
        Sets the invoice_information of this UpdateInvoiceRequest.

        :param invoice_information: The invoice_information of this UpdateInvoiceRequest.
        :type: Invoicingv2invoicesidInvoiceInformation
        """

        self._invoice_information = invoice_information

    @property
    def order_information(self):
        """
        Gets the order_information of this UpdateInvoiceRequest.

        :return: The order_information of this UpdateInvoiceRequest.
        :rtype: Invoicingv2invoicesOrderInformation
        """
        return self._order_information

    @order_information.setter
    def order_information(self, order_information):
        """
        Sets the order_information of this UpdateInvoiceRequest.

        :param order_information: The order_information of this UpdateInvoiceRequest.
        :type: Invoicingv2invoicesOrderInformation
        """

        self._order_information = order_information

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
        if not isinstance(other, UpdateInvoiceRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
