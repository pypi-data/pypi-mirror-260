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


class DmConfig(object):
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
        'processing_options': 'DmConfigProcessingOptions',
        'organization': 'DmConfigOrganization',
        'portfolio_controls': 'DmConfigPortfolioControls',
        'thirdparty': 'DmConfigThirdparty'
    }

    attribute_map = {
        'processing_options': 'processingOptions',
        'organization': 'organization',
        'portfolio_controls': 'portfolioControls',
        'thirdparty': 'thirdparty'
    }

    def __init__(self, processing_options=None, organization=None, portfolio_controls=None, thirdparty=None):
        """
        DmConfig - a model defined in Swagger
        """

        self._processing_options = None
        self._organization = None
        self._portfolio_controls = None
        self._thirdparty = None

        if processing_options is not None:
          self.processing_options = processing_options
        if organization is not None:
          self.organization = organization
        if portfolio_controls is not None:
          self.portfolio_controls = portfolio_controls
        if thirdparty is not None:
          self.thirdparty = thirdparty

    @property
    def processing_options(self):
        """
        Gets the processing_options of this DmConfig.

        :return: The processing_options of this DmConfig.
        :rtype: DmConfigProcessingOptions
        """
        return self._processing_options

    @processing_options.setter
    def processing_options(self, processing_options):
        """
        Sets the processing_options of this DmConfig.

        :param processing_options: The processing_options of this DmConfig.
        :type: DmConfigProcessingOptions
        """

        self._processing_options = processing_options

    @property
    def organization(self):
        """
        Gets the organization of this DmConfig.

        :return: The organization of this DmConfig.
        :rtype: DmConfigOrganization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """
        Sets the organization of this DmConfig.

        :param organization: The organization of this DmConfig.
        :type: DmConfigOrganization
        """

        self._organization = organization

    @property
    def portfolio_controls(self):
        """
        Gets the portfolio_controls of this DmConfig.

        :return: The portfolio_controls of this DmConfig.
        :rtype: DmConfigPortfolioControls
        """
        return self._portfolio_controls

    @portfolio_controls.setter
    def portfolio_controls(self, portfolio_controls):
        """
        Sets the portfolio_controls of this DmConfig.

        :param portfolio_controls: The portfolio_controls of this DmConfig.
        :type: DmConfigPortfolioControls
        """

        self._portfolio_controls = portfolio_controls

    @property
    def thirdparty(self):
        """
        Gets the thirdparty of this DmConfig.

        :return: The thirdparty of this DmConfig.
        :rtype: DmConfigThirdparty
        """
        return self._thirdparty

    @thirdparty.setter
    def thirdparty(self, thirdparty):
        """
        Sets the thirdparty of this DmConfig.

        :param thirdparty: The thirdparty of this DmConfig.
        :type: DmConfigThirdparty
        """

        self._thirdparty = thirdparty

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
        if not isinstance(other, DmConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
