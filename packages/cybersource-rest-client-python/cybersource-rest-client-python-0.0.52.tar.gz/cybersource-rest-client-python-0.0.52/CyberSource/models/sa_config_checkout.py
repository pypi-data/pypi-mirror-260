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


class SAConfigCheckout(object):
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
        'display_tax_amount': 'bool',
        'template_type': 'str',
        'return_to_merchant_site_url': 'str'
    }

    attribute_map = {
        'display_tax_amount': 'displayTaxAmount',
        'template_type': 'templateType',
        'return_to_merchant_site_url': 'returnToMerchantSiteUrl'
    }

    def __init__(self, display_tax_amount=None, template_type=None, return_to_merchant_site_url=None):
        """
        SAConfigCheckout - a model defined in Swagger
        """

        self._display_tax_amount = None
        self._template_type = None
        self._return_to_merchant_site_url = None

        if display_tax_amount is not None:
          self.display_tax_amount = display_tax_amount
        if template_type is not None:
          self.template_type = template_type
        if return_to_merchant_site_url is not None:
          self.return_to_merchant_site_url = return_to_merchant_site_url

    @property
    def display_tax_amount(self):
        """
        Gets the display_tax_amount of this SAConfigCheckout.
        Toggles whether or not the tax amount is displayed on the Hosted Checkout.

        :return: The display_tax_amount of this SAConfigCheckout.
        :rtype: bool
        """
        return self._display_tax_amount

    @display_tax_amount.setter
    def display_tax_amount(self, display_tax_amount):
        """
        Sets the display_tax_amount of this SAConfigCheckout.
        Toggles whether or not the tax amount is displayed on the Hosted Checkout.

        :param display_tax_amount: The display_tax_amount of this SAConfigCheckout.
        :type: bool
        """

        self._display_tax_amount = display_tax_amount

    @property
    def template_type(self):
        """
        Gets the template_type of this SAConfigCheckout.
        Specifies whether the Hosted Checkout is displayed as a single page form or multi page checkout.   Valid values:  `multi`  `single` 

        :return: The template_type of this SAConfigCheckout.
        :rtype: str
        """
        return self._template_type

    @template_type.setter
    def template_type(self, template_type):
        """
        Sets the template_type of this SAConfigCheckout.
        Specifies whether the Hosted Checkout is displayed as a single page form or multi page checkout.   Valid values:  `multi`  `single` 

        :param template_type: The template_type of this SAConfigCheckout.
        :type: str
        """

        self._template_type = template_type

    @property
    def return_to_merchant_site_url(self):
        """
        Gets the return_to_merchant_site_url of this SAConfigCheckout.
        URL of the website linked to from the Secure Acceptance receipt page. Only used if the profile does not have custom receipt pages configured.

        :return: The return_to_merchant_site_url of this SAConfigCheckout.
        :rtype: str
        """
        return self._return_to_merchant_site_url

    @return_to_merchant_site_url.setter
    def return_to_merchant_site_url(self, return_to_merchant_site_url):
        """
        Sets the return_to_merchant_site_url of this SAConfigCheckout.
        URL of the website linked to from the Secure Acceptance receipt page. Only used if the profile does not have custom receipt pages configured.

        :param return_to_merchant_site_url: The return_to_merchant_site_url of this SAConfigCheckout.
        :type: str
        """

        self._return_to_merchant_site_url = return_to_merchant_site_url

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
        if not isinstance(other, SAConfigCheckout):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
