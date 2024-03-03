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


class ECheckConfigCommonProcessors(object):
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
        'company_entry_description': 'str',
        'company_id': 'str',
        'batch_group': 'str',
        'enable_accuity_for_avs': 'bool',
        'set_completed_state': 'bool'
    }

    attribute_map = {
        'company_entry_description': 'companyEntryDescription',
        'company_id': 'companyId',
        'batch_group': 'batchGroup',
        'enable_accuity_for_avs': 'enableAccuityForAvs',
        'set_completed_state': 'setCompletedState'
    }

    def __init__(self, company_entry_description=None, company_id=None, batch_group=None, enable_accuity_for_avs=True, set_completed_state=False):
        """
        ECheckConfigCommonProcessors - a model defined in Swagger
        """

        self._company_entry_description = None
        self._company_id = None
        self._batch_group = None
        self._enable_accuity_for_avs = None
        self._set_completed_state = None

        self.company_entry_description = company_entry_description
        if company_id is not None:
          self.company_id = company_id
        if batch_group is not None:
          self.batch_group = batch_group
        if enable_accuity_for_avs is not None:
          self.enable_accuity_for_avs = enable_accuity_for_avs
        if set_completed_state is not None:
          self.set_completed_state = set_completed_state

    @property
    def company_entry_description(self):
        """
        Gets the company_entry_description of this ECheckConfigCommonProcessors.
        *EXISTING* Company (merchant) defined description of entry to receive.  For e.g. PAYROLL, GAS BILL, INS PREM. This field is alphanumeric

        :return: The company_entry_description of this ECheckConfigCommonProcessors.
        :rtype: str
        """
        return self._company_entry_description

    @company_entry_description.setter
    def company_entry_description(self, company_entry_description):
        """
        Sets the company_entry_description of this ECheckConfigCommonProcessors.
        *EXISTING* Company (merchant) defined description of entry to receive.  For e.g. PAYROLL, GAS BILL, INS PREM. This field is alphanumeric

        :param company_entry_description: The company_entry_description of this ECheckConfigCommonProcessors.
        :type: str
        """
        if company_entry_description is None:
            raise ValueError("Invalid value for `company_entry_description`, must not be `None`")

        self._company_entry_description = company_entry_description

    @property
    def company_id(self):
        """
        Gets the company_id of this ECheckConfigCommonProcessors.
        *EXISTING* company ID assigned to merchant by Acquiring bank. This field is alphanumeric

        :return: The company_id of this ECheckConfigCommonProcessors.
        :rtype: str
        """
        return self._company_id

    @company_id.setter
    def company_id(self, company_id):
        """
        Sets the company_id of this ECheckConfigCommonProcessors.
        *EXISTING* company ID assigned to merchant by Acquiring bank. This field is alphanumeric

        :param company_id: The company_id of this ECheckConfigCommonProcessors.
        :type: str
        """

        self._company_id = company_id

    @property
    def batch_group(self):
        """
        Gets the batch_group of this ECheckConfigCommonProcessors.
        *EXISTING* Capture requests are grouped into a batch bound for your payment processor. The batch time can be identified by reading the last 2-digits as military time. E.g., <processor>_16 = your processing cutoff is 4PM PST. Please note if you are in a different location you may then need to convert time zone as well.

        :return: The batch_group of this ECheckConfigCommonProcessors.
        :rtype: str
        """
        return self._batch_group

    @batch_group.setter
    def batch_group(self, batch_group):
        """
        Sets the batch_group of this ECheckConfigCommonProcessors.
        *EXISTING* Capture requests are grouped into a batch bound for your payment processor. The batch time can be identified by reading the last 2-digits as military time. E.g., <processor>_16 = your processing cutoff is 4PM PST. Please note if you are in a different location you may then need to convert time zone as well.

        :param batch_group: The batch_group of this ECheckConfigCommonProcessors.
        :type: str
        """

        self._batch_group = batch_group

    @property
    def enable_accuity_for_avs(self):
        """
        Gets the enable_accuity_for_avs of this ECheckConfigCommonProcessors.
        *NEW* Accuity is the original validation service that checks the account/routing number for formatting issues. Used by WF and set to \"Yes\" unless told otherwise

        :return: The enable_accuity_for_avs of this ECheckConfigCommonProcessors.
        :rtype: bool
        """
        return self._enable_accuity_for_avs

    @enable_accuity_for_avs.setter
    def enable_accuity_for_avs(self, enable_accuity_for_avs):
        """
        Sets the enable_accuity_for_avs of this ECheckConfigCommonProcessors.
        *NEW* Accuity is the original validation service that checks the account/routing number for formatting issues. Used by WF and set to \"Yes\" unless told otherwise

        :param enable_accuity_for_avs: The enable_accuity_for_avs of this ECheckConfigCommonProcessors.
        :type: bool
        """

        self._enable_accuity_for_avs = enable_accuity_for_avs

    @property
    def set_completed_state(self):
        """
        Gets the set_completed_state of this ECheckConfigCommonProcessors.
        *Moved* When set to Yes we will automatically update transactions to a completed status X-number of days after the transaction comes through; if no failure notification is received. When set to No means we will not update transaction status in this manner. For BAMS/Bank of America merchants, they should be set to No unless we are explicitly asked to set a merchant to YES.

        :return: The set_completed_state of this ECheckConfigCommonProcessors.
        :rtype: bool
        """
        return self._set_completed_state

    @set_completed_state.setter
    def set_completed_state(self, set_completed_state):
        """
        Sets the set_completed_state of this ECheckConfigCommonProcessors.
        *Moved* When set to Yes we will automatically update transactions to a completed status X-number of days after the transaction comes through; if no failure notification is received. When set to No means we will not update transaction status in this manner. For BAMS/Bank of America merchants, they should be set to No unless we are explicitly asked to set a merchant to YES.

        :param set_completed_state: The set_completed_state of this ECheckConfigCommonProcessors.
        :type: bool
        """

        self._set_completed_state = set_completed_state

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
        if not isinstance(other, ECheckConfigCommonProcessors):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
