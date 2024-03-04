import json
import logging
import threading
import time

import urllib3
from urllib3 import Timeout, Retry

from . import util
from .PluginAccessRequestEncryptor import PluginAccessRequestEncryptor
from .exception import PAIGException
from .message import ErrorMessage
from .model import ConversationType, ResponseMessage
from .util import AtomicCounter

_logger = logging.getLogger(__name__)

sequence_number = AtomicCounter()


class ShieldAccessRequest:
    def __init__(self, **kwargs):
        """
        Initialize a ShieldAccessRequest instance.

        Args:
            application_key (str): The Key of the application.
            client_application_key (str): The Key of the client application.
            conversation_thread_id (str): The ID of the conversation thread.
            request_id (str): The Request ID.
            user_name (str): The name of the user making the request.
            context (dict): The dictionary containing extra information about request.
            request_text (list[str]): The text of the request.
            conversation_type (str): The type of conversation (prompt or reply).

        Note:
            - The conversation_type should be one of the values defined in the ConversationType enum.

        """
        self.application_key = kwargs.get('application_key')
        self.client_application_key = kwargs.get('client_application_key')
        self.conversation_thread_id = kwargs.get('conversation_thread_id')
        self.request_id = kwargs.get('request_id')
        self.user_name = kwargs.get('user_name')
        self.context = kwargs.get('context', {})
        self.request_text = kwargs.get('request_text')
        self.conversation_type = kwargs.get('conversation_type', ConversationType.PROMPT)
        self.shield_server_key_id = kwargs.get('shield_server_key_id', None)
        self.shield_plugin_key_id = kwargs.get('shield_plugin_key_id', None)
        self.shield_run_mode = kwargs.get('shield_run_mode', "freemium")

    def to_payload_dict(self):
        """
        Serialize the ShieldAccessRequest instance to a JSON string.

        Returns:
            str: JSON representation of the instance.
        """
        request_dict = {
            # "conversationId": "1001", # Not able to get

            "threadId": self.conversation_thread_id,
            "requestId": self.request_id,

            "sequenceNumber": sequence_number.increment(),
            "requestType": self.conversation_type.lower(),

            "requestDateTime": int(time.time()) * 1000,
            # datetime.now(timezone.utc),
            # utils.get_time_now_utc_str(), # TODO: this is a breaking change from int to iso8601 time format

            "clientApplicationKey": self.client_application_key,
            "applicationKey": self.application_key,

            "userId": self.user_name,

            "context": self.context,  # Additional context information
            "messages": self.request_text,

            "clientIp": util.get_my_ip_address(),
            "clientHostName": util.get_my_hostname(),

            "shieldServerKeyId": self.shield_server_key_id,
            "shieldPluginKeyId": self.shield_plugin_key_id
        }

        return request_dict

    @classmethod
    def create_request_context(cls, paig_plugin):
        context = {}

        vector_db_filter_expr = paig_plugin.get_current("vector_db_filter_expr", default_value=None)
        if vector_db_filter_expr is not None:
            context["vector_db_filter_expr"] = vector_db_filter_expr
            paig_plugin.set_current(vector_db_filter_expr=None)

        return context


