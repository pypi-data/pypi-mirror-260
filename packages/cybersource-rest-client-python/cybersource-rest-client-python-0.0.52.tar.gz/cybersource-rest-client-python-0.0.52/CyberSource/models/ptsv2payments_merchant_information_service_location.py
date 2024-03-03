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


class Ptsv2paymentsMerchantInformationServiceLocation(object):
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
        'locality': 'str',
        'country_subdivision_code': 'str',
        'country_code': 'str',
        'postal_code': 'str'
    }

    attribute_map = {
        'locality': 'locality',
        'country_subdivision_code': 'countrySubdivisionCode',
        'country_code': 'countryCode',
        'postal_code': 'postalCode'
    }

    def __init__(self, locality=None, country_subdivision_code=None, country_code=None, postal_code=None):
        """
        Ptsv2paymentsMerchantInformationServiceLocation - a model defined in Swagger
        """

        self._locality = None
        self._country_subdivision_code = None
        self._country_code = None
        self._postal_code = None

        if locality is not None:
          self.locality = locality
        if country_subdivision_code is not None:
          self.country_subdivision_code = country_subdivision_code
        if country_code is not None:
          self.country_code = country_code
        if postal_code is not None:
          self.postal_code = postal_code

    @property
    def locality(self):
        """
        Gets the locality of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location city name. When merchant provides services from a location other than the location identified as merchant location. 

        :return: The locality of this Ptsv2paymentsMerchantInformationServiceLocation.
        :rtype: str
        """
        return self._locality

    @locality.setter
    def locality(self, locality):
        """
        Sets the locality of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location city name. When merchant provides services from a location other than the location identified as merchant location. 

        :param locality: The locality of this Ptsv2paymentsMerchantInformationServiceLocation.
        :type: str
        """

        self._locality = locality

    @property
    def country_subdivision_code(self):
        """
        Gets the country_subdivision_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location country subdivision code. When merchant provides services from a location other than the location identified as merchant location. 

        :return: The country_subdivision_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :rtype: str
        """
        return self._country_subdivision_code

    @country_subdivision_code.setter
    def country_subdivision_code(self, country_subdivision_code):
        """
        Sets the country_subdivision_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location country subdivision code. When merchant provides services from a location other than the location identified as merchant location. 

        :param country_subdivision_code: The country_subdivision_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :type: str
        """

        self._country_subdivision_code = country_subdivision_code

    @property
    def country_code(self):
        """
        Gets the country_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location country code. When merchant provides services from a location other than the location identified as merchant location. 

        :return: The country_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location country code. When merchant provides services from a location other than the location identified as merchant location. 

        :param country_code: The country_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :type: str
        """

        self._country_code = country_code

    @property
    def postal_code(self):
        """
        Gets the postal_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location postal code. When merchant provides services from a location other than the location identified as merchant location. 

        :return: The postal_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """
        Sets the postal_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        #### Visa Platform Connect  Merchant's service location postal code. When merchant provides services from a location other than the location identified as merchant location. 

        :param postal_code: The postal_code of this Ptsv2paymentsMerchantInformationServiceLocation.
        :type: str
        """

        self._postal_code = postal_code

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
        if not isinstance(other, Ptsv2paymentsMerchantInformationServiceLocation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
