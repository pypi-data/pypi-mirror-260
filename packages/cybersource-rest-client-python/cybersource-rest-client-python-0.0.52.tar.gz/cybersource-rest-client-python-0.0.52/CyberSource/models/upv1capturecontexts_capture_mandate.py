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


class Upv1capturecontextsCaptureMandate(object):
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
        'billing_type': 'str',
        'request_email': 'bool',
        'request_phone': 'bool',
        'request_shipping': 'bool',
        'ship_to_countries': 'list[str]',
        'show_accepted_network_icons': 'bool'
    }

    attribute_map = {
        'billing_type': 'billingType',
        'request_email': 'requestEmail',
        'request_phone': 'requestPhone',
        'request_shipping': 'requestShipping',
        'ship_to_countries': 'shipToCountries',
        'show_accepted_network_icons': 'showAcceptedNetworkIcons'
    }

    def __init__(self, billing_type=None, request_email=None, request_phone=None, request_shipping=None, ship_to_countries=None, show_accepted_network_icons=None):
        """
        Upv1capturecontextsCaptureMandate - a model defined in Swagger
        """

        self._billing_type = None
        self._request_email = None
        self._request_phone = None
        self._request_shipping = None
        self._ship_to_countries = None
        self._show_accepted_network_icons = None

        if billing_type is not None:
          self.billing_type = billing_type
        if request_email is not None:
          self.request_email = request_email
        if request_phone is not None:
          self.request_phone = request_phone
        if request_shipping is not None:
          self.request_shipping = request_shipping
        if ship_to_countries is not None:
          self.ship_to_countries = ship_to_countries
        if show_accepted_network_icons is not None:
          self.show_accepted_network_icons = show_accepted_network_icons

    @property
    def billing_type(self):
        """
        Gets the billing_type of this Upv1capturecontextsCaptureMandate.
        This field defines the type of Billing Address information captured through the Manual card Entry UX. FULL, PARTIAL

        :return: The billing_type of this Upv1capturecontextsCaptureMandate.
        :rtype: str
        """
        return self._billing_type

    @billing_type.setter
    def billing_type(self, billing_type):
        """
        Sets the billing_type of this Upv1capturecontextsCaptureMandate.
        This field defines the type of Billing Address information captured through the Manual card Entry UX. FULL, PARTIAL

        :param billing_type: The billing_type of this Upv1capturecontextsCaptureMandate.
        :type: str
        """

        self._billing_type = billing_type

    @property
    def request_email(self):
        """
        Gets the request_email of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :return: The request_email of this Upv1capturecontextsCaptureMandate.
        :rtype: bool
        """
        return self._request_email

    @request_email.setter
    def request_email(self, request_email):
        """
        Sets the request_email of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :param request_email: The request_email of this Upv1capturecontextsCaptureMandate.
        :type: bool
        """

        self._request_email = request_email

    @property
    def request_phone(self):
        """
        Gets the request_phone of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :return: The request_phone of this Upv1capturecontextsCaptureMandate.
        :rtype: bool
        """
        return self._request_phone

    @request_phone.setter
    def request_phone(self, request_phone):
        """
        Sets the request_phone of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :param request_phone: The request_phone of this Upv1capturecontextsCaptureMandate.
        :type: bool
        """

        self._request_phone = request_phone

    @property
    def request_shipping(self):
        """
        Gets the request_shipping of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :return: The request_shipping of this Upv1capturecontextsCaptureMandate.
        :rtype: bool
        """
        return self._request_shipping

    @request_shipping.setter
    def request_shipping(self, request_shipping):
        """
        Sets the request_shipping of this Upv1capturecontextsCaptureMandate.
        Capture email contact information in the manual card acceptance screens.

        :param request_shipping: The request_shipping of this Upv1capturecontextsCaptureMandate.
        :type: bool
        """

        self._request_shipping = request_shipping

    @property
    def ship_to_countries(self):
        """
        Gets the ship_to_countries of this Upv1capturecontextsCaptureMandate.
        List of countries available to ship to. Use the two- character ISO Standard Country Codes.

        :return: The ship_to_countries of this Upv1capturecontextsCaptureMandate.
        :rtype: list[str]
        """
        return self._ship_to_countries

    @ship_to_countries.setter
    def ship_to_countries(self, ship_to_countries):
        """
        Sets the ship_to_countries of this Upv1capturecontextsCaptureMandate.
        List of countries available to ship to. Use the two- character ISO Standard Country Codes.

        :param ship_to_countries: The ship_to_countries of this Upv1capturecontextsCaptureMandate.
        :type: list[str]
        """

        self._ship_to_countries = ship_to_countries

    @property
    def show_accepted_network_icons(self):
        """
        Gets the show_accepted_network_icons of this Upv1capturecontextsCaptureMandate.
        Show the list of accepted payment icons in the payment button

        :return: The show_accepted_network_icons of this Upv1capturecontextsCaptureMandate.
        :rtype: bool
        """
        return self._show_accepted_network_icons

    @show_accepted_network_icons.setter
    def show_accepted_network_icons(self, show_accepted_network_icons):
        """
        Sets the show_accepted_network_icons of this Upv1capturecontextsCaptureMandate.
        Show the list of accepted payment icons in the payment button

        :param show_accepted_network_icons: The show_accepted_network_icons of this Upv1capturecontextsCaptureMandate.
        :type: bool
        """

        self._show_accepted_network_icons = show_accepted_network_icons

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
        if not isinstance(other, Upv1capturecontextsCaptureMandate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
