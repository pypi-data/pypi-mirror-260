import inspect
import logging
from typing import Optional, Union, Any
from uuid import UUID

from langchain.callbacks.tracers.base import BaseTracer
from langchain.schema import LLMResult
from langchain_core.callbacks import CallbackManager
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk
from langchain_core.tracers import Run

from .langchain_method_interceptor import LangChainMethodInterceptor
from .message import InfoMessage
from .model import ConversationType
from .util import process_nested_input

_logger = logging.getLogger(__name__)
TRACE_LEVEL = 5

# TRACE_LEVEL = logging.DEBUG


# not used, but kept in case we want to quickly test something
# def _intercept_langchain(paig_plugin):
#     # moved the imports here so that this becomes a runtime dependency
#     from langchain.llms.openai import BaseOpenAI
#     from langchain.chains.base import Chain
#
#     intercept_methods(paig_plugin, BaseOpenAI, ['_generate', '_agenerate'], BaseLLMGenerateCallback)
#     intercept_methods(paig_plugin, Chain, ['__call__'], ChainCallCallback)

# set this to True if using newer CallbackManager based approach
_callbackManagerBased = True


def setup_langchain_interceptors(interceptor_list, paig_plugin):
    if _callbackManagerBased:
        langchain_interceptor = LangChainCallbackManagerSetup()
        langchain_interceptor.setup(paig_plugin)
        interceptor_list.append(langchain_interceptor)
    else:
        # older method
        langchain_interceptor = LangChainMethodInterceptor()
        langchain_interceptor.find_all_methods_to_intercept()
        count = langchain_interceptor.setup_interceptors(paig_plugin)
        if _logger.isEnabledFor(logging.INFO):
            _logger.info(InfoMessage.LANGCHAIN_INITIALIZED.format(count=count))
        interceptor_list.append(langchain_interceptor)


