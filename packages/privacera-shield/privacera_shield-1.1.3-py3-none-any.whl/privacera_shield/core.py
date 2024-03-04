import json
import logging
import os
import threading
import uuid

from . import interceptor_setup
from .backend import ShieldRestHttpClient, ShieldAccessRequest, HttpTransport, VectorDBAccessRequest
from .exception import PAIGException, AccessControlException
from .message import ErrorMessage, InfoMessage, WarningMessage

_logger = logging.getLogger(__name__)


class PAIGPlugin:
    """
    Base plugin for Privacera AI Governance (PAIG).

    This class provides the foundational functionality for PAIG plugins,
    including method interception and user_name context management.

    Attributes:
        enable_privacera_shield (bool): Whether to enable Privacera Shield.
        frameworks (list): The list of frameworks to intercept methods from.
        thread_local: An instance of threading.local() for managing thread-local data.
        thread_local_rlock: An instance of threading.RLock() for thread-local data locking.
        interceptor_installer_list: A list of interceptor installers for the PAIG plugin.
    """

    USER_CONTEXT = "user_context"
    """This is the key stored in thread-local storage for the user_name context."""

    def __init__(self, **kwargs):
        """
        Initializes an instance of the PAIGPlugin class.

        Args:
            kwargs: The name-value pairs to be set in the context. The following are the supported options:

                enable_privacera_shield (bool): Whether to enable Privacera Shield.

                frameworks (list): The list of frameworks to intercept methods from.

                http: An instance of urlib3.PoolManager to be used by the PAIG plugin.

                max_retries (int): The maximum number of retries for HTTP requests.

                backoff_factor (int): The backoff factor for HTTP retries.

                allowed_methods (list): The list of HTTP methods allowed for retry.

                status_retry_forcelist (list): The list of HTTP status codes for which retry is forced.

                connection_timeout (float): The connection timeout for the access request.

                read_timeout (float): The read timeout for the access request.
        """

        try:
            # TODO need to pass a flag saying this is default app
            # for default app we can look in the folder and pick any config file
            # but when creating a new app we need to pass the config file
            self.default_application = PAIGApplication(**kwargs)
            if not self.default_application.is_configured():
                self.default_application = None
        except PAIGException as e:
            if str(ErrorMessage.SHIELD_SERVER_INITIALIZATION_FAILED.value[0]) in e.args[0]:
                raise e
            else:
                self.default_application = None
        except:
            self.default_application = None

        # Init from the loaded file
        self.enable_privacera_shield = kwargs.get("enable_privacera_shield",
                                                  os.getenv("PRIVACERA_SHIELD_ENABLE", "true").lower() == "true")
        _logger.info(
            InfoMessage.PRIVACERA_SHIELD_IS_ENABLED.format(is_enabled=self.enable_privacera_shield))

        self.interceptor_installer_list = None

        self.frameworks = None
        if "frameworks" in kwargs:
            self.frameworks = kwargs["frameworks"]
        else:
            raise PAIGException(ErrorMessage.FRAMEWORKS_NOT_PROVIDED)

        HttpTransport.setup(**kwargs)

        # TODO replace threading local with ContextVars which are available in python 3.7
        self.thread_local = threading.local()
        self.thread_local_rlock = threading.RLock()

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"PAIGPlugin initialized with {self.__dict__}")

    def get_frameworks_to_intercept(self):
        return self.frameworks

    def get_current_application(self):
        application = self.get_current("application")
        if not application:
            if not self.default_application:
                raise PAIGException(ErrorMessage.APPLICATION_NOT_PROVIDED)
            else:
                return self.default_application
        else:
            return application

    def get_shield_client(self):
        return self.get_current_application().get_shield_client()

    def get_application_key(self):
        return self.get_current_application().get_application_key()

    def get_client_application_key(self):
        return self.get_current_application().get_client_application_key()

    def get_shield_run_mode(self):
        return self.get_current_application().get_shield_run_mode()

    def setup(self):
        """
        Set up the PAIG plugin by intercepting methods for enhanced functionality.
        """
        if self.enable_privacera_shield:
            self.interceptor_installer_list = interceptor_setup.setup(self)

    def undo_setup(self):
        """
        Undo the setup of the PAIG plugin by removing the method interceptors. Usually used for testing.
        :return:
        """
        for interceptor_installer in self.interceptor_installer_list:
            interceptor_installer.undo_setup_interceptors()

    def set_current_user(self, username):
        """
        Set the current user_name context for the PAIG plugin.

        Args:
            username (str): The username of the current user_name.

        Notes:
            This method needs to be called before making any request to LLM
        """
        self.set_current(username=username)

    def get_current_user(self):
        """
        Get the current user_name from the PAIG plugin's context.

        Returns:
            str: The username of the current user_name.

        Raises:
            Exception: If the current user_name is not set in the context.
        """
        return self.get_current("username")

    def generate_request_id(self):
        """
        Generate a unique Request ID.

        Returns:
            str: A unique Request ID in UUID format.
        """
        return str(uuid.uuid4())

    def generate_conversation_thread_id(self):
        """
        Generate a unique Thread ID for the conversation.

        Returns:
            str: A unique Thread ID in UUID format.
        """
        return str(uuid.uuid4())

    def set_current(self, **kwargs):
        """
        Set any name-value into current thread-local context for the PAIG plugin.
        :param kwargs: name=value pairs to be set in the context
        :return: nothing
        """
        with self.thread_local_rlock:
            user_context = getattr(self.thread_local, PAIGPlugin.USER_CONTEXT, {})
            user_context.update(kwargs)
            setattr(self.thread_local, PAIGPlugin.USER_CONTEXT, user_context)

    def get_current(self, key, default_value=None):
        """
        Get the value of the given key from the current thread-local context for the PAIG plugin.
        :param key:
        :param default_value: returned if the key does not exist
        :return:
        """
        with self.thread_local_rlock:
            user_context = getattr(self.thread_local, PAIGPlugin.USER_CONTEXT, {})
            if key in user_context:
                return user_context[key]
            else:
                return default_value

    def clear(self):
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug("Clearing thread-local context for PAIG plugin")
        with self.thread_local_rlock:
            delattr(self.thread_local, PAIGPlugin.USER_CONTEXT)

    def check_access(self, **kwargs):
        return self.get_current_application().check_access(**kwargs)

    def get_vector_db_filter_expression(self, **kwargs):
        return self.get_current_application().get_vector_db_filter_expression(**kwargs)


