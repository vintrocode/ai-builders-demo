import sys
from calls import Think, Converse, Summarize
from dotenv import load_dotenv
from honcho import Honcho

load_dotenv()

# honcho client
honcho = Honcho()  # defaults to local
app = honcho.apps.get_or_create("ai-builders-demo")

think = Think(
    name="",
    history=[],
)

converse = Converse(
    history=[],
    name="",
    thought="",
)

summarize = Summarize(
    history=[],
)

history = []

def main():
    global history

    # enter a name upon starting to simulate some auth flow
    user_input = input("Enter your name: ")
    name = user_input

    # get_or_create a user
    user = honcho.apps.users.get_or_create(app_id=app.id, name=name)

    # create session
    session = honcho.apps.users.sessions.create(
        app_id=app.id,
        user_id=user.id,
        location_id="cli",
    )

    history += [
        {"role": "user", "content": user_input}
    ]

    think.history = history
    converse.history = history

    think_response = ""
    converse_response = ""

    # conversation loop
    while True:

        response = think.stream()
        print("Thought:")
        for chunk in response:
            print(chunk.content, end="", flush=True)
            think_response += chunk.content
        print("\n")

        response = converse.stream()
        print("Response:")
        for chunk in response:
            print(chunk.content, end="", flush=True)
            converse_response += chunk.content
        print("\n")

        user_input = input(">>> ")

        history += [
            {"role": "assistant", "content": converse_response}
        ]
        history += [
            {"role": "user", "content": user_input}
        ]

        # write as message
        message = honcho.apps.users.sessions.messages.create(
            app_id=app.id,
            session_id=session.id,
            user_id=user.id,
            content=converse_response,
            is_user=False,
        )
        honcho.apps.users.sessions.messages.create(
            app_id=app.id,
            session_id=session.id,
            user_id=user.id,
            content=user_input,
            is_user=True,
        )

        # write as metamessage associated to that message
        honcho.apps.users.sessions.metamessages.create(
            app_id=app.id,
            session_id=session.id,
            user_id=user.id,
            message_id=message.id,
            metamessage_type="thought",
            content=think_response,
        )

        if user_input == 'exit':
            get_summary(name, session.id)
            sys.exit()

        user_input = ""
        converse_response = ""
        think_response = ""


def get_summary(name: str, session_id: str):
    global summarize
    ## query message history from honcho
    history = []
    # get_or_create a user
    user = honcho.apps.users.get_or_create(app_id=app.id, name=name)
    session = honcho.apps.users.sessions.get(
        app_id=app.id,
        user_id=user.id,
        session_id=session_id
    )
    history_iter = honcho.apps.users.sessions.messages.list(
        app_id=app.id, session_id=session.id, user_id=user.id
    )
    for message in history_iter:
        if message.is_user:
            history.append(f"user: {message.content}")
        else:
            history.append(f"assistant: {message.content}")

    # summarize
    print("Summary:")
    summarize.history = history
    response = summarize.stream()
    for chunk in response:
        print(chunk.content, end="", flush=True)
    print("\n")

    print("Dialectic API Response")
    answer = honcho.apps.users.sessions.chat(
        session_id, 
        user_id=user.id, 
        app_id=app.id, 
        query="What do we know about the user?"
    )
    print(answer.content)


if __name__ == "__main__":
    main()