class PrivaceraShieldCallback(BaseTracer):
    """Callback for Privacera Shield.
    This is based on the BaseTracer which captures events coming from Langchain library and creates a Run
    object which captures the input and output associated with each event. The Run object is then passed to
    forward. Run object also has tags and meta-data that it can pass from one event to another. The Runs are
    nested so there is a parent_run_id that can be used to trace the lineage of the Run objects.

    One typical RAG application flow results in following events,

    on_chain_start
        on_retriever_start
        on_retriever_end
        on_llm_start
        on_llm_end
    on_chain_end

    Or

    on_chain_start
        on_llm_start - convert question to standalone question
        on_llm_end
        on_retriever_start
        on_retriever_end
        on_llm_start
        on_llm_end
    on_chain_end
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.raise_error = True
        self.paig_plugin = kwargs.get("paig_plugin")

    def print_run(self, event, run: Run, details=True):
        if _logger.isEnabledFor(logging.DEBUG):
            run_dict = run.dict()
            _logger.debug(f'\n{event}: Run name={run.name}, run_type={run.run_type}, id={run.id}')
            if details:
                for k in sorted(run_dict.keys()):
                    v = run_dict[k]
                    _logger.debug(f"  k={k}, v={v}")

    def create_payload(self, event, run: Run):
        payload = dict()
        payload["event"] = event
        payload["id"] = run.id
        payload["name"] = run.name
        payload["run_type"] = run.run_type
        payload["parent_run_id"] = run.parent_run_id
        payload["inputs"] = run.inputs
        payload["outputs"] = run.outputs
        payload["metadata"] = run.tags
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"event={event}, payload={payload}")
        return payload

    def _persist_run(self, run: Run) -> None:
        """Persist a run."""
        # self.print_run("_persist_run", run)
        pass

    def _on_run_create(self, run: Run) -> None:
        """Process a run upon creation."""
        # self.print_run("_on_run_create", run, False)
        pass

    def _on_run_update(self, run: Run) -> None:
        """Process a run upon update."""
        # self.print_run("_on_run_update", run, False)
        pass

    def _on_llm_start(self, run: Run) -> None:
        """Process the LLM Run upon start."""
        self.print_run("_on_llm_start", run)
        payload = self.create_payload("on_llm_start", run)
        response = self.paig_plugin.check_access(text=run.inputs["prompts"],
                                                 conversation_type=ConversationType.ENRICHED_PROMPT,
                                                 thread_id=self.paig_plugin.get_current("thread_id"))  # ENRICHED_PROMPT)
        run.inputs["prompts"] = [response_message.get_response_text() for response_message in response]

    def _on_llm_new_token(
            self,
            run: Run,
            token: str,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]],
    ) -> None:
        """Process new LLM token."""
        self.print_run("_on_llm_new_token, run={self.self.print_run(run)}, token={token}", run)

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> Run:
        # self.print_run("on_llm_end", run)
        # payload = self.create_payload("on_llm_end", run)
        output_list = []
        for generations in response.generations:
            for generation in generations:
                output_list.append(generation.text)

        shield_response = self.paig_plugin.check_access(text=output_list,
                                                        conversation_type=ConversationType.REPLY,
                                                        thread_id=self.paig_plugin.get_current("thread_id"))
        i = 0
        for generations in response.generations:
            for generation in generations:
                generation.text = shield_response[i].get_response_text()
                i += 1

        llm_run = super().on_llm_end(response, run_id=run_id, **kwargs)
        return llm_run

    # def _on_llm_end(self, run: Run) -> None:
    #     """Process the LLM Run."""
    #     self.print_run("_on_llm_end", run)
    #     payload = self.create_payload("on_llm_end", run)
    #     output_list = []
    #     for generations in run.outputs["generations"]:
    #         for generation in generations:
    #             output_list.append(generation["text"])
    #
    #     response = self.paig_plugin.check_access(text=output_list,
    #                                              conversation_type=ConversationType.REPLY,
    #                                              thread_id=self.paig_plugin.get_current("thread_id"))
    #     i = 0
    #     for generations in run.outputs["generations"]:
    #         for generation in generations:
    #             generation["text"] = response[i].get_response_text()
    #             i += 1

    def _on_llm_error(self, run: Run) -> None:
        """Process the LLM Run upon error."""
        self.print_run("_on_llm_error", run)

    def _on_chain_start(self, run: Run) -> None:
        """Process the Chain Run upon start."""
        self.print_run("_on_chain_start", run)

        if "parent_run_id" not in run.__dict__ or not run.__dict__["parent_run_id"]:
            # intercept and possible break the flow
            # raise Exception("in chain start")
            self.create_payload("on_chain_start", run)
            # text = extract_text_from_input(input)
            # text = run.inputs.get("question", run.inputs.get("input"))
            text = []
            process_nested_input(run.inputs, text)
            response_messages = self.paig_plugin.check_access(text=text,
                                                              conversation_type=ConversationType.PROMPT,
                                                              thread_id=self.paig_plugin.get_current("thread_id"))
            # response = shield.process(payload)
            # copy response to run.__dict__["inputs"]
            # run.inputs["question"] = response_messages[0].get_response_text()
            process_nested_input(run.inputs,
                                 [response_message.get_response_text() for response_message in response_messages],
                                 False)
            # print(f"redacted question={run.inputs['question']}")

    def _on_chain_end(self, run: Run) -> None:
        """Process the Chain Run."""
        self.print_run("_on_chain_end", run)

    def _on_chain_error(self, run: Run) -> None:
        """Process the Chain Run upon error."""
        self.print_run("_on_chain_error", run)

    def _on_tool_start(self, run: Run) -> None:
        """Process the Tool Run upon start."""
        self.print_run("_on_tool_start", run)

    def _on_tool_end(self, run: Run) -> None:
        """Process the Tool Run."""
        self.print_run("_on_tool_end", run)

    def _on_tool_error(self, run: Run) -> None:
        """Process the Tool Run upon error."""
        self.print_run("_on_tool_error", run)

    def _on_chat_model_start(self, run: Run) -> None:
        """Process the Chat Model Run upon start."""
        self.print_run("_on_chat_model_start", run)

    def _on_retriever_start(self, run: Run) -> None:
        """Process the Retriever Run upon start."""
        self.print_run("_on_retriever_start", run)

    def _on_retriever_end(self, run: Run) -> None:
        """Process the Retriever Run."""
        self.print_run("_on_retriever_end", run)
        payload = self.create_payload("on_retriever_end", run)
        response = self.paig_plugin.check_access(
            text=[document.page_content for document in run.outputs["documents"]],
            conversation_type=ConversationType.RAG,  # RETRIEVAL)
            thread_id=self.paig_plugin.get_current("thread_id"))
        for document, response_message in zip(run.outputs["documents"], response):
            document.page_content = response_message.get_response_text()

    def _on_retriever_error(self, run: Run) -> None:
        """Process the Retriever Run upon error."""
        self.print_run("_on_retriever_error", run)


class Interceptor:
    def __init__(self, method_name, original_func, *args, **kwargs):
        self.method_name = method_name
        self.original_func = original_func
        self.paig_plugin = kwargs.get("paig_plugin")
        pass

    def __call__(self, *args, **kwargs):
        _logger.debug(f"before calling {self.method_name}, args={args}, kwargs={kwargs}")
        ret = self.original_func(*args, **kwargs)
        if isinstance(ret, CallbackManager):
            if not any(isinstance(handler, PrivaceraShieldCallback) for handler in ret.inheritable_handlers):
                ret.add_handler(PrivaceraShieldCallback(paig_plugin=self.paig_plugin))
                self.paig_plugin.set_current(thread_id=self.paig_plugin.generate_conversation_thread_id())
                _logger.debug("added PrivaceraShieldCallback to CallbackManager")
            else:
                _logger.debug("PrivaceraShieldCallback already exists in CallbackManager")
        _logger.debug(f"after calling {self.method_name}, ret={ret}")
        return ret

    def get_original_func(self):
        return self.original_func


def monkey_patch(cls, method_names, interceptor_cls, *args, **kwargs):
    interceptor_list = []
    for method_name, method in inspect.getmembers(cls, callable):
        _logger.debug(f"method_name={method_name}, method={method}")
        if method_name in method_names:
            interceptor_instance = interceptor_cls(method_name, method, *args, **kwargs)
            setattr(cls, method_name, interceptor_instance)
            _logger.debug(f"have set interceptor on method_name={method_name}, method={method}")
            interceptor_list.append(interceptor_instance)
    return interceptor_list


class LangChainCallbackManagerSetup:
    def __init__(self):
        self.method_list = ['configure']
        self.interceptor_list = []

    def setup(self, paig_plugin):
        self.interceptor_list = monkey_patch(CallbackManager, self.method_list, Interceptor, paig_plugin=paig_plugin)

    def undo_setup_interceptors(self):
        for method, interceptor in zip(self.method_list, self.interceptor_list):
            setattr(CallbackManager, method, interceptor.get_original_func())
