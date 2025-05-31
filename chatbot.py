from my_secrets import Secrets
import chainlit as cl
from litellm import acompletion  # ✅ Use async version
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
    msg = cl.Message(content="")
    await msg.send()

    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    current_response_content = ""

    try:
        # ✅ Await acompletion to get async generator
        response_stream = await acompletion(
            model=secrets.openrouter_gemini_model,
            api_key=secrets.openrouter_api_key,
            messages=history,
            stream=True,
        )

        # ✅ This is now an async generator
        async for chunk in response_stream:
            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                token = chunk.choices[0].delta.content
                current_response_content += token
                await msg.stream_token(token)

        msg.content = current_response_content
        await msg.update()
        history.append({"role": "assistant", "content": current_response_content})
        cl.user_session.set("chat_history", history)
    except Exception as e:
        msg.content = f"An error occurred: {str(e)}"
        await msg.update()


@cl.on_chat_end
async def end():
    history = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=4)
