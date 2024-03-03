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


class PatchCustomerShippingAddressRequest(object):
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
        'links': 'Tmsv2customersEmbeddedDefaultShippingAddressLinks',
        'id': 'str',
        'default': 'bool',
        'ship_to': 'Tmsv2customersEmbeddedDefaultShippingAddressShipTo',
        'metadata': 'Tmsv2customersEmbeddedDefaultShippingAddressMetadata'
    }

    attribute_map = {
        'links': '_links',
        'id': 'id',
        'default': 'default',
        'ship_to': 'shipTo',
        'metadata': 'metadata'
    }

    def __init__(self, links=None, id=None, default=None, ship_to=None, metadata=None):
        """
        PatchCustomerShippingAddressRequest - a model defined in Swagger
        """

        self._links = None
        self._id = None
        self._default = None
        self._ship_to = None
        self._metadata = None

        if links is not None:
          self.links = links
        if id is not None:
          self.id = id
        if default is not None:
          self.default = default
        if ship_to is not None:
          self.ship_to = ship_to
        if metadata is not None:
          self.metadata = metadata

    @property
    def links(self):
        """
        Gets the links of this PatchCustomerShippingAddressRequest.

        :return: The links of this PatchCustomerShippingAddressRequest.
        :rtype: Tmsv2customersEmbeddedDefaultShippingAddressLinks
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this PatchCustomerShippingAddressRequest.

        :param links: The links of this PatchCustomerShippingAddressRequest.
        :type: Tmsv2customersEmbeddedDefaultShippingAddressLinks
        """

        self._links = links

    @property
    def id(self):
        """
        Gets the id of this PatchCustomerShippingAddressRequest.
        The Id of the Shipping Address Token.

        :return: The id of this PatchCustomerShippingAddressRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PatchCustomerShippingAddressRequest.
        The Id of the Shipping Address Token.

        :param id: The id of this PatchCustomerShippingAddressRequest.
        :type: str
        """

        self._id = id

    @property
    def default(self):
        """
        Gets the default of this PatchCustomerShippingAddressRequest.
        Flag that indicates whether customer shipping address is the dafault. Possible Values:  - `true`: Shipping Address is customer's default.  - `false`: Shipping Address is not customer's default. 

        :return: The default of this PatchCustomerShippingAddressRequest.
        :rtype: bool
        """
        return self._default

    @default.setter
    def default(self, default):
        """
        Sets the default of this PatchCustomerShippingAddressRequest.
        Flag that indicates whether customer shipping address is the dafault. Possible Values:  - `true`: Shipping Address is customer's default.  - `false`: Shipping Address is not customer's default. 

        :param default: The default of this PatchCustomerShippingAddressRequest.
        :type: bool
        """

        self._default = default

    @property
    def ship_to(self):
        """
        Gets the ship_to of this PatchCustomerShippingAddressRequest.

        :return: The ship_to of this PatchCustomerShippingAddressRequest.
        :rtype: Tmsv2customersEmbeddedDefaultShippingAddressShipTo
        """
        return self._ship_to

    @ship_to.setter
    def ship_to(self, ship_to):
        """
        Sets the ship_to of this PatchCustomerShippingAddressRequest.

        :param ship_to: The ship_to of this PatchCustomerShippingAddressRequest.
        :type: Tmsv2customersEmbeddedDefaultShippingAddressShipTo
        """

        self._ship_to = ship_to

    @property
    def metadata(self):
        """
        Gets the metadata of this PatchCustomerShippingAddressRequest.

        :return: The metadata of this PatchCustomerShippingAddressRequest.
        :rtype: Tmsv2customersEmbeddedDefaultShippingAddressMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this PatchCustomerShippingAddressRequest.

        :param metadata: The metadata of this PatchCustomerShippingAddressRequest.
        :type: Tmsv2customersEmbeddedDefaultShippingAddressMetadata
        """

        self._metadata = metadata

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
        if not isinstance(other, PatchCustomerShippingAddressRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
