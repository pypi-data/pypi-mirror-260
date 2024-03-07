"""
Module for interacting with an API using Pipeline class.
"""

import os
import json
import requests
from werkzeug.utils import secure_filename


class Pipeline:
    """
    Pipeline class represents a pipeline for interacting with an API.

    Attributes:
        API_URL (str): The base URL of the API.
    """

    # API_URL = "https://vecflow-apis-2147-e82b72a8-4s59j2od.onporter.run"
    API_URL = "http://127.0.0.1:5001"
    UPLOAD_ENDPOINT = "/files/upload"
    QUERY_ENDPOINT = "/query/completion"

    def __init__(self, name, api_key):
        self.name = name
        self._api_key = api_key

    # must use full path for uploading file
    def upload(self, file_path):
        """
        The `upload` function uploads a file to an API endpoint using the provided
        API key and returns the response.

        :param file_path: The `file_path` parameter is the path to the file that you want to upload.
        It should be a string representing the file's location on your local machine
        :return: a dictionary containing the response from the API endpoint. If the upload is
        successful, it returns the JSON response from the API. If there is an error, it raises an
        exception with an error message, status code, and the error message from the API response.
        """
        req_headers = {"Authorization": self._api_key}
        # Check if file exists
        if not os.path.exists(file_path):
            raise ValueError(
                {
                    "error": "Upload failed",
                    "response": "file not found at path provided",
                }
            )

        # Open the file in binary mode for uploading
        with open(file_path, "rb") as file:
            files = {
                "file": (secure_filename(os.path.basename(file_path)), file),
            }
            data = {
                "pipeline_name": self.name,
            }

            # Send a POST request to the endpoint
            try:
                response = requests.post(
                    self.API_URL + self.UPLOAD_ENDPOINT,
                    files=files,
                    data=data,
                    headers=req_headers,
                    timeout=10,
                )
            except requests.RequestException as e:
                return {"error": str(e)}

        # Check response status and handle appropriately
        if response.status_code == 200:
            return response.json()  # Assuming the successful response is JSON
        else:
            raise ValueError(
                {
                    "error": "Upload failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def query(
        self,
        query,
        retrieval_method,
        llm_config,
        history=None,
        prompt=None,
        stream=False,
        file_ids=None,
        kwargs={},
    ):
        """
        The function `query` sends a POST request with specified data to an API endpoint and
        returns the JSON response if successful, otherwise raises an exception with error details.

        :param query: The `query` parameter in the `query` method represents the text query that you
        want to send to the API for processing and retrieval of information. It is the actual query
        string that you want the API to act upon
        :param retrieval_method: The `retrieval_method` parameter in the `query` method
        specifies the method to be used for retrieving information based on the query provided.
        It is a key parameter that determines how the system will search and retrieve
        relevant data based on the input query. The method specified here will impact the
        results returned
        :param llm_config: The `llm_config` parameter in the `query` method is used to specify the
        configuration settings for the language model that will be used for processing the query.
        This configuration could include parameters such as model type, model size, temperature,
        top_k, top_p, etc., depending on the specific
        :param history: The `history` parameter in the `query` method is used to store a list of
        previous queries or interactions. It is an optional parameter that defaults to an empty list
        if not provided when calling the method. This allows you to pass a list of historical
        interactions to provide context for the current query being
        :param prompt: The `prompt` parameter in the `query` function is used to provide additional
        context or information to the model when generating a response based on the query. It can
        be a text prompt that helps guide the model in understanding the query better and generating
        a more relevant response.
        :param stream: The `stream` parameter is a boolean which tells the LLM whether to stream
        your response. It defaults to false.
        :return: The `query` method returns the JSON response if the status code of the HTTP
        response is 200 (indicating success). If the status code is not 200, it raises an
        Exception with details about the error, including the status code and the error
        message from the response JSON.
        """
        if history is None:
            history = []

        if file_ids is None:
            file_ids = []

        req_headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }

        data = {
            "pipeline_name": self.name,
            "query": query,
            "llm_config": llm_config,
            "retrieval_method": retrieval_method,
            "history": history,
            "prompt": prompt,
            "file_ids": file_ids,
            "stream": stream,
            "kwargs": kwargs,
        }

        response = requests.post(
            self.API_URL + self.QUERY_ENDPOINT,
            json=data,
            headers=req_headers,
            timeout=30,
            stream=stream,  # Ensure the 'stream' parameter is correctly passed to requests.post
        )

        if response.status_code == 200:
            if stream:
                # Return a generator if streaming is enabled
                return (line.decode("utf-8") + "\n" for line in response.iter_lines() if line)
            else:
                # Return the full JSON response if streaming is not enabled
                return response.json()
        else:
            raise ValueError(
                {
                    "error": "Query failed",
                    "status_code": response.status_code,
                    "response": response,
                }
            )
