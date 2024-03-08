"""This module contains the TakeoffClient class, which is used to interact with the Takeoff server."""

# ────────────────────────────────────────────────────── Import ────────────────────────────────────────────────────── #
import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

import requests
from sseclient import Event, SSEClient
from takeoff_config import ReaderConfig

from .exceptions import TakeoffError

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Takeoff Client                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class TakeoffClient:
    def __init__(self, base_url: str = "http://localhost", port: int = 3000, mgmt_port: int = None):
        """TakeoffClient is used to interact with the Takeoff server.

        Args:
            base_url (str, optional): base url that takeoff server runs on. Defaults to "http://localhost".
            port (int, optional): port that main server runs on. Defaults to 8000.
            mgmt_port (int, optional): port that management api runs on. Usually be `port + 1`. Defaults to None.
        """
        self.base_url = base_url  # "http://localhost"
        self.port = port  # 8000

        if mgmt_port is None:
            self.mgmt_port = port + 1  # 8001
        else:
            self.mgmt_port = mgmt_port

        self.url = f"{self.base_url}:{self.port}"  # "http://localhost:3000"
        self.mgmt_url = f"{self.base_url}:{self.mgmt_port}"  # "http://localhost:3001"

    def get_readers(self) -> dict:
        """Get a list of information about all readers.

        Returns:
            dict: List of information about all readers.
        """
        response = requests.get(self.mgmt_url + "/reader_groups")
        return response.json()

    def embed(self, text: Union[str, List[str]], consumer_group: str = "primary") -> dict:
        """Embed a batch of text.

        Args:
            text (str | List[str]): Text to embed.
            consumer_group (str, optional): consumer group to use. Defaults to "primary".

        Returns:
            dict: Embedding response.
        """
        response = requests.post(self.url + "/embed", json={"text": text, "consumer_group": consumer_group})

        if response.status_code != 200:
            raise TakeoffError(
                status_code=response.status_code,
                message=f"Embedding failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )

        return response.json()

    def classify(self, text: Union[str, List[str], List[List[str]]], consumer_group: str = "classify") -> dict:
        """Classify a batch of text.

        Text that is passed in as a list of list of strings will be concatenated on the
        innermost list, and the outermost list treated as a batch of concatenated strings.

        Concatenation happens server-side, as it needs information from the model tokenizer.

        Args:
            text (str | List[str] | List[List[str]]): Text to classify.
            consumer_group (str, optional): consumer group to use. Defaults to "classify".

        Returns:
            dict: Classification response.
        """

        response = requests.post(self.url + "/classify", json={"text": text, "consumer_group": consumer_group})
        if response.status_code != 200:
            raise Exception(
                f"Classification failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}"
            )

        return response.json()

    def generate(
        self,
        text: Union[str, List[str]],
        sampling_temperature: float = None,
        sampling_topp: float = None,
        sampling_topk: int = None,
        repetition_penalty: float = None,
        no_repeat_ngram_size: int = None,
        max_new_tokens: int = None,
        min_new_tokens: int = None,
        regex_string: str = None,
        json_schema: Any = None,
        prompt_max_tokens: int = None,
        consumer_group: str = "primary",
        image_path: Optional[Path] = None,
    ) -> dict:
        """Generates text, seeking a completion for the input prompt. Buffers output and returns at once.

        Args:
            text (str): Input prompt from which to generate
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.

        Returns:
            Output (dict): The response from Takeoff containing the generated text as a whole.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }

        if image_path is not None:
            with open(image_path, "rb") as f:
                # The payload needs to be converted to a string and then wrapped in a tuple with the content type
                files = {
                    # The 'json_data' is part of the multipart form data, with a content type of application/json
                    "json_data": (None, json.dumps(json_data), "application/json"),
                    # The image is sent as a file with the key 'image_data'
                    "image_data": (None, f, "image/*"),
                }

                response = requests.post(self.url + "/image_generate", files=files)
        else:
            response = requests.post(
                url=self.url + "/generate",
                json=json_data,
                stream=True,
            )

        if response.status_code != 200:
            raise TakeoffError(
                status_code=response.status_code,
                message=f"Generation failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )

        return response.json()

    def generate_stream(
        self,
        text: Union[str, List[str]],
        sampling_temperature: float = None,
        sampling_topp: float = None,
        sampling_topk: int = None,
        repetition_penalty: float = None,
        no_repeat_ngram_size: int = None,
        max_new_tokens: int = None,
        min_new_tokens: int = None,
        regex_string: str = None,
        json_schema: dict = None,
        prompt_max_tokens: int = None,
        consumer_group: str = "primary",
        image_path: Optional[Path] = None,
    ) -> Iterator[Event]:
        """Generates text, seeking a completion for the input prompt.

        Args:
            text (str | List[str]): Input prompt from which to generate
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.


        Returns:
            Iterator[sseclient.SSEClient.Event]: An iterator of server-sent events.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }
        if image_path is not None:
            with open(image_path, "rb") as f:
                # The payload needs to be converted to a string and then wrapped in a tuple with the content type
                files = {
                    # The 'json_data' is part of the multipart form data, with a content type of application/json
                    "json_data": (None, json.dumps(json_data), "application/json"),
                    # The image is sent as a file with the key 'image_data'
                    "image_data": (None, f, "image/*"),
                }

                response = requests.post(self.url + "/image_generate", files=files)
        else:
            response = requests.post(
                url=self.url + "/generate_stream",
                json=json_data,
                stream=True,
            )
        if response.status_code != 200:
            raise TakeoffError(
                status_code=response.status_code,
                message=f"Generation failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )

        # return a python generator
        return SSEClient(response).events()

    def tokenize(self, text: str, reader_id: str) -> List[str]:
        """Tokenize a single text item.

        The tokenize endpoint can be used to send a string to a models tokenizer for tokenization.
        The result is a list of tokens. For example, if "my_reader" is the id of a model that uses a Llama tokenizer,
        The following code will tokenize the string "hello, world" using the Llama tokenizer:

        >>> takeoff_client.tokenize("hello, world", reader_id="my_reader")
        ... ['▁hello', ',', '▁world']

        NOTE: The `reader_id` parameter is not the same as the `consumer_group` parameter used in other endpoints.
        Because tokenization is specific to a specific loaded model, we need to specify a unique id that identifies
        a particular reader. To find this ID for the models currently loaded into your takeoff server, try the following

        >>> readers = takeoff_client.get_readers()
        >>> for reader_group in readers.values():
        >>>    for reader in reader_group:
        >>>       print(reader["reader_id"])

        Args:
            text (str): Text to tokenize.
            reader_id (str): The id of the reader to use.

        Returns:
            List[str]: Tokenized text.
        """
        response = requests.post(self.url + f"/tokenize/{reader_id}", json={"text": text})
        if response.status_code != 200:
            raise TakeoffError(
                response.status_code,
                f"Tokenization failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )
        if "tokens" not in response.json():
            raise TakeoffError(400, "Tokenization failed\nResponse: " + response.text)
        else:
            return response.json()["tokens"]

    def create_reader(self, reader_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reader.

        Args:
            reader_config (Dict[str, Any]): Dict containing all the reader configuration parameters.
        """
        try:
            reader = ReaderConfig(**reader_config)
        except Exception as e:
            raise TakeoffError(400, f"Reader creation failed\nError: {str(e)}")

        response = requests.post(self.mgmt_url + "/reader", json=reader.dict_without_optionals())
        if response.status_code != 201:
            raise TakeoffError(
                response.status_code,
                f"Reader creation failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )
        return response.json()

    def delete_reader(self, reader_id: str) -> None:
        """Delete a reader, using their reader_id.

        Args:
            reader_id (str): Reader id.
        """
        response = requests.delete(self.mgmt_url + f"/reader/{reader_id}")
        if response.status_code != 204:
            raise TakeoffError(
                response.status_code,
                f"Reader deletion failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )

    def list_all_readers(self) -> Dict[str, Dict[str, Any]]:
        """List all readers, ordering by consumer group.

        Returns:
            Dict[str, Dict[str, Any]]: List of reader ids.
        """
        response = requests.get(self.mgmt_url + "/reader_groups")
        if response.status_code != 200:
            raise TakeoffError(
                response.status_code,
                f"Reader listing failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )
        return response.json()

    def get_reader_config(self, reader_id: str) -> Dict[str, Any]:
        """Get the config.json that a reader is running.

        Args:
            reader_id (str): Reader id.

        Returns:
            Dict[str, Any]: Reader configuration.
        """
        response = requests.get(self.mgmt_url + f"/config/{reader_id}")
        if response.status_code != 200:
            raise TakeoffError(
                response.status_code,
                f"Reader config retrieval failed\nStatus code: {str(response.status_code)}\nResponse: {response.text}",
            )
        return response.json()


if __name__ == "__main__":
    pass
