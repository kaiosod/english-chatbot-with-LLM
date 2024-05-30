import ollama
import chainlit as cl
import autocorrect
from gtts import gTTS


@cl.on_chat_start
async def on_chat_start():
    # cl.user_session.set("chat_history", [])
    cl.user_session.set("chat_history", [{"role": "system",
                        "content": "You an online English teacher focused on learning English through internet chat conversations. You are a teacher that always provide short and natural answers. You must correct grammar errors, typos and any english erros"}])

@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")

    # fixed text
    fixed = autocorrect.grammar_checker(query.content)

    # Show user input
    chat_history.append({"role": "user", "content": query.content})
    
    response = cl.Message(content="")
    answer = ollama.chat(model="llama3:8b", # Llama3:8b
                         messages=chat_history, 
                         stream=True)
    
    # Generate answer based on user input (query.content)
    complete_answer = ""
    for token_dict in answer:
        token = token_dict["message"]["content"]
        complete_answer += token
        await response.stream_token(token)

    tts = gTTS(text=f'{complete_answer}', lang='en')
    tts.save("output.mp3")
    
    # final_message = complete_answer + f"\n {fixed}"

    chat_history.append({"role": "assistant", "content": complete_answer + ""})    
    cl.user_session.set("chat_history", chat_history)

    if fixed == 1: 
        pass
    else: 
        # Add correction
        response = cl.Message(content= f"Correction: {fixed}")

    # send the correction message
    await response.send()

    #Audio
    elements = [
        cl.Audio(name="output.mp3", path="output.mp3", display="inline"),
    ]

    await cl.Message(
        content="Voice Output",
        elements=elements,
    ).send()




