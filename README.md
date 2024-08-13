# ChatBuddy

ChatBuddy is your friendly Chatbot designed to help you improve your English through conversational practice. Whether you're a beginner or looking to refine your skills, ChatBuddy offers interactive conversations to enhance your fluency and confidence.

![alt text](img/example.png)

ChatBuddy supports practicing:

* Speaking: Use the mic for voice input, which is transcribed to text.
* Listening: Hear the responses through voice output at the end of each ChatBuddy message.
* Reading: Engage with text-based interactions.
* Writing: Practice your writing skills through typed responses.

## Used Tools

- Chainlit - https://docs.chainlit.io/get-started/overview
- Python (3.11) - https://docs.python.org/3.11/
- Ollama - https://ollama.com/
- Gramformer - https://github.com/PrithivirajDamodaran/Gramformer
- Google Text-to-Speech - https://gtts.readthedocs.io/en/latest/

## Gramformer Installation

```js
pip3 install spacy
```

```js
python3 -m spacy download en_core_web_sm
en-core-web-sm==3.7.1
```

```js
pip install -U git+https://github.com/PrithivirajDamodaran/Gramformer.git
```

## Install required libraries

```js
pip install -r requirements.txt
```

## How to run Chainlit

```js
python -m chainlit run main.py
```


