from my_secrets import Secrets
import chainlit as cl
from litellm import completion
import json

secrets = Secrets()


@cl.on_chat_start
async def start_chat():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content="Welcome to the chatbot! How can I assist you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(
        content="",  # Initialize with empty content
    )
    await msg.send()

    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    try:

        response = completion(
            model=secrets.gemini_model,
            api_key=secrets.gemini_api_key,
            messages=history,
            # stream=True,
        )
        # Streaming currently not supported(giving errors) by litellm, so we use the full response instead
        # Iterate over the streamed chunks
        # This 'async for' loop is what awaits the next chunk from the stream
        """ async for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                current_response_content += token
                await msg.stream_token(token) # Stream the token to the UI

        msg.content = current_response_content # Set the final content of the message
        await msg.update() # Update the message to ensure all content is displayed
        history.append({"role": "assistant", "content": current_response_content})
        """
        response_content = response.choices[0].message.content
        msg.content = response_content
        history = cl.user_session.get("chat_history", [])
        history.append({"role": "assistant", "content": response_content})
        await msg.update()

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        msg.content = error_message
        await msg.update()


@cl.on_chat_end
async def end():
    history = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=4)