class PAIGPluginContext:
    """
    This class provides a context manager for the PAIG plugin.
    """

    def __init__(self, **kwargs):
        """
        Initializes an instance of the PAIGPluginContext class.

        Args:
            kwargs: The name-value pairs to be set in the context.

        Attributes:
            kwargs: The name-value pairs to be set in the context.
        """
        self.kwargs = kwargs

    def __enter__(self):
        """
        Set the name-value pairs in the context.

        Returns:
            PAIGPluginContext: The current instance of the PAIGPluginContext class.
        """
        global _paig_plugin
        _paig_plugin.set_current(**self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clear the context.

        Args:
            exc_type: The type of the exception.
            exc_val: The exception value.
            exc_tb: The exception traceback.
        """
        global _paig_plugin
        _paig_plugin.clear()


# Global variable to store the PAIGPlugin instance
_paig_plugin: PAIGPlugin = None


def setup(**options):
    """
    This function initializes the PAIGPlugin instance and calls its 'init' method to set up the PAIG plugin.

    Note:
        The global '_paig_plugin' variable is used to store the PAIGPlugin instance for later use.

    """
    global _paig_plugin
    if _paig_plugin is not None:
        _logger.error(ErrorMessage.PAIG_IS_ALREADY_INITIALIZED.format())
    else:
        _paig_plugin = PAIGPlugin(**options)  # Create an instance of PAIGPlugin
        _paig_plugin.setup()  # Initialize the PAIG plugin
        if _logger.isEnabledFor(logging.INFO):
            _logger.info(InfoMessage.PAIG_IS_INITIALIZED.format(kwargs=options))


def set_current_user(username):
    """
    Set the current user_name context for the PAIG plugin.

    Args:
        username (str): The username of the current user_name.

    Note:
        This function sets the user_name context using the 'set_current_user_context' method of the PAIGPlugin instance
        stored in the global '_paig_plugin' variable.

    """
    global _paig_plugin
    _paig_plugin.set_current_user(username)  # Set the current user_name


def get_current_user():
    global _paig_plugin
    _paig_plugin.get_current("username")


def set_current(**kwargs):
    global _paig_plugin
    _paig_plugin.set_current(**kwargs)


def get_current(key, default_value=None):
    global _paig_plugin
    ret_val = _paig_plugin.get_current(key, default_value)
    return ret_val


def clear():
    global _paig_plugin
    _paig_plugin.clear()


def create_shield_context(**kwargs):
    return PAIGPluginContext(**kwargs)


def check_access(**kwargs):
    global _paig_plugin
    return _paig_plugin.check_access(**kwargs)


def get_vector_db_filter_expression(**kwargs):
    global _paig_plugin
    return _paig_plugin.get_vector_db_filter_expression(**kwargs)


def dummy_access_denied():
    raise AccessControlException("Access Denied")


def setup_app(**kwargs):
    """
    This function creates an instance of PAIGApplication from the application config file.
    Args:
        kwargs: The following are the supported options.
            application_config_file: The path to the application config file.
            application_config: The application config dictionary or string contents of the file
            request_kwargs: The keyword arguments to be passed to the urllib3.request call and can contain
            timeout and retry objects
    Returns:
        Instance of PAIGApplication
    """
    if "application_config_file" in kwargs or "application_config" in kwargs:
        app = PAIGApplication(**kwargs)
        if app.is_configured():
            return app
        else:
            raise PAIGException(ErrorMessage.APPLICATION_NOT_CONFIGURED)
    else:
        raise PAIGException(ErrorMessage.PARAMETERS_FOR_APP_CONFIG_NOT_PROVIDED)


class PAIGApplication:
    """
     Base plugin for Privacera AI Governance (PAIG).

     This class provides the foundational functionality for PAIG plugins,
     including method interception and user_name context management.

     Attributes:
         client_application_key (str): The client application id for the client making requests.
         application_id (str): The application id for the client making requests.
         application_key (str): The application key for the client making requests.
         tenant_id (str): The ID of the tenant using the plugin.
         shield_base_url (str): The base URL for the Shield service.
         api_key (str): The API key.
         shield_server_key_id (str): The key ID for the Shield server.
         shield_server_public_key (str): The public key for the Shield server.
         shield_plugin_key_id (str): The key ID for the Shield plugin.
         shield_plugin_private_key (str): The private key for the Shield plugin.
         shield_run_mode (str): The run mode for the Shield plugin.
         shield_client: An instance of the ShieldRestHttpClient class for making requests to the Shield service.
         request_kwargs: The keyword arguments to be passed to the ShieldRestHttpClient class.
     """

    def __init__(self, **kwargs):
        """
        Initializes an instance of the PAIGPlugin class.

        Args:
            kwargs: The following are the supported options.
                application_config_file (str): The path to the application config file.
                application_config (dict): The application config dictionary or string contents of the file
                request_kwargs (dict): The keyword arguments to be passed to the ShieldRestHttpClient class.

                You can also pass in any of the keys from the application config file as keyword arguments in case
                you want to override the values that are in the application config file.
        """

        plugin_app_config_dict = self.get_plugin_app_config(kwargs)

        # Init from the loaded file
        self.client_application_key = plugin_app_config_dict.get("clientApplicationKey", "*")
        self.application_id = plugin_app_config_dict.get("applicationId")
        self.application_key = plugin_app_config_dict.get("applicationKey")
        self.tenant_id = plugin_app_config_dict.get("tenantId")
        shield_server_url = plugin_app_config_dict.get("shieldServerUrl")
        if shield_server_url is not None :
            self.shield_base_url = shield_server_url
        else:
            self.shield_base_url = plugin_app_config_dict.get("apiServerUrl")
        self.api_key = plugin_app_config_dict.get("apiKey")
        self.shield_server_key_id = plugin_app_config_dict.get("shieldServerKeyId")
        self.shield_server_public_key = plugin_app_config_dict.get("shieldServerPublicKey")
        self.shield_plugin_key_id = plugin_app_config_dict.get("shieldPluginKeyId")
        self.shield_plugin_private_key = plugin_app_config_dict.get("shieldPluginPrivateKey")

        self.shield_run_mode = plugin_app_config_dict.get("shieldRunMode", "freemium")

        # Allow override from kwargs
        for key, value in kwargs.items():
            if key in self.__dict__:
                self.__dict__[key] = value

        encryption_keys_info = {
            "shield_server_key_id": self.shield_server_key_id,
            "shield_server_public_key": self.shield_server_public_key,
            "shield_plugin_key_id": self.shield_plugin_key_id,
            "shield_plugin_private_key": self.shield_plugin_private_key
        }

        self.shield_client = ShieldRestHttpClient(base_url=self.shield_base_url, tenant_id=self.tenant_id,
                                                  api_key=self.api_key, encryption_keys_info=encryption_keys_info,
                                                  request_kwargs=kwargs.get("request_kwargs", {}))

        self.shield_client.init_shield_server()

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"PAIGPlugin initialized with {self.__dict__}")

    def get_plugin_app_config(self, kwargs):
        """
        Get the plugin application config from the given kwargs. User could pass the entire application config
        file contents in application_config parameter or pass the path to the application config file in
        application_config_file parameter.
        :param kwargs:
        :return: application_config as a dictionary
        """
        if "application_config" in kwargs:
            if isinstance(kwargs["application_config"], str):
                try:
                    plugin_app_config_dict = json.loads(kwargs["application_config"])
                except Exception as e:
                    raise PAIGException(ErrorMessage.INVALID_APPLICATION_CONFIG_FILE.format(error_message=e))
            elif isinstance(kwargs["application_config"], dict):
                plugin_app_config_dict = kwargs["application_config"]
            else:
                raise PAIGException(ErrorMessage.INVALID_APPLICATION_CONFIG_FILE_DATA.format())
        else:
            plugin_app_config_dict = self.read_options_from_app_config(kwargs.get("application_config_file"))
        return plugin_app_config_dict

    def read_options_from_app_config(self, application_config_file=None):
        """
        Read the options from the application config file.
        :param application_config_file: application config file name
        :return: application config as a dictionary
        """
        # first check if the file path is in the parameter
        if application_config_file:
            if not os.path.exists(application_config_file):
                raise PAIGException(
                    WarningMessage.APP_CONFIG_FILE_NOT_FOUND_IN_PARAMETER.format(file_path=application_config_file))
            else:
                _logger.info(InfoMessage.USING_CONFIG_FILE_FROM_PARAMETER.format(file_path=application_config_file))
                return self.load_plugin_application_configs_from_file(application_config_file)

        # Get the application config file path from the environment variable
        application_config_file = os.getenv("PRIVACERA_SHIELD_CONF_FILE")
        if application_config_file:
            if not os.path.exists(application_config_file):
                raise PAIGException(
                    ErrorMessage.APP_CONFIG_FILE_IN_ENV_NOT_FOUND.format(file_path=application_config_file))
            else:
                if not os.path.isfile(application_config_file):
                    raise PAIGException(
                        ErrorMessage.APP_CONFIG_FILE_IN_ENV_NOT_FOUND.format(file_path=application_config_file))
                _logger.info(InfoMessage.USING_CONFIG_FILE_FROM_ENV_VAR.format(file_path=application_config_file))
                return self.load_plugin_application_configs_from_file(application_config_file)
        else:
            # If the environment variable is not set, look in the local directory
            application_config_file = PAIGApplication.find_config_file()
            if application_config_file:
                _logger.info(InfoMessage.USING_CONFIG_FILE_FROM_FOLDER.format(file_path=application_config_file))
                return self.load_plugin_application_configs_from_file(application_config_file)

        raise PAIGException(ErrorMessage.API_KEY_NOT_PROVIDED)

    @staticmethod
    def find_config_file():
        application_config_dir = os.getenv("PRIVACERA_SHIELD_CONF_DIR", os.path.join(os.getcwd(), "privacera"))
        if not os.path.exists(application_config_dir):
            _logger.warning(
                WarningMessage.APP_CONFIG_FILE_NOT_FOUND_NO_DEFAULT_FOLDER.format(file_path=application_config_dir))
            return None

        app_config_files = [filename for filename in os.listdir(application_config_dir) if
                            filename.startswith("privacera-shield-") and filename.endswith("-config.json")]
        if len(app_config_files) == 1:
            return os.path.join(application_config_dir, app_config_files[0])
        else:
            raise PAIGException(
                ErrorMessage.MULTIPLE_APP_CONFIG_FILES_FOUND.format(application_config_dir=application_config_dir))

    def load_plugin_application_configs_from_file(self, app_config_file_path: str):
        with open(app_config_file_path, 'r') as config_file:
            plugin_app_config_dict = json.load(config_file)
            return plugin_app_config_dict

    def is_configured(self):
        return (self.application_id and
                self.application_key and
                self.api_key and
                self.tenant_id and
                self.shield_base_url and
                self.shield_server_key_id and
                self.shield_server_public_key and
                self.shield_plugin_key_id and
                self.shield_plugin_private_key)

    def get_shield_client(self):
        return self.shield_client

    def get_application_key(self):
        return self.application_key

    def get_client_application_key(self):
        return self.client_application_key

    def get_shield_run_mode(self):
        return self.shield_run_mode

    def check_access(self, **kwargs):
        access_request = kwargs.get("access_request")
        if access_request is None:
            if "text" not in kwargs:
                raise PAIGException(ErrorMessage.PROMPT_NOT_PROVIDED)
            if "conversation_type" not in kwargs:
                raise PAIGException(ErrorMessage.CONVERSATION_TYPE_NOT_PROVIDED)
            text = kwargs["text"]
            conversation_type = kwargs["conversation_type"]

            global _paig_plugin

            access_request = ShieldAccessRequest(
                application_key=self.get_application_key(),
                client_application_key=self.get_client_application_key(),
                conversation_thread_id=kwargs.get("thread_id", _paig_plugin.generate_conversation_thread_id()),
                request_id=_paig_plugin.generate_request_id(),
                user_name=_paig_plugin.get_current_user(),
                context=ShieldAccessRequest.create_request_context(paig_plugin=_paig_plugin),
                request_text=text if isinstance(text, list) else [text],
                conversation_type=conversation_type,
                shield_run_mode=self.shield_run_mode
            )
        access_result = self.get_shield_client().is_access_allowed(request=access_request)
        if not access_result.get_is_allowed():
            raise AccessControlException(access_result.get_response_messages()[0].get_response_text())
        else:
            return access_result.get_response_messages()

    def get_vector_db_filter_expression(self, **kwargs):
        access_request = kwargs.get("access_request")
        if access_request is None:
            global _paig_plugin

            access_request = VectorDBAccessRequest(
                application_key=self.get_application_key(),
                client_application_key=self.get_client_application_key(),
                conversation_thread_id=kwargs.get("thread_id", _paig_plugin.generate_conversation_thread_id()),
                request_id=_paig_plugin.generate_request_id(),
                user_name=_paig_plugin.get_current_user(),
                shield_run_mode=self.shield_run_mode
            )

        access_result = self.get_shield_client().get_filter_expression(request=access_request)

        return access_result.get_filter_expression()
