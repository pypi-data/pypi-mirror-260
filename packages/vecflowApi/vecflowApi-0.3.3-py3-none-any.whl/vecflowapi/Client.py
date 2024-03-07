"""
Module for interacting with the VecFlow API. Contains methods for authentication, 
pipeline creation, and API key management.
"""

import json
import requests

from vecflowapi.Pipeline import Pipeline


class Client:
    """
    The :class: Client class is the primary method for authentication and pipeline \
creation with VecFlow. Clients can be created with an existing API key, or can be \
created without one in order to sign-up/login. 

    :return: Usually none, though Class may return a Pipeline object after a \
pipeline has been created.
    :rtype: none, :class: vecflowapi.Pipeline.Pipeline
    \n
    """

    API_URL = "https://vecflow-apis-2147-e82b72a8-4s59j2od.onporter.run"
    # API_URL = "http://127.0.0.1:5001"

    _api_key = None

    def __init__(self, api_key=None):
        self._api_key = api_key

    def _has_api_key(self):
        return self._api_key is not None

    def _login(self, username, password):
        request_json = {"username": username, "password": password}
        response = requests.post(
            self.API_URL + "/users/login", json=request_json, timeout=10
        )
        if response.status_code == 200:
            response_data = response.json()
            return response_data["token"]
        else:
            raise ValueError(
                {
                    "error": "Login failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def signup(self, username, password):
        """
        Input a new username and password to sign up for the API.
        POTENTIALLY TO BE DEPRECATED IN THE FUTURE, PENDING A WEBSITE.

        :param username: The username for the new account.
        :type username: str
        :param password: The password for the new account.
        :type password: str
        \n
        """
        request_json = {"username": username, "password": password}
        response = requests.post(
            self.API_URL + "/users/signup", json=request_json, timeout=10
        )
        if response.status_code == 200:
            print("Success! You have been signed up.")
        else:
            raise ValueError(
                {
                    "error": "Signup failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def generate_api_key(self, username, password):
        """
        Given an existing user, generate an API key attached to the user's \
profile. Note that a user can have more than one API key. Upon completion, \
returns the generated API key.

        :param username: The existing user's username.
        :type username: str
        :param password: The existing user's password.
        :type password: str
        :return: The new API key. 
        :rtype: str
        \n
        """
        jwt_token = self._login(username, password)

        url = self.API_URL + "/api_keys/generate"
        headers = {
            "accept": "application/json",
            "Authorization": jwt_token,
        }
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["api_key"]
        else:
            raise ValueError(
                {
                    "error": "Generating API key failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def list_api_keys(self, username, password):
        """
        This function retrieves a user's API keys using a JWT token for authentication.

        :param username: The `list_api_keys` function you provided is used to retrieve a list of API
        keys for a given user by sending a GET request to the API endpoint. The function takes three
        parameters: `self` (assuming it's a method within a class), `username`, and `password`
        :param password: The `password` parameter in the `list_api_keys` function is used to
        authenticate the user and obtain a JWT token for accessing the API.
        This password is typically
        the user's password for the system or service that requires
        authentication before retrieving the
        API keys. It is passed along with the `username`
        :return: The `list_api_keys` function returns a list of API keys if the HTTP response status
        code is 200. If the status code is not 200, it raises an
        exception with details about the error,
        including the status code and the error message from the response.
        """
        jwt_token = self._login(username, password)

        url = self.API_URL + "/api_keys/"
        headers = {
            "accept": "application/json",
            "Authorization": jwt_token,
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["api_keys"]
        else:
            print(response.json())
            raise ValueError(
                {
                    "error": "Retrieving API keys failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def create_pipeline(
        self,
        name,
        splitter_type="NLTKTextSplitter",
        splitter_args=None,
        embedder_type="OpenAI_003_Small",
        embedder_args=None,
        vector_store_type="PineconeVectorStore",
        vector_store_args=None,
    ):
        """
        The primary function for creating pipelines via the VecFlow API. `create_pipeline`
        takes several
        inputs to create a hosted chunking, embedding, and vector store pipeline for the user.
        :param name: The name of the pipeline. If this matches the name of an existing pipeline, the
        existing pipeline will be overwritten.
        :type name: str
        :param splitter_type: The type of splitter to use for chunking data. Defaults to
        'NLTKTextSplitter'. Available splitters include: 'NLTKTextSplitter'.
        :type splitter_type: str, optional
        :param splitter_args: Arguments for the splitter, varying based on the splitter type.
        For 'NLTKTextSplitter',
        required arguments include 'chunk_size' (int), 'chunk_overlap' (int), and
        'length_function' (str, choices: ['len']).
        :type splitter_args: dict, optional
        :param embedder_type: The type of embedder to use. Options include 'OpenAIEmbedder',
        'OpenAI_003_Large', and 'OpenAI_003_Small'.
        Each embedder has specific requirements for `embedder_args`.
        :type embedder_type: str, optional
        :param embedder_args: Arguments for the embedder, varying based on the embedder type.
        For 'OpenAIEmbedder',
        required arguments include 'api_key' (str).
        :type embedder_args: dict, optional
        :param vector_store_type: The type of vector store to use. Defaults to
        'PineconeVectorStore'.
        Options and required `vector_store_args` are detailed in the API documentation.
        :type vector_store_type: str, optional
        :param vector_store_args: Arguments for the vector store, varying based on the store type.
        For 'PineconeVectorStore',
        required arguments include 'api_key' (str), 'environment' (str), and 'index' (str).
        :type vector_store_args: dict, optional
        :raises PermissionError: Raised if no API key is provided and no login has occurred.
        :return: The pipeline object that was created.
        :rtype: vecflowapi.Pipeline.Pipeline
        \n
        """
        if vector_store_args is None:
            vector_store_args = {
                "api_key": None,
                "environment": "env-name",
                "index": "index-name",
            }
        if embedder_args is None:
            embedder_args = {"api_key": None}
        if splitter_args is None:
            splitter_args = {
                "chunk_size": 200,
                "chunk_overlap": 20,
                "length_function": "len",
            }
        if not self._has_api_key():
            raise PermissionError(
                "API key not provided.\nEither initialize your client with an API key or login "
                "with your username and password."
            )
        # create pipeline (via api)
        req_headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        # Define the endpoint
        endpoint = "/pipelines/create"
        # Define the data to send to the endpoint
        # FIXME: Add some checking here later.
        data = {
            "pipeline_name": name,  # cannot already exist in db
            "splitter": {
                "type": splitter_type,
                "args": splitter_args,
            },
            "embedder": {
                "type": embedder_type,
                "args": embedder_args,
            },
            "vector_store": {
                "type": vector_store_type,
                "args": vector_store_args,
            },
        }
        # Send a POST request to the endpoint
        endpoint = self.API_URL + endpoint
        response = requests.post(
            endpoint, data=json.dumps(data), headers=req_headers, timeout=10
        )

        if response.status_code == 200:
            # create and return pipline
            return Pipeline(name, self._api_key)
        else:
            raise ValueError(
                {
                    "error": "Creation of pipeline failed",
                    "status_code": response.status_code,
                    "response": response.json()["error"]["message"],
                }
            )

    def get_pipeline(self, name):
        """
        Given a pipeline's name, returns the pipeline.

        :param name: The name of the pipeline to be returned.
        :type name: str
        :raises PermissionError: If no API key is provided and no login has occured.
        :return: The existing Pipeline object.
        :rtype: :class: vecflowapi.Pipeline.Pipeline
        \n
        """
        if not self._has_api_key():
            raise ValueError(
                "API key not provided.\nEither initialize your client with an API key "
                "or login with your username and password."
            )

        return Pipeline(name, self._api_key)
