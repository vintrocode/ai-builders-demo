# AI Builders Demo

Quick CLI chatbot to run through the basic functionalities of Honcho for the AI Builders group in the Netherlands. This is a simple conversational chatbot that has an intermediate "thought" step to make a prediction about what the user might be thinking and using that as context to generate a response.

**This project assumes you have [Honcho]([url](https://github.com/plastic-labs/honcho)) running locally.** Alternatively, you can use the hosted demo server by changing line 9 in `main.py` to the following:
```
honcho = Honcho(environment='demo')
```

This is a python poetry project. To set up the virtual env, run the following commands at the root of the repo:

```
poetry install
poetry shell
```

Then it's a simple `python main.py` to run the app.
