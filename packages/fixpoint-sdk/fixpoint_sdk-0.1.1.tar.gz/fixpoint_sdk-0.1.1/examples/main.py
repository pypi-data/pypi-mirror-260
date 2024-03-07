"""An example using the basics of the Fixpoint SDK."""

# pylint: disable=unused-variable

from fixpoint_sdk import FixpointClient, ThumbsReaction


def main() -> None:
    """An example of using FixpointClient to make LLM calls and record feedback."""

    # Make sure that the enviroment variables set:
    # - `FIXPOINT_API_KEY` is set to your Fixpoint API key
    # - `OPENAI_API_KEY` is set to your normal OpenAI API key
    # Create a FixpointClient instance (uses the FIXPOINT_API_KEY env var)
    client = FixpointClient()

    # Call create method on FixpointClient instance. You can specify a user to
    # associate with the request. The user will be automatically passed through
    # to OpenAI's API.
    openai_response, fixpoint_input_log_response, fixpoint_output_log_response = (
        client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What are you?"},
            ],
            user="some-user-id",
        )
    )

    # If you make multiple calls to an LLM that are all part of the same "trace"
    # (e.g. a multi-step chain of prompts), you can pass in a trace_id to
    # associate them together.
    openai_response2, fixpoint_input_log_response2, fixpoint_output_log_response2 = (
        client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What are you?"},
            ],
            trace_id="some-trace-id",
        )
    )

    # You can use the Fixpoint API in different environment modes: "test",
    # "staging", and "prod".
    # This is useful to make sure that your logged production traffic does not
    # get cluttered with test data or staging data.
    # If you do not specify a mode, we default to "prod".
    for env_mode in ["test", "staging", "prod"]:
        client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            mode=env_mode,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant running in {env_mode} mode.",
                },
                {"role": "user", "content": "What are you?"},
            ],
        )

    # Record user feedback. One user giving a thumbs up to a log, the other giving a thumbs down.
    # The `user_id` you specify should be your own system's user identifier for
    # whoever gave the feedback.
    client.fixpoint.user_feedback.create(
        {
            "likes": [
                {
                    "log_name": fixpoint_input_log_response["name"],
                    "thumbs_reaction": ThumbsReaction.THUMBS_UP,
                    "user_id": "some-user-id",
                },
                {
                    "log_name": fixpoint_input_log_response2["name"],
                    "thumbs_reaction": ThumbsReaction.THUMBS_DOWN,
                    "user_id": "some-other-user-id",
                },
            ]
        }
    )

    # Record an attribute
    client.fixpoint.attributes.create(
        {
            "log_attribute": {
                "log_name": fixpoint_input_log_response["name"],
                "key": "conversion",
                "value": "true",
            }
        }
    )


main()
