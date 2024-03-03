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


class PtsV2PaymentsReversalsPost201ResponseProcessorInformation(object):
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
        'transaction_id': 'str',
        'response_code': 'str',
        'response_category_code': 'str',
        'forwarded_acquirer_code': 'str',
        'master_card_service_code': 'str',
        'master_card_service_reply_code': 'str'
    }

    attribute_map = {
        'transaction_id': 'transactionId',
        'response_code': 'responseCode',
        'response_category_code': 'responseCategoryCode',
        'forwarded_acquirer_code': 'forwardedAcquirerCode',
        'master_card_service_code': 'masterCardServiceCode',
        'master_card_service_reply_code': 'masterCardServiceReplyCode'
    }

    def __init__(self, transaction_id=None, response_code=None, response_category_code=None, forwarded_acquirer_code=None, master_card_service_code=None, master_card_service_reply_code=None):
        """
        PtsV2PaymentsReversalsPost201ResponseProcessorInformation - a model defined in Swagger
        """

        self._transaction_id = None
        self._response_code = None
        self._response_category_code = None
        self._forwarded_acquirer_code = None
        self._master_card_service_code = None
        self._master_card_service_reply_code = None

        if transaction_id is not None:
          self.transaction_id = transaction_id
        if response_code is not None:
          self.response_code = response_code
        if response_category_code is not None:
          self.response_category_code = response_category_code
        if forwarded_acquirer_code is not None:
          self.forwarded_acquirer_code = forwarded_acquirer_code
        if master_card_service_code is not None:
          self.master_card_service_code = master_card_service_code
        if master_card_service_reply_code is not None:
          self.master_card_service_reply_code = master_card_service_reply_code

    @property
    def transaction_id(self):
        """
        Gets the transaction_id of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Processor transaction ID.  This value identifies the transaction on a host system. This value is supported only for Moneris. It contains this information:   - Terminal used to process the transaction  - Shift during which the transaction took place  - Batch number  - Transaction number within the batch  You must store this value. If you give the customer a receipt, display this value on the receipt.  Example For the value 66012345001069003:   - Terminal ID = 66012345  - Shift number = 001  - Batch number = 069  - Transaction number = 003 

        :return: The transaction_id of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """
        Sets the transaction_id of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Processor transaction ID.  This value identifies the transaction on a host system. This value is supported only for Moneris. It contains this information:   - Terminal used to process the transaction  - Shift during which the transaction took place  - Batch number  - Transaction number within the batch  You must store this value. If you give the customer a receipt, display this value on the receipt.  Example For the value 66012345001069003:   - Terminal ID = 66012345  - Shift number = 001  - Batch number = 069  - Transaction number = 003 

        :param transaction_id: The transaction_id of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._transaction_id = transaction_id

    @property
    def response_code(self):
        """
        Gets the response_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        For most processors, this is the error message sent directly from the bank. Returned only when the processor returns this value.  **Important** Do not use this field to evaluate the result of the authorization.  #### PIN debit Response value that is returned by the processor or bank. **Important** Do not use this field to evaluate the results of the transaction request.  Returned by PIN debit credit, PIN debit purchase, and PIN debit reversal.  #### AIBMS If this value is `08`, you can accept the transaction if the customer provides you with identification.  #### Atos This value is the response code sent from Atos and it might also include the response code from the bank. Format: `aa,bb` with the two values separated by a comma and where: - `aa` is the two-digit error message from Atos. - `bb` is the optional two-digit error message from the bank.  #### Comercio Latino This value is the status code and the error or response code received from the processor separated by a colon. Format: [status code]:E[error code] or [status code]:R[response code] Example `2:R06`  #### JCN Gateway Processor-defined detail error code. The associated response category code is in the `processorInformation.responseCategoryCode` field. String (3) 

        :return: The response_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._response_code

    @response_code.setter
    def response_code(self, response_code):
        """
        Sets the response_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        For most processors, this is the error message sent directly from the bank. Returned only when the processor returns this value.  **Important** Do not use this field to evaluate the result of the authorization.  #### PIN debit Response value that is returned by the processor or bank. **Important** Do not use this field to evaluate the results of the transaction request.  Returned by PIN debit credit, PIN debit purchase, and PIN debit reversal.  #### AIBMS If this value is `08`, you can accept the transaction if the customer provides you with identification.  #### Atos This value is the response code sent from Atos and it might also include the response code from the bank. Format: `aa,bb` with the two values separated by a comma and where: - `aa` is the two-digit error message from Atos. - `bb` is the optional two-digit error message from the bank.  #### Comercio Latino This value is the status code and the error or response code received from the processor separated by a colon. Format: [status code]:E[error code] or [status code]:R[response code] Example `2:R06`  #### JCN Gateway Processor-defined detail error code. The associated response category code is in the `processorInformation.responseCategoryCode` field. String (3) 

        :param response_code: The response_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._response_code = response_code

    @property
    def response_category_code(self):
        """
        Gets the response_category_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Processor-defined response category code. The associated detail error code is in the `processorInformation.responseCode` or `issuerInformation.responseCode` field of the service you requested.  This field is supported only for:   - Japanese issuers  - Domestic transactions in Japan  - Comercio Latino—processor transaction ID required for troubleshooting  #### Maximum length for processors   - Comercio Latino: 36  - All other processors: 3 

        :return: The response_category_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._response_category_code

    @response_category_code.setter
    def response_category_code(self, response_category_code):
        """
        Sets the response_category_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Processor-defined response category code. The associated detail error code is in the `processorInformation.responseCode` or `issuerInformation.responseCode` field of the service you requested.  This field is supported only for:   - Japanese issuers  - Domestic transactions in Japan  - Comercio Latino—processor transaction ID required for troubleshooting  #### Maximum length for processors   - Comercio Latino: 36  - All other processors: 3 

        :param response_category_code: The response_category_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._response_category_code = response_category_code

    @property
    def forwarded_acquirer_code(self):
        """
        Gets the forwarded_acquirer_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Name of the Japanese acquirer that processed the transaction. Returned only for JCN Gateway. Please contact the CyberSource Japan Support Group for more information. 

        :return: The forwarded_acquirer_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._forwarded_acquirer_code

    @forwarded_acquirer_code.setter
    def forwarded_acquirer_code(self, forwarded_acquirer_code):
        """
        Sets the forwarded_acquirer_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Name of the Japanese acquirer that processed the transaction. Returned only for JCN Gateway. Please contact the CyberSource Japan Support Group for more information. 

        :param forwarded_acquirer_code: The forwarded_acquirer_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._forwarded_acquirer_code = forwarded_acquirer_code

    @property
    def master_card_service_code(self):
        """
        Gets the master_card_service_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Mastercard service that was used for the transaction. Mastercard provides this value to CyberSource.  Possible value:  - 53: Mastercard card-on-file token service  #### CyberSource through VisaNet The value for this field corresponds to the following data in the TC 33 capture file: - Record: CP01 TCR6 - Position: 133-134 - Field: Mastercard Merchant on-behalf service. **Note** This field is returned only for CyberSource through VisaNet. 

        :return: The master_card_service_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._master_card_service_code

    @master_card_service_code.setter
    def master_card_service_code(self, master_card_service_code):
        """
        Sets the master_card_service_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Mastercard service that was used for the transaction. Mastercard provides this value to CyberSource.  Possible value:  - 53: Mastercard card-on-file token service  #### CyberSource through VisaNet The value for this field corresponds to the following data in the TC 33 capture file: - Record: CP01 TCR6 - Position: 133-134 - Field: Mastercard Merchant on-behalf service. **Note** This field is returned only for CyberSource through VisaNet. 

        :param master_card_service_code: The master_card_service_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._master_card_service_code = master_card_service_code

    @property
    def master_card_service_reply_code(self):
        """
        Gets the master_card_service_reply_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Result of the Mastercard card-on-file token service. Mastercard provides this value to CyberSource.  Possible values:   - `C`: Service completed successfully.  - `F`: One of the following:    - Incorrect Mastercard POS entry mode. The Mastercard POS entry mode should be 81 for an authorization or      authorization reversal.    - Incorrect Mastercard POS entry mode. The Mastercard POS entry mode should be 01 for a tokenized request.    - Token requestor ID is missing or formatted incorrectly.  - `I`: One of the following:    - Invalid token requestor ID.    - Suspended or deactivated token.    - Invalid token (not in mapping table).  - `T`: Invalid combination of token requestor ID and token.  - `U`: Expired token.  - `W`: Primary account number (PAN) listed in electronic warning bulletin.  **Note** This field is returned only for **CyberSource through VisaNet**. 

        :return: The master_card_service_reply_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :rtype: str
        """
        return self._master_card_service_reply_code

    @master_card_service_reply_code.setter
    def master_card_service_reply_code(self, master_card_service_reply_code):
        """
        Sets the master_card_service_reply_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        Result of the Mastercard card-on-file token service. Mastercard provides this value to CyberSource.  Possible values:   - `C`: Service completed successfully.  - `F`: One of the following:    - Incorrect Mastercard POS entry mode. The Mastercard POS entry mode should be 81 for an authorization or      authorization reversal.    - Incorrect Mastercard POS entry mode. The Mastercard POS entry mode should be 01 for a tokenized request.    - Token requestor ID is missing or formatted incorrectly.  - `I`: One of the following:    - Invalid token requestor ID.    - Suspended or deactivated token.    - Invalid token (not in mapping table).  - `T`: Invalid combination of token requestor ID and token.  - `U`: Expired token.  - `W`: Primary account number (PAN) listed in electronic warning bulletin.  **Note** This field is returned only for **CyberSource through VisaNet**. 

        :param master_card_service_reply_code: The master_card_service_reply_code of this PtsV2PaymentsReversalsPost201ResponseProcessorInformation.
        :type: str
        """

        self._master_card_service_reply_code = master_card_service_reply_code

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
        if not isinstance(other, PtsV2PaymentsReversalsPost201ResponseProcessorInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
