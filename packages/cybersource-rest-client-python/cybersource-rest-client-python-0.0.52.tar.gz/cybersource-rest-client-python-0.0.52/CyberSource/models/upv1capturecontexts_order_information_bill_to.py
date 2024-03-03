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


class Upv1capturecontextsOrderInformationBillTo(object):
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
        'address1': 'str',
        'address2': 'str',
        'address3': 'str',
        'address4': 'str',
        'administrative_area': 'str',
        'building_number': 'str',
        'country': 'str',
        'district': 'str',
        'locality': 'str',
        'postal_code': 'str',
        'company': 'Upv1capturecontextsOrderInformationBillToCompany',
        'email': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'middle_name': 'str',
        'name_suffix': 'str',
        'title': 'str',
        'phone_number': 'str',
        'phone_type': 'str'
    }

    attribute_map = {
        'address1': 'address1',
        'address2': 'address2',
        'address3': 'address3',
        'address4': 'address4',
        'administrative_area': 'administrativeArea',
        'building_number': 'buildingNumber',
        'country': 'country',
        'district': 'district',
        'locality': 'locality',
        'postal_code': 'postalCode',
        'company': 'company',
        'email': 'email',
        'first_name': 'firstName',
        'last_name': 'lastName',
        'middle_name': 'middleName',
        'name_suffix': 'nameSuffix',
        'title': 'title',
        'phone_number': 'phoneNumber',
        'phone_type': 'phoneType'
    }

    def __init__(self, address1=None, address2=None, address3=None, address4=None, administrative_area=None, building_number=None, country=None, district=None, locality=None, postal_code=None, company=None, email=None, first_name=None, last_name=None, middle_name=None, name_suffix=None, title=None, phone_number=None, phone_type=None):
        """
        Upv1capturecontextsOrderInformationBillTo - a model defined in Swagger
        """

        self._address1 = None
        self._address2 = None
        self._address3 = None
        self._address4 = None
        self._administrative_area = None
        self._building_number = None
        self._country = None
        self._district = None
        self._locality = None
        self._postal_code = None
        self._company = None
        self._email = None
        self._first_name = None
        self._last_name = None
        self._middle_name = None
        self._name_suffix = None
        self._title = None
        self._phone_number = None
        self._phone_type = None

        if address1 is not None:
          self.address1 = address1
        if address2 is not None:
          self.address2 = address2
        if address3 is not None:
          self.address3 = address3
        if address4 is not None:
          self.address4 = address4
        if administrative_area is not None:
          self.administrative_area = administrative_area
        if building_number is not None:
          self.building_number = building_number
        if country is not None:
          self.country = country
        if district is not None:
          self.district = district
        if locality is not None:
          self.locality = locality
        if postal_code is not None:
          self.postal_code = postal_code
        if company is not None:
          self.company = company
        if email is not None:
          self.email = email
        if first_name is not None:
          self.first_name = first_name
        if last_name is not None:
          self.last_name = last_name
        if middle_name is not None:
          self.middle_name = middle_name
        if name_suffix is not None:
          self.name_suffix = name_suffix
        if title is not None:
          self.title = title
        if phone_number is not None:
          self.phone_number = phone_number
        if phone_type is not None:
          self.phone_type = phone_type

    @property
    def address1(self):
        """
        Gets the address1 of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing street address as it appears on the credit card issuer's records. 

        :return: The address1 of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._address1

    @address1.setter
    def address1(self, address1):
        """
        Sets the address1 of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing street address as it appears on the credit card issuer's records. 

        :param address1: The address1 of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._address1 = address1

    @property
    def address2(self):
        """
        Gets the address2 of this Upv1capturecontextsOrderInformationBillTo.
        Used for additional address information. For example: _Attention: Accounts Payable_ Optional field. 

        :return: The address2 of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._address2

    @address2.setter
    def address2(self, address2):
        """
        Sets the address2 of this Upv1capturecontextsOrderInformationBillTo.
        Used for additional address information. For example: _Attention: Accounts Payable_ Optional field. 

        :param address2: The address2 of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._address2 = address2

    @property
    def address3(self):
        """
        Gets the address3 of this Upv1capturecontextsOrderInformationBillTo.
        Additional address information (third line of the billing address)

        :return: The address3 of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._address3

    @address3.setter
    def address3(self, address3):
        """
        Sets the address3 of this Upv1capturecontextsOrderInformationBillTo.
        Additional address information (third line of the billing address)

        :param address3: The address3 of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._address3 = address3

    @property
    def address4(self):
        """
        Gets the address4 of this Upv1capturecontextsOrderInformationBillTo.
        Additional address information (fourth line of the billing address) 

        :return: The address4 of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._address4

    @address4.setter
    def address4(self, address4):
        """
        Sets the address4 of this Upv1capturecontextsOrderInformationBillTo.
        Additional address information (fourth line of the billing address) 

        :param address4: The address4 of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._address4 = address4

    @property
    def administrative_area(self):
        """
        Gets the administrative_area of this Upv1capturecontextsOrderInformationBillTo.
        State or province of the billing address. Use the [State, Province, and Territory Codes for the United States and Canada](https://developer.cybersource.com/library/documentation/sbc/quickref/states_and_provinces.pdf). 

        :return: The administrative_area of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._administrative_area

    @administrative_area.setter
    def administrative_area(self, administrative_area):
        """
        Sets the administrative_area of this Upv1capturecontextsOrderInformationBillTo.
        State or province of the billing address. Use the [State, Province, and Territory Codes for the United States and Canada](https://developer.cybersource.com/library/documentation/sbc/quickref/states_and_provinces.pdf). 

        :param administrative_area: The administrative_area of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._administrative_area = administrative_area

    @property
    def building_number(self):
        """
        Gets the building_number of this Upv1capturecontextsOrderInformationBillTo.
        Building number in the street address. 

        :return: The building_number of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._building_number

    @building_number.setter
    def building_number(self, building_number):
        """
        Sets the building_number of this Upv1capturecontextsOrderInformationBillTo.
        Building number in the street address. 

        :param building_number: The building_number of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._building_number = building_number

    @property
    def country(self):
        """
        Gets the country of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing country. Use the two-character [ISO Standard Country Codes](http://apps.cybersource.com/library/documentation/sbc/quickref/countries_alpha_list.pdf). 

        :return: The country of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """
        Sets the country of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing country. Use the two-character [ISO Standard Country Codes](http://apps.cybersource.com/library/documentation/sbc/quickref/countries_alpha_list.pdf). 

        :param country: The country of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._country = country

    @property
    def district(self):
        """
        Gets the district of this Upv1capturecontextsOrderInformationBillTo.
        Customer's neighborhood, community, or region (a barrio in Brazil) within the city or municipality 

        :return: The district of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._district

    @district.setter
    def district(self, district):
        """
        Sets the district of this Upv1capturecontextsOrderInformationBillTo.
        Customer's neighborhood, community, or region (a barrio in Brazil) within the city or municipality 

        :param district: The district of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._district = district

    @property
    def locality(self):
        """
        Gets the locality of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing city. 

        :return: The locality of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._locality

    @locality.setter
    def locality(self, locality):
        """
        Sets the locality of this Upv1capturecontextsOrderInformationBillTo.
        Payment card billing city. 

        :param locality: The locality of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._locality = locality

    @property
    def postal_code(self):
        """
        Gets the postal_code of this Upv1capturecontextsOrderInformationBillTo.
        Postal code for the billing address. The postal code must consist of 5 to 9 digits. 

        :return: The postal_code of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """
        Sets the postal_code of this Upv1capturecontextsOrderInformationBillTo.
        Postal code for the billing address. The postal code must consist of 5 to 9 digits. 

        :param postal_code: The postal_code of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._postal_code = postal_code

    @property
    def company(self):
        """
        Gets the company of this Upv1capturecontextsOrderInformationBillTo.

        :return: The company of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: Upv1capturecontextsOrderInformationBillToCompany
        """
        return self._company

    @company.setter
    def company(self, company):
        """
        Sets the company of this Upv1capturecontextsOrderInformationBillTo.

        :param company: The company of this Upv1capturecontextsOrderInformationBillTo.
        :type: Upv1capturecontextsOrderInformationBillToCompany
        """

        self._company = company

    @property
    def email(self):
        """
        Gets the email of this Upv1capturecontextsOrderInformationBillTo.
        Customer's email address, including the full domain name. 

        :return: The email of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this Upv1capturecontextsOrderInformationBillTo.
        Customer's email address, including the full domain name. 

        :param email: The email of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._email = email

    @property
    def first_name(self):
        """
        Gets the first_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's first name. This name must be the same as the name on the card

        :return: The first_name of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's first name. This name must be the same as the name on the card

        :param first_name: The first_name of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """
        Gets the last_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's last name. This name must be the same as the name on the card. 

        :return: The last_name of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's last name. This name must be the same as the name on the card. 

        :param last_name: The last_name of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._last_name = last_name

    @property
    def middle_name(self):
        """
        Gets the middle_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's middle name. 

        :return: The middle_name of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._middle_name

    @middle_name.setter
    def middle_name(self, middle_name):
        """
        Sets the middle_name of this Upv1capturecontextsOrderInformationBillTo.
        Customer's middle name. 

        :param middle_name: The middle_name of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._middle_name = middle_name

    @property
    def name_suffix(self):
        """
        Gets the name_suffix of this Upv1capturecontextsOrderInformationBillTo.
        Customer's name suffix. 

        :return: The name_suffix of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._name_suffix

    @name_suffix.setter
    def name_suffix(self, name_suffix):
        """
        Sets the name_suffix of this Upv1capturecontextsOrderInformationBillTo.
        Customer's name suffix. 

        :param name_suffix: The name_suffix of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._name_suffix = name_suffix

    @property
    def title(self):
        """
        Gets the title of this Upv1capturecontextsOrderInformationBillTo.
        Title. 

        :return: The title of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this Upv1capturecontextsOrderInformationBillTo.
        Title. 

        :param title: The title of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._title = title

    @property
    def phone_number(self):
        """
        Gets the phone_number of this Upv1capturecontextsOrderInformationBillTo.
        Customer's phone number. 

        :return: The phone_number of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """
        Sets the phone_number of this Upv1capturecontextsOrderInformationBillTo.
        Customer's phone number. 

        :param phone_number: The phone_number of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._phone_number = phone_number

    @property
    def phone_type(self):
        """
        Gets the phone_type of this Upv1capturecontextsOrderInformationBillTo.
        Customer's phone number type.  #### For Payouts: This field may be sent only for FDC Compass.  Possible Values: * day * home * night * work 

        :return: The phone_type of this Upv1capturecontextsOrderInformationBillTo.
        :rtype: str
        """
        return self._phone_type

    @phone_type.setter
    def phone_type(self, phone_type):
        """
        Sets the phone_type of this Upv1capturecontextsOrderInformationBillTo.
        Customer's phone number type.  #### For Payouts: This field may be sent only for FDC Compass.  Possible Values: * day * home * night * work 

        :param phone_type: The phone_type of this Upv1capturecontextsOrderInformationBillTo.
        :type: str
        """

        self._phone_type = phone_type

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
        if not isinstance(other, Upv1capturecontextsOrderInformationBillTo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
