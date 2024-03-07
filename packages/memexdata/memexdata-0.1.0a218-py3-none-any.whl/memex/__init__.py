import io
from typing import Any, BinaryIO, Dict, List
from .types import _udf_payload
import pandas as pd
import requests
import os


class MemexSessionError(Exception):
    """Custom exception for API errors."""

    pass


class MemexSession:
    def __init__(
        self, base_url: str = "http://127.0.0.1:8000", api_key: str = None, verify_ssl: bool = True
    ) -> None:
        """Connect to Memex API at the specified base URL.
        Set the API key for authentication explicitly or via environment variable `MEMEX_API_KEY`.
        Args:
            base_url (str, optional): The base URL of the Memex API. Defaults to "http://127.0.0.1:8000".
            api_key (str, optional): The API key to use for authentication. Defaults to None.
            verify_ssl (bool, optional): Whether to verify the SSL certificate. Defaults to True.
        """
        self.base_url = base_url
        self.verify_ssl = verify_ssl
        self.api_key = api_key or os.getenv("MEMEX_API_KEY")
        if self.api_key is None:
            raise MemexSessionError(
                "No API key provided and MEMEX_API_KEY environment variable not set."
            )

    def headers(self) -> Dict[str, str]:
        """Returns the headers to use for API requests."""
        return {"Authorization": f"Bearer {self.api_key}"}

    def _handle_response(self, response: requests.Response, as_csv: bool = False) -> Any:
        """
        Handles the HTTP response, raising an error if it's not successful.

        Args:
            response (requests.Response): The response object to handle.

        Returns:
            Any: The JSON content from the response, if successful.
        """
        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            # Attempt to provide a JSON-based error message if one can be parsed
            try:
                error_data = response.json()
                error_message = error_data.get("detail", str(error_data))
            except ValueError:  # JSON response could not be decoded
                error_message = str(http_err)

            raise MemexSessionError(f"API request unsuccessful: {error_message}") from http_err

        if as_csv:
            content_type = response.headers.get("Content-Type")
            if "text/csv" in content_type:
                return pd.read_csv(io.StringIO(response.content.decode()))
            else:
                return response.json()
        else:
            return response.json()

    def list_datasets(self) -> List[Dict[str, Any]]:
        """Fetches available datasets."""
        response = requests.get(
            f"{self.base_url}/api/datasets", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_prompt_as_function(
        self, name: str, prompt: str, variables: List[str], overwrite: bool = False
    ) -> Dict[str, Any]:
        """Saves a prompt as a function."""
        function_data = {"name": name, "content": prompt, "variables": variables}
        function_param = {"function": function_data, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/functions",
            json=function_param,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def query(self, query: str, **kwargs) -> pd.DataFrame:
        """Execute a SQL query and return the results as a pandas DataFrame."""
        query_data = {"query": query, **kwargs}
        response = requests.post(
            f"{self.base_url}/api/query",
            json=query_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        json_response = self._handle_response(response)

        # Check if the response has the expected data key.
        if "data" not in json_response:
            raise MemexSessionError("Query response did not contain 'data'")

        # Convert the JSON response to a pandas DataFrame
        return pd.DataFrame(json_response["data"])

    def upload_dataset(self, file: BinaryIO, file_name: str) -> Dict[str, Any]:
        """Uploads a dataset."""
        files = {"file": (file_name, file)}
        response = requests.put(
            f"{self.base_url}/api/datasets/upload",
            files=files,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def download_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Download a dataset in CSV format.
        Returns:
            pd.DataFrame: The dataset as a pandas DataFrame.
        """
        response = requests.get(
            f"{self.base_url}/api/datasets/download/{dataset_name}",
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response, as_csv=True)

    def get_models(self) -> List[Dict[str, Any]]:
        """Retrieves the list of available models."""
        response = requests.get(
            f"{self.base_url}/api/models", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def llm(self, prompts: list[str], model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """Invokes an LLM with a specified prompt."""
        prompt_data = {"items": prompts, "model": model}
        response = requests.post(
            f"{self.base_url}/api/llm",
            json=prompt_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def update_function(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a function with new details."""
        response = requests.put(
            f"{self.base_url}/api/functions",
            json=function_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def save_function(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a new function."""
        response = requests.post(
            f"{self.base_url}/api/functions",
            json=function_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def get_function(self, name: str) -> Dict[str, Any]:
        """Fetches a function with the given name."""
        response = requests.get(
            f"{self.base_url}/api/functions/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_as_table(self, name: str, query: str, *, overwrite=False, **kwargs) -> Dict[str, Any]:
        """Saves a query as a table with a specified name.
        Args:
            name (str): The name of the table.
            query (str): The SQL query to save as a table.
            overwrite (bool, optional): Whether to overwrite an existing table with the same name. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the query.
        Kwargs:
            max_tokens (int, optional): The maximum number of tokens to generate.
            temperature (float, optional): The temperature for generation
            use_cache (bool, optional): Whether to use the cache for the query
        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        payload = {"name": name, "query": {"query": query, **kwargs}, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/tables",
            json=payload,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def delete_table(self, table_name: str) -> Dict[str, Any]:
        """Deletes a table with the given reference."""
        response = requests.delete(
            f"{self.base_url}/api/tables",
            json=dict(name=table_name),
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def list_queries(self) -> List[Dict[str, Any]]:
        """Lists all saved queries."""
        response = requests.get(
            f"{self.base_url}/api/queries", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def get_query(self, name: str) -> Dict[str, Any]:
        """Fetches a query with the given name."""
        response = requests.get(
            f"{self.base_url}/api/queries/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_query(self, name: str, query: str, overwrite: bool = False) -> Dict[str, Any]:
        """Saves a query with a specified name."""
        payload = {"name": name, "query": query, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/queries",
            json=payload,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def delete_query(self, name: str) -> Dict[str, Any]:
        """Deletes a query with the given name."""
        response = requests.delete(
            f"{self.base_url}/api/queries/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_label(self, label_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves label data for a dataset."""
        response = requests.post(
            f"{self.base_url}/api/labels/items",
            json=label_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def create_label_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a label session for labeling tasks."""
        response = requests.post(
            f"{self.base_url}/api/labels",
            json=session_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def delete_label_session(self, session_reference: Dict[str, str]) -> Dict[str, Any]:
        """Deletes a label session with the given reference."""
        response = requests.delete(
            f"{self.base_url}/api/labels",
            json=session_reference,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def list_functions(self) -> List[Dict[str, Any]]:
        """Lists all available functions."""
        response = requests.get(
            f"{self.base_url}/api/functions", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def udf(self, func=None, *, prompt=False, resources=None, remote=False):
        """
        Decorator that registers a function as a User-Defined Function (UDF) for use within Memex SQL queries.

        This decorator is intended to be used on functions to either register them as native Python functions or as LLM
        prompt functions for execution within Memex SQL.

        Parameters
        ----------
        - func (callable): The function to register as a UDF.
        - prompt (bool, optional): If True, the function is registered as an LLM prompt function, using its docstring as the prompt. Defaults to False.
        - session (MemexSession, optional): The session instance for registration. Defaults to a new MemexSession instance.
        - resources (any, optional): Additional resources required by the UDF. Defaults to None. Any resources specified will be stored and make available to the UDF at runtime. Resources are only applicable to Python native functions.
        - remote (bool, optional): If True, indicates the UDF should be executed remotely. Defaults to False.

        Behavior
        --------
        - When `prompt` is True, the decorated function's body is ignored, and its docstring is used as the prompt for LLM, with parameters as template variables. The return type is inferred from the LLM response.
        - When `prompt` is False, the function is registered as a native Python function. It must be a pure function and can only use the Python standard library.

        Example usage
        -------------
        - A prompt function:
        ```
        @mx.prompt
        def joke(about:str) -> str:
            "Tell me a joke about {about}"
        ```

        - A native Python function:
        ```
        @mx.udf
        def is_anagram(a:str, b:str) -> bool:
            return sorted(a) == sorted(b)
        ```
        """
        return _udf(func, prompt=prompt, session=self, resources=resources, remote=remote)

    def prompt(self, func=None):
        """Decorator that registers a function as a prompt for use within Memex SQL queries.
        See the `udf` decorator for more details.
        """
        return _udf(func, prompt=True, session=self)


def _udf(func=None, *, prompt=False, session=None, resources=None, remote=False):
    # this is to allow for both @udf and @udf()
    if func is None:
        return lambda f: _udf(f, prompt=prompt, session=session, resources=resources, remote=remote)

    payload = _udf_payload(func, prompt, resources, remote)

    session.update_function(payload)

    return func


def make_resources(resources: dict[str, str]):
    """Wrap a dictionary of resources to make it available to the Python UDF in Memex.
    For example:
    ```
    resources = make_resources({"my_resource": "path/to/my/resource"})

    @mx.udf(resources=resources)
    def my_udf():
        resource = resources("my_resource")
        ...
    ```
    The `resources` will be made available to the Python function local scope at runtime under the name `__resources`.
    """
    return resources


__all__ = [MemexSession, make_resources]
