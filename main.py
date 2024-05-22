import ollama
import chainlit as cl
import autocorrect


@cl.on_chat_start
async def on_chat_start():
    # cl.user_session.set("chat_history", [])
    cl.user_session.set("chat_history", [{"role": "system",
                        "content": "You an online English teacher focused on learning English through internet chat conversations. You are a teacher that always provide short and natural answers. You must correct grammar errors, typos and any english erros"}])

@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")

    fixed = autocorrect.grammar_checker(query.content)

    # Show user input
    chat_history.append({"role": "user", "content": query.content})

    # List of used LLM
    # llama2 - answers with emojis and heavy
    # gemma:2b - ?
    
    response = cl.Message(content="")
    answer = ollama.chat(model="llama3:8b", # llama2 - the last one tested for chatbot 
                         messages=chat_history, 
                         stream=True)
    # Generate answer based on user input (query.content)
    complete_answer = ""
    for token_dict in answer:
        token = token_dict["message"]["content"]
        complete_answer += token
        await response.stream_token(token)
    

    # complete_answer += f"\n {fixed}"
    # Show Bot input
    print(complete_answer)
    print(type(complete_answer))

    final_message = complete_answer + f"\n {fixed}"

    chat_history.append({"role": "assistant", "content": complete_answer + "FIM"})    
    cl.user_session.set("chat_history", chat_history)

    await response.send()

    # query.content = f"\n {fixed}"

    # await response.update()



