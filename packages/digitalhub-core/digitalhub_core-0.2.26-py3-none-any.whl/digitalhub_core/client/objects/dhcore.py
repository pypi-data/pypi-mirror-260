"""
DHCore Client module.
"""
from __future__ import annotations

import os
from typing import Literal

import requests
from digitalhub_core.client.objects.base import Client
from digitalhub_core.utils.exceptions import BackendError
from pydantic import BaseModel


class AuthConfig(BaseModel):
    """Client configuration model."""

    auth_type: Literal["basic", "token"]


class OAuth2TokenAuth(AuthConfig):
    """OAuth2 token authentication model."""

    token: str
    """OAuth2 token."""


class BasicAuth(AuthConfig):
    """Basic authentication model."""

    username: str
    """Basic authentication username."""
    password: str
    """Basic authentication password."""


class ClientDHCore(Client):
    """
    DHCore client.

    The DHCore client is used to communicate with the Digitalhub Core backendAPI via REST.
    At creation, the client trys to get the endpoint and authentication parameters
    from the environment variables. In case the endpoint is not set, it raises an exception.
    """

    def __init__(self, config: dict = None) -> None:
        """
        Constructor.
        """
        super().__init__()

        self._endpoint = None
        self._auth_type = None
        self._auth_params = None
        self._set_connection(config)

    def create_object(self, obj: dict, api: str) -> dict:
        """
        Create an object.

        Parameters
        ----------
        obj : dict
            The object to create.
        api : str
            The api to create the object with.

        Returns
        -------
        dict
            The created object.
        """
        return self._call("POST", api, json=obj)

    def read_object(self, api: str) -> dict:
        """
        Get an object.

        Parameters
        ----------
        api : str
            The api to get the object with.

        Returns
        -------
        dict
            The object.
        """
        return self._call("GET", api)

    def update_object(self, obj: dict, api: str) -> dict:
        """
        Update an object.

        Parameters
        ----------
        obj : dict
            The object to update.
        api : str
            The api to update the object with.

        Returns
        -------
        dict
            The updated object.
        """
        return self._call("PUT", api, json=obj)

    def delete_object(self, api: str) -> dict:
        """
        Delete an object.

        Parameters
        ----------
        api : str
            The api to delete the object with.

        Returns
        -------
        dict
            A generic dictionary.
        """
        resp = self._call("DELETE", api)
        if isinstance(resp, bool):
            resp = {"deleted": resp}
        return resp

    def _call(self, call_type: str, api: str, **kwargs) -> dict:
        """
        Make a call to the DHCore API.
        Keyword arguments are passed to the session.request function.

        Parameters
        ----------
        call_type : str
            The type of call to make.
        api : str
            The api to call.
        **kwargs
            Keyword arguments.

        Returns
        -------
        dict
            The response object.
        """
        url = self._endpoint + api

        # Choose auth type
        if self._auth_type == "basic":
            kwargs["auth"] = self._auth_params
        elif self._auth_type == "token":
            kwargs["headers"] = {"Authorization": f"Bearer {self._auth_params}"}

        # Call
        response = None
        try:
            response = requests.request(call_type, url, timeout=60, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.Timeout):
                msg = "Request to DHCore backend timed out."
            elif isinstance(e, requests.exceptions.ConnectionError):
                msg = "Unable to connect to DHCore backend."
            elif isinstance(e, requests.exceptions.JSONDecodeError):
                return {}
            else:
                msg = f"Backend error: {e}"
            raise BackendError(msg) from e

    ################################
    # Env methods
    ################################

    def _set_connection(self, config: dict = None) -> None:
        """
        Function to set environment variables for DHub Core config.

        Parameters
        ----------
        config : ClientConfig
            The client config.

        Returns
        -------
        None
        """

        # Get endpoint at the beginning
        self._endpoint = self._get_endpoint()

        # Evaluate configuration authentication parameters
        if config is not None:
            auth_type = config.get("auth_type")

            # Validate configuration against pydantic model
            if auth_type == "token":
                config = OAuth2TokenAuth(**config)
                self._auth_params = config.token
            elif auth_type == "basic":
                config = BasicAuth(**config)
                self._auth_params = (config.username, config.password)

            self._auth_type = auth_type
            return

        # Otherwise, use environment variables
        self._auth_params = self._get_auth()
        if isinstance(self._auth_params, tuple):
            self._auth_type = "basic"
        if isinstance(self._auth_params, str):
            self._auth_type = "token"
        return

    @staticmethod
    def _get_endpoint() -> str:
        """
        Get DHub Core endpoint environment variables.

        Returns
        -------
        str
            DHub Core endpoint environment variables.

        Raises
        ------
        Exception
            If the endpoint of DHCore is not set in the env variables.
        """
        endpoint = os.getenv("DIGITALHUB_CORE_ENDPOINT")
        if endpoint is None:
            raise BackendError("Endpoint not set as environment variables.")

        # Sanitize endpoint string
        return endpoint.removesuffix("/")

    @staticmethod
    def _get_auth() -> str | tuple[str, str] | None:
        """
        Get authentication parameters from the config.

        Returns
        -------
        tuple[str, str], str, None
            The authentication parameters.
        """
        token = os.getenv("DIGITALHUB_CORE_TOKEN")
        if token is not None:
            return token

        user = os.getenv("DIGITALHUB_CORE_USER")
        password = os.getenv("DIGITALHUB_CORE_PASSWORD")
        if user is not None and password is not None:
            return user, password

    @staticmethod
    def is_local() -> bool:
        """
        Declare if Client is local.

        Returns
        -------
        bool
            False
        """
        return False
