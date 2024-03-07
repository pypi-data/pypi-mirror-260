"""Defines the Fixpoint client, which is the main interface for the SDK."""

import typing

from openai import OpenAI
from openai.types.chat import ChatCompletion

from .lib.env import get_fixpoint_api_key, get_api_base_url
from .lib.requests import Requester
from .lib.debugging import dprint
from . import types


class FixpointClient:
    """The FixpointClient lets you interact with the Fixpoint API."""

    def __init__(
        self,
        *args: typing.Any,
        fixpoint_api_key: typing.Optional[str] = None,
        openai_api_key: typing.Optional[str] = None,
        api_base_url: typing.Optional[str] = None,
        **kwargs: typing.Any,
    ):
        # Check that the environment variable FIXPOINT_API_KEY is set
        _api_key = get_fixpoint_api_key(fixpoint_api_key)

        self._api_key = _api_key
        self._requester = Requester(self._api_key, get_api_base_url(api_base_url))
        if openai_api_key:
            kwargs = dict(kwargs, api_key=openai_api_key)
        self.client = OpenAI(*args, **kwargs)
        self.chat = self._Chat(self._requester, self.client)
        self.fixpoint = self._Fixpoint(self._requester)

    class _Fixpoint:
        def __init__(self, requester: Requester):
            self.user_feedback = self._UserFeedback(requester)
            self.attributes = self._Attributes(requester)

        class _UserFeedback:
            def __init__(self, requester: Requester):
                self._requester = requester

            def create(
                self, request: types.CreateUserFeedbackRequest
            ) -> types.CreateUserFeedbackResponse:
                """Attach user feedback to an LLM log."""
                return self._requester.create_user_feedback(request)

        class _Attributes:
            def __init__(self, requester: Requester):
                self._requester = requester

            def create(
                self, request: types.CreateLogAttributeRequest
            ) -> types.LogAttribute:
                """Attach a log attribute to an LLM log."""
                return self._requester.create_attribute(request)

    class _Completions:
        def __init__(self, requester: Requester, client: OpenAI):
            self.client = client
            self._requester = requester

        def create(
            self, *args: typing.Any, **kwargs: typing.Any
        ) -> typing.Tuple[ChatCompletion, typing.Any, typing.Any]:
            """Create an OpenAI completion and log the LLM input and output."""
            # Do not mutate the input kwargs. That is an unexpected behavior for
            # our caller.
            kwargs = kwargs.copy()
            # Extract trace_id from kwargs, if it exists, otherwise set it to None
            trace_id = kwargs.pop("trace_id", None)
            mode_type = types.parse_mode_type(kwargs.pop("mode", "unspecified"))

            # Deep copy the kwargs to avoid modifying the original
            req_copy = kwargs.copy()
            if "model" not in req_copy:
                raise ValueError("model needs to be passed in as a kwarg")
            req_copy["model_name"] = req_copy.pop("model")

            # Send HTTP request before calling create
            input_resp = self._requester.create_openai_input_log(
                req_copy["model_name"],
                # TODO(dbmikus) fix sloppy typing
                typing.cast(types.OpenAILLMInputLog, req_copy),
                trace_id=trace_id,
                mode=mode_type,
            )
            dprint(f'Created an input log: {input_resp["name"]}')

            # Make create call to OPEN AI
            openai_response = self.client.chat.completions.create(*args, **kwargs)
            dprint(f"Received an openai response: {openai_response.id}")

            # Send HTTP request after calling create
            output_resp = self._requester.create_openai_output_log(
                req_copy["model_name"],
                input_resp,
                openai_response,
                trace_id=trace_id,
                mode=mode_type,
            )
            dprint(f"Created an output log: {output_resp['name']}")

            return openai_response, input_resp, output_resp

    class _Chat:
        def __init__(self, requester: Requester, client: OpenAI):
            self.completions = FixpointClient._Completions(requester, client)
