"""
Here are a few examples of building with Orca.
"""

from threading import Thread
from typing import Any, Optional

import torch
from orcalib.database import OrcaDatabase
from orcalib.hf_utils import OrcaGroundingProcessor
from orcalib.orca_types import TextT
from orcalib.torch import (
    OrcaGenericLookupLayer,
    OrcaLookupConfig,
    OrcaLookupType,
    OrcaModel,
    OrcaModule,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LogitsProcessorList,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    TextIteratorStreamer,
)

orca_llama_system_prompt = """You are a helpful and direct assistant.
You should try to be as direct and succinct as possible.
You will be provided with context to help answer user queries.
Some of the context may or may not be useful.
If it is, be as true to the context as possible, with priority in order of the context.
If it is not, say you cannot answer or do not know.
DO NOT MENTION THE CONTEXT OR TALK ABOUT UNRELATED ENTITIES IN THE CONTEXT.
Potentially useful context:"""


class OrcaChat(OrcaModule):
    """
    A basic wrapper for a chatbot model that uses Orca for memory retrieval,
    and a base model with a generate method for response generation.
    """

    def __init__(
        self,
        orca_lookup_config: OrcaLookupConfig,
        model: str | PreTrainedModel | torch.nn.Module = "facebook/opt-350m",
        model_id: str = "orca_public_chatbot_v0",
        mode: str = "chat",
        rag: bool = False,
        ground: bool = False,
        max_context_length: int = 4096,
        tokenizer=None,
        **kwargs,
    ):
        super().__init__()

        self.rag = rag
        self.ground = ground

        if isinstance(model, str):
            self.model = AutoModelForCausalLM.from_pretrained(model, **kwargs)
            self.tokenizer = AutoTokenizer.from_pretrained(
                model,
                use_default_system_prompt=True if not rag else False,
                **kwargs,
            )

        elif isinstance(model, PreTrainedModel) or isinstance(model, torch.nn.Module):
            assert hasattr(model, "generate")
            assert isinstance(tokenizer, PreTrainedTokenizerBase)
            self.tokenizer = tokenizer
            self.model = model

        self.lookup_type = OrcaLookupType(
            index_type=TextT,
            return_column_types=[TextT, TextT],
        )

        self.lookup = OrcaModel(orca_lookup_config.orca_db_instance)(OrcaGenericLookupLayer)(
            orca_lookup_type=self.lookup_type,
            orca_lookup_config=orca_lookup_config,
        )

        self.streamer = TextIteratorStreamer(
            tokenizer=self.tokenizer,  # type: ignore
            skip_special_tokens=True,
            skip_prompt=True,
            timeout=15.0,
        )

        self.model_id = model_id
        self.mode = mode
        if self.rag:
            self.chat_history = [
                {
                    "role": "system",
                    "content": orca_llama_system_prompt,
                }
            ]
        else:
            self.chat_history = []
        self.ui_history = []
        self.lookup_history = []
        self.last_user_input = None
        self.max_context_length = max_context_length
        self.last_retrieval_query = None
        self.last_model_input = None
        self.last_accessed_memories: Optional[list[list[Any]]] = None
        self.text_memories: list[list[str]] = []
        self.sim_weight = 0.0
        self.bag_weight = 0.0

    def enable_curate(self) -> None:
        """
        This is temporary until the workflow for attaching orca and curate to models is changed here.
        This will likely change based on how we decide the interface for swapping/attaching databases,
        indices, and columns looks.
        """
        self.lookup.init_curate(
            model_id=self.model_id, model_version="0.0.1", extra_tags=["from_chatbot_demo"], batch_size=1
        )
        self.lookup.enable_curate()

    def determine_retrieval_query(self) -> str:
        """
        Determine the retrieval query based on the last user input
        and other context.

        Currently, this just combines all user inputs into a single query.
        """
        return " ".join([obj["content"] if obj["role"] == "user" else "" for obj in self.chat_history])

    def prep_next_gen(self, last_user_input: str) -> tuple[str, list[list[str]], Optional[list[list[Any]]]]:
        """
        Prepares the next generation by updating the chat history and last user input.
        """
        if self.mode == "StatelessQA":
            self.clear_chat()

        self.last_user_input = last_user_input
        self.chat_history.append({"role": "user", "content": last_user_input})
        self.ui_history.append([last_user_input, None])

        retrieval_query = self.determine_retrieval_query()
        context = self.retrieve(retrieval_query)

        # modify the system prompt with new memories
        if self.rag:
            self.chat_history[0] = {
                "role": "system",
                "content": orca_llama_system_prompt + self.format_context(context) + "\n",
            }

        self.last_retrieval_query = retrieval_query

        return "", self.ui_history, self.last_accessed_memories

    def retrieve(self, query: str) -> list[str]:
        """
        Do the retrieval of memories from the orca database.
        """

        # HACK-y, TODO Fix this
        self._batch_size = 1
        self.lookup._batch_size = 1  # type: ignore

        payload = self.lookup([query])[0]
        memory_texts = []
        for doc in payload:
            # the first element is the vector, the second is the meta
            memory_texts.append(doc[1])

        self.last_accessed_memories = payload
        self.text_memories = memory_texts
        self.lookup_history.append(memory_texts)

        return memory_texts

    def gen_response(self, ui_history):
        if self.mode == "chat":
            formatted_query = self.tokenizer.apply_chat_template(self.chat_history, tokenize=False)
        elif self.mode == "StatelessQA":
            formatted_query = self.tokenizer.apply_chat_template(self.chat_history, tokenize=False)
        else:
            raise NotImplementedError(f"Mode {self.mode} not supported by OrcaChat.gen_response()")

        self.last_model_input = formatted_query
        input_ids = self.tokenizer(formatted_query, return_tensors="pt", max_length=self.max_context_length).to(  # type: ignore
            self.model.device
        )

        grounding_processor = OrcaGroundingProcessor(
            memories=self.text_memories,
            tokenizer=self.tokenizer,
            sim_weight=self.sim_weight,
            bag_weight=self.bag_weight,
        )

        postproc_list = LogitsProcessorList([grounding_processor])

        def gen_then_ack():
            self.model.generate(
                **input_ids,  # type: ignore
                max_length=self.max_context_length,
                num_return_sequences=1,
                streamer=self.streamer,
                logits_processor=postproc_list,
            )

        t1 = Thread(target=gen_then_ack)
        t1.start()

        gen_text_stream = ""
        for next_tok in self.streamer:
            gen_text_stream += next_tok
            self.ui_history[-1][1] = gen_text_stream
            yield self.ui_history

        self.chat_history.append(
            {
                "role": "assistant",
                "content": gen_text_stream,
            }
        )

        self.lookup.record_model_input_output(*self.ui_history[-1])

    def clear_chat(self) -> None:
        """
        This clears all histories.
        """
        self.lookup_history = []
        if self.rag:
            self.chat_history = [
                {
                    "role": "system",
                    "content": None,
                }
            ]
        else:
            self.chat_history = []
        self.ui_history = []

    def format_context(self, memories: list[str]) -> str:
        """
        String format memories for prompt injection to model
        """
        context = ""
        for i, memory in enumerate(memories):
            context += f"\n\n{i + 1}. {memory}"

        return context

    def update_grounding_params(self, sim_weight: float, bag_weight: float) -> None:
        """
        Update the grounding parameters for the OrcaGroundingProcessor.
        """
        self.sim_weight = sim_weight
        self.bag_weight = bag_weight

    def switch_config(self, new_config: OrcaLookupConfig) -> None:
        """
        Switch the OrcaLookupConfig for the OrcaChat instance,
        clearing the chat history.
        """
        self.lookup.set_lookup_config(new_config)
        self.clear_chat()

    def print_chat_log(self) -> None:
        """
        Print the chat log to whatever/wherever the stdout is.
        """
        print("*" * 80)
        print("*" * 30 + "Last Input to Model:" + "*" * 30)
        print(self.last_model_input)
        print("*" * 30 + "I/O to GR Interface:" + "*" * 30)
        print(self.ui_history)
        print("*" * 80)
        print("*" * 30 + "Last Query for Orca:" + "*" * 30)
        print(self.last_retrieval_query)
        print("*" * 80)