class ShieldAccessResult:
    def __init__(self, **kwargs):
        """
        Initialize a ShieldAccessResult instance.

        Args:
            threadId (str): The ID of the thread.
            requestId (str): The ID of the request.
            sequenceNumber (int): The sequence number.
            isAllowed (bool): Indicates whether the access is allowed.
            responseMessages (list): A list of response messages.

        Attributes:
            threadId (str): The ID of the thread.
            requestId (str): The ID of the request.
            sequenceNumber (int): The sequence number.
            isAllowed (bool): Indicates whether the access is allowed.
            responseMessages (list): A list of response messages.
        """
        self.threadId = kwargs.get('threadId')
        self.requestId = kwargs.get('requestId')
        self.sequenceNumber = kwargs.get('sequenceNumber')
        self.isAllowed = kwargs.get('isAllowed')
        self.responseMessages = kwargs.get('responseMessages')

    @classmethod
    def from_json(cls, **response_dict):
        """
        Deserialize a JSON string to create a ShieldAccessResult instance.

        Args:
            response_dict (str): JSON representation of the ShieldAccessResult.

        Returns:
            ShieldAccessResult: An instance of ShieldAccessResult.
        """
        return cls(**response_dict)

    def get_response_messages(self):
        """
        Get a list of ResponseMessage instances from 'responseMessages'.

        Returns:
            list: A list of ResponseMessage instances.
        """
        response_messages = []
        for message in self.responseMessages:
            response_messages.append(ResponseMessage(message['responseText']))
        return response_messages

    def get_last_response_message(self) -> ResponseMessage:
        """
        Get the last ResponseMessage in the 'responseMessages' list.

        Returns:
            ResponseMessage: The last ResponseMessage.

        Raises:
            Exception: If no responseMessages are found.
        """
        if len(self.responseMessages) == 0:
            raise Exception("No responseMessages found.")

        last_response_message = self.responseMessages[-1]
        return ResponseMessage(last_response_message['responseText'])

    def get_is_allowed(self):
        """
        Get the 'isAllowed' attribute value.

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        return self.isAllowed


class VectorDBAccessRequest:
    """
            Initialize a VectorDBAccessRequest instance.

            Args:
                application_key (str): The Key of the application.
                client_application_key (str): The Key of the client application.
                conversation_thread_id (str): The ID of the conversation thread.
                request_id (str): The Request ID.
                user_name (str): The name of the user making the request.
                request_text (list[str]): The text of the request.
                conversation_type (str): The type of conversation (prompt or reply).
            """

    def __init__(self, **kwargs):
        self.application_key = kwargs.get('application_key')
        self.client_application_key = kwargs.get('client_application_key')
        self.conversation_thread_id = kwargs.get('conversation_thread_id')
        self.request_id = kwargs.get('request_id')
        self.user_name = kwargs.get('user_name')
        self.shield_run_mode = kwargs.get('shield_run_mode', "freemium")

    def to_payload_dict(self):
        """
                Serialize the VectorDBAccessRequest instance to a JSON string.

                Returns:
                    str: JSON representation of the instance.
        """
        request_dict = {
            "threadId": self.conversation_thread_id,
            "requestId": self.request_id,
            "sequenceNumber": sequence_number.increment(),
            "requestDateTime": int(time.time()) * 1000,
            "clientApplicationKey": self.client_application_key,
            "applicationKey": self.application_key,
            "userId": self.user_name,
            "context": {},  # Additional context information
            "clientIp": util.get_my_ip_address(),
            "clientHostName": util.get_my_hostname(),
        }

        return request_dict


class VectorDBAccessResult:
    """
            Initialize a VectorDBAccessResult instance.

            Args:
                filterExpression (str): Row level filter expression policy

            Attributes:
                filterExpression (str): Row level filter expression policy
    """

    def __init__(self, **kwargs):
        self.filterExpression = kwargs.get('filterExpression')

    @classmethod
    def from_json(cls, **response_dict):
        """
                Deserialize a JSON string to create a ShieldAccessResult instance.

                Args:
                    response_dict (str): JSON representation of the ShieldAccessResult.

                Returns:
                    VectorDBAccessResult: An instance of VectorDBAccessResult.
                """
        return cls(**response_dict)

    def get_filter_expression(self):
        """
        Get the 'filter_expression' attribute value.

        Returns:
            str: returns filter expression .
        """
        return self.filterExpression


class HttpTransport:
    """
    HttpTransport class maintains a single instance of urllib3.PoolManager for all the ShieldRestHttpClient instances.
    """
    _http: urllib3.PoolManager = None
    _rw_lock = threading.RLock()

    _max_retries = 4
    _backoff_factor = 1
    _allowed_methods = ["GET", "POST", "PUT", "DELETE"]
    _status_forcelist = [500, 502, 503, 504]
    _connect_timeout_sec = 2.0
    _read_timeout_sec = 7.0
    """
    These are default settings that can be overridden by calling the setup method.
    """

    @staticmethod
    def setup(**kwargs):
        """
        This optional method allows you to pass your own instance of the PoolManager to be used by all the
        ShieldRestHttpClient instances.
        :param kwargs:
            - http: Instance of urllib3.PoolManager
            - max_retries
            - backoff_factor
            - allowed_methods
            - status_forcelist
            - connect_timeout_sec
            - read_timeout_sec
        :return:
        """
        HttpTransport._http = kwargs.get('http', HttpTransport._http)
        HttpTransport._max_retries = kwargs.get('max_retries', HttpTransport._max_retries)
        HttpTransport._backoff_factor = kwargs.get('backoff_factor', HttpTransport._backoff_factor)
        HttpTransport._allowed_methods = kwargs.get('allowed_methods', HttpTransport._allowed_methods)
        HttpTransport._status_forcelist = kwargs.get('status_forcelist', HttpTransport._status_forcelist)
        HttpTransport._connect_timeout_sec = kwargs.get('connect_timeout_sec', HttpTransport._connect_timeout_sec)
        HttpTransport._read_timeout_sec = kwargs.get('read_timeout_sec', HttpTransport._read_timeout_sec)

    @staticmethod
    def get_http():
        if not HttpTransport._http:
            HttpTransport.create_default_http()
        return HttpTransport._http

    @staticmethod
    def create_default_http():
        with HttpTransport._rw_lock:
            if not HttpTransport._http:
                # TODO: add proxy support
                # TODO: add ignore SSL support
                # TODO: expose any metrics

                retries = Retry(total=HttpTransport._max_retries,
                                backoff_factor=HttpTransport._backoff_factor,
                                allowed_methods=HttpTransport._allowed_methods,
                                status_forcelist=HttpTransport._status_forcelist)
                timeout = Timeout(connect=HttpTransport._connect_timeout_sec, read=HttpTransport._read_timeout_sec)
                HttpTransport._http = urllib3.PoolManager(maxsize=50, block=True, retries=retries, timeout=timeout)


class ShieldRestHttpClient:
    """
    ShieldRestHttpClient class is the main class that is used to make requests to the Privacera Shield server.
    """

    def __init__(self, **kwargs):
        self.tenant_id = kwargs['tenant_id'] if 'tenant_id' in kwargs else None
        self.base_url = kwargs['base_url']
        self.api_key = kwargs['api_key']

        # you can pass in a dict() in request_kwargs that will added to kwargs of the request method call
        # this will allow you to set custom Timeout or Retry objects for an application
        self.request_kwargs = kwargs.get('request_kwargs', {})
        if 'timeout' not in self.request_kwargs:
            self.request_kwargs['timeout'] = Timeout(connect=2.0, read=7.0)

        self.plugin_access_request_encryptor = PluginAccessRequestEncryptor(self.tenant_id,
                                                                            kwargs["encryption_keys_info"])

    def get_default_headers(self):
        headers = dict()
        if self.tenant_id:
            headers["x-tenant-id"] = self.tenant_id
        if self.api_key:
            headers["x-paig-api-key"] = self.api_key
        return headers

    def is_access_allowed(self, request: ShieldAccessRequest) -> ShieldAccessResult:
        """
        Check if access is allowed and return the result.

        Args:
            request (ShieldAccessRequest): The access request to be checked.

        Returns:
            ShieldAccessResult: The result of the access check.
        """

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access request parameters: {request.to_payload_dict()}")

        if request.shield_run_mode == "freemium":
            # Encrypt the request messages and set the encryption key id and plugin public key in request
            self.plugin_access_request_encryptor.encrypt_request(request)

        request.shield_server_key_id = self.plugin_access_request_encryptor.shield_server_key_id
        request.shield_plugin_key_id = self.plugin_access_request_encryptor.shield_plugin_key_id

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access request parameters (encrypted): {request.to_payload_dict()}")

        response = HttpTransport.get_http().request(method="POST",
                                                    url=self.base_url + "/shield/authorize",
                                                    headers=self.get_default_headers(),
                                                    json=request.to_payload_dict(),
                                                    **self.request_kwargs)

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access response status (encrypted): {response.status}, body: {response.data}")

        if response.status == 200:
            access_result = ShieldAccessResult.from_json(**response.json())
            if access_result.isAllowed and request.shield_run_mode == "freemium":
                # Decrypt the response messages
                self.plugin_access_request_encryptor.decrypt_response(access_result)
                if _logger.isEnabledFor(logging.DEBUG):
                    _logger.debug(
                        f"Access response status: {response.status}, access_result: {json.dumps(access_result.__dict__)}")
            return access_result
        else:
            error_message = f"Request failed with status code {response.status}: {response.data}"
            _logger.error(error_message)
            raise Exception(error_message)

    def init_shield_server(self) -> None:
        """
        Initialize shield server for the tenant id.
        """
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Initializing shield server for tenant: tenant_id={self.tenant_id}")

        request = {"shieldServerKeyId": self.plugin_access_request_encryptor.shield_server_key_id,
                   "shieldPluginKeyId": self.plugin_access_request_encryptor.shield_plugin_key_id}

        error_message = ""
        init_success = False
        response_status = 0

        try:
            response = HttpTransport.get_http().request(method="POST",
                                                        url=self.base_url + "/shield/init",
                                                        headers=self.get_default_headers(),
                                                        json=json.dumps(request),
                                                        **self.request_kwargs)

            response_status = response.status

            if _logger.isEnabledFor(logging.DEBUG):
                _logger.debug(f"Shield server initialization response status: {response.status}, body: {response.data}")

            if response_status == 200:
                init_success = True
                _logger.info(f"Shield server initialized for tenant: tenant_id={self.tenant_id}")
            else:
                if response_status == 400 or response_status == 404:
                    error_message = str(response.data)
                    error_message += (
                        "\n\nThe request sent to the shield server for initialization is invalid or malformed.\n\n"
                        "To resolve this issue, please verify the configuration file for the plugin.\n"
                        "Try re-downloading the configuration file from the PAIG Portal and restarting your application to ensure that the configuration is correct.\n\n"
                        "For detailed instructions, please follow the guidance provided in the integration documentation at https://na.privacera.ai/docs/integration/.\n"
                        "If the issue persists after performing the above steps, please contact Privacera Support for further assistance."
                    )
                elif response_status == 500:
                    error_message = str(response.data)
                    error_message += (
                        "\n\nThe server encountered an unexpected condition that prevented it from fulfilling the request.\n\n"
                        "Please contact Privacera Support for further assistance."
                    )
        except Exception as e:
            error_message = (
                "\n\nThe Privacera Shield Plugin is unable to establish a connection with the Privacera Shield Server.\n"
                "Please ensure that the Shield Server is up and running and is reachable from the current environment where this application is being executed.\n\n"
                "For privacera.ai hosted shield server, verify https://status.privacera.com for any reported downtime.\n"
                "If the issue persists after performing the above steps, please contact Privacera Support for further assistance."
            )

        if not init_success:
            message = ErrorMessage.SHIELD_SERVER_INITIALIZATION_FAILED.format(response_status=response_status,
                                                                              response_data=error_message)
            _logger.error(message)
            raise PAIGException(message)

    def get_filter_expression(self, request: VectorDBAccessRequest) -> VectorDBAccessResult:

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Vector DB Access request parameters: {request.to_payload_dict()}")

        response = HttpTransport.get_http().request(method="POST",
                                     url=self.base_url + "/shield/authorize/vectordb",
                                     headers=self.get_default_headers(),
                                     json=request.to_payload_dict(),
                                     **self.request_kwargs)

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Response status: {response.status}, body: {response.data}")

        if response.status == 200:
            return VectorDBAccessResult.from_json(**response.json())
        else:
            error_message = f"Request failed with status code {response.status}: {response.data}"
            _logger.error(error_message)
            raise Exception(error_message)