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


class CardProcessingConfigCommonAcquirer(object):
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
        'institution_id': 'str',
        'interbank_card_association_id': 'str',
        'discover_institution_id': 'str',
        'country_code': 'str',
        'file_destination_bin': 'str'
    }

    attribute_map = {
        'institution_id': 'institutionId',
        'interbank_card_association_id': 'interbankCardAssociationId',
        'discover_institution_id': 'discoverInstitutionId',
        'country_code': 'countryCode',
        'file_destination_bin': 'fileDestinationBin'
    }

    def __init__(self, institution_id=None, interbank_card_association_id=None, discover_institution_id=None, country_code=None, file_destination_bin=None):
        """
        CardProcessingConfigCommonAcquirer - a model defined in Swagger
        """

        self._institution_id = None
        self._interbank_card_association_id = None
        self._discover_institution_id = None
        self._country_code = None
        self._file_destination_bin = None

        if institution_id is not None:
          self.institution_id = institution_id
        if interbank_card_association_id is not None:
          self.interbank_card_association_id = interbank_card_association_id
        if discover_institution_id is not None:
          self.discover_institution_id = discover_institution_id
        if country_code is not None:
          self.country_code = country_code
        if file_destination_bin is not None:
          self.file_destination_bin = file_destination_bin

    @property
    def institution_id(self):
        """
        Gets the institution_id of this CardProcessingConfigCommonAcquirer.
        Identifier of the acquirer. This number is usually assigned by Visa. Applicable for VPC, GPX (gpx), CMCIC (cmcic), EFTPOS, CB2A, CUP, American Express Direct (amexdirect) and Six (six) processors.  Validation details (for selected processors)...  <table> <thead><tr><th>Processor</th><th>Acceptance Type</th><th>Required</th><th>Min. Length</th><th>Max. Length</th><th>Regex</th><th>Default Value</th></tr></thead> <tr><td>American Express Direct</td><td>cnp, cp, hybrid</td><td>Yes</td><td>1</td><td>13</td><td>^[0-9]+$</td><td>1111</td></tr> </table> 

        :return: The institution_id of this CardProcessingConfigCommonAcquirer.
        :rtype: str
        """
        return self._institution_id

    @institution_id.setter
    def institution_id(self, institution_id):
        """
        Sets the institution_id of this CardProcessingConfigCommonAcquirer.
        Identifier of the acquirer. This number is usually assigned by Visa. Applicable for VPC, GPX (gpx), CMCIC (cmcic), EFTPOS, CB2A, CUP, American Express Direct (amexdirect) and Six (six) processors.  Validation details (for selected processors)...  <table> <thead><tr><th>Processor</th><th>Acceptance Type</th><th>Required</th><th>Min. Length</th><th>Max. Length</th><th>Regex</th><th>Default Value</th></tr></thead> <tr><td>American Express Direct</td><td>cnp, cp, hybrid</td><td>Yes</td><td>1</td><td>13</td><td>^[0-9]+$</td><td>1111</td></tr> </table> 

        :param institution_id: The institution_id of this CardProcessingConfigCommonAcquirer.
        :type: str
        """

        self._institution_id = institution_id

    @property
    def interbank_card_association_id(self):
        """
        Gets the interbank_card_association_id of this CardProcessingConfigCommonAcquirer.
        Number assigned by MasterCard to banks to identify the member in transactions. Applicable for VPC and GPX (gpx) processors.

        :return: The interbank_card_association_id of this CardProcessingConfigCommonAcquirer.
        :rtype: str
        """
        return self._interbank_card_association_id

    @interbank_card_association_id.setter
    def interbank_card_association_id(self, interbank_card_association_id):
        """
        Sets the interbank_card_association_id of this CardProcessingConfigCommonAcquirer.
        Number assigned by MasterCard to banks to identify the member in transactions. Applicable for VPC and GPX (gpx) processors.

        :param interbank_card_association_id: The interbank_card_association_id of this CardProcessingConfigCommonAcquirer.
        :type: str
        """

        self._interbank_card_association_id = interbank_card_association_id

    @property
    def discover_institution_id(self):
        """
        Gets the discover_institution_id of this CardProcessingConfigCommonAcquirer.
        Assigned by Discover to identify the acquirer. Applicable for VPC and GPX (gpx) processors.

        :return: The discover_institution_id of this CardProcessingConfigCommonAcquirer.
        :rtype: str
        """
        return self._discover_institution_id

    @discover_institution_id.setter
    def discover_institution_id(self, discover_institution_id):
        """
        Sets the discover_institution_id of this CardProcessingConfigCommonAcquirer.
        Assigned by Discover to identify the acquirer. Applicable for VPC and GPX (gpx) processors.

        :param discover_institution_id: The discover_institution_id of this CardProcessingConfigCommonAcquirer.
        :type: str
        """

        self._discover_institution_id = discover_institution_id

    @property
    def country_code(self):
        """
        Gets the country_code of this CardProcessingConfigCommonAcquirer.
        ISO 4217 format. Applicable for VPC, GPX (gpx), EFTPOS, RUPAY, Prisma (prisma) and CUP processors.

        :return: The country_code of this CardProcessingConfigCommonAcquirer.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this CardProcessingConfigCommonAcquirer.
        ISO 4217 format. Applicable for VPC, GPX (gpx), EFTPOS, RUPAY, Prisma (prisma) and CUP processors.

        :param country_code: The country_code of this CardProcessingConfigCommonAcquirer.
        :type: str
        """

        self._country_code = country_code

    @property
    def file_destination_bin(self):
        """
        Gets the file_destination_bin of this CardProcessingConfigCommonAcquirer.
        The BIN to which this capturefile is sent. This field must contain a valid BIN. Applicable for VPC and GPX (gpx) processors.

        :return: The file_destination_bin of this CardProcessingConfigCommonAcquirer.
        :rtype: str
        """
        return self._file_destination_bin

    @file_destination_bin.setter
    def file_destination_bin(self, file_destination_bin):
        """
        Sets the file_destination_bin of this CardProcessingConfigCommonAcquirer.
        The BIN to which this capturefile is sent. This field must contain a valid BIN. Applicable for VPC and GPX (gpx) processors.

        :param file_destination_bin: The file_destination_bin of this CardProcessingConfigCommonAcquirer.
        :type: str
        """

        self._file_destination_bin = file_destination_bin

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
        if not isinstance(other, CardProcessingConfigCommonAcquirer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
