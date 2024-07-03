from calls import Think, Converse
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

think_response = ""
converse_response = ""

def main():
    global think_response
    global converse_response
    global converse
    # enter a name upon starting to simulate some auth flow
    name = input("Enter your name: ")

    # get_or_create a user
    user = honcho.apps.users.get_or_create(app_id=app.id, name=name)

    # create session
    session = honcho.apps.users.sessions.create(
        app_id=app.id,
        user_id=user.id,
        location_id="cli",
    )

    # one time name roast
    print("Thought:")
    think.name = name
    think.history = []
    response = think.stream()
    for chunk in response:
        think_response += chunk.content
        print(chunk.content, end="", flush=True)
    print("\n")


    print("Response:")
    converse.name = name
    converse.history = []
    converse.thought = think_response
    response = converse.stream()
    for chunk in response:
        converse_response += chunk.content
        print(chunk.content, end="", flush=True)
    print("\n")

    # write to honcho
    honcho.apps.users.sessions.messages.create(
        app_id=app.id,
        session_id=session.id,
        user_id=user.id,
        content=converse_response,
        is_user=False
    )
    message = honcho.apps.users.sessions.messages.create(
        app_id=app.id,
        session_id=session.id,
        user_id=user.id,
        content=name,
        is_user=True
    )
    honcho.apps.users.sessions.metamessages.create(
        app_id=app.id,
        session_id=session.id,
        user_id=user.id,
        content=think_response,
        metamessage_type="thought",
        message_id=message.id
    )

    # conversation loop
    while True:

        user_input = input(">>> ")

        history_iter = honcho.apps.users.sessions.messages.list(
            app_id=app.id, session_id=session.id, user_id=user.id
        )

        think.history = []
        converse.history = []

        for message in history_iter:
            if message.is_user:
                think.history += [
                    {"role": "user", "content": message.content}
                ]
                converse.history += [
                    {"role": "user", "content": message.content}
                ]
            else:
                think.history += [
                    {"role": "assistant", "content": message.content}
                ]
                converse.history += [
                    {"role": "assistant", "content": message.content}
                ]


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

        # write as message
        honcho.apps.users.sessions.messages.create(
            app_id=app.id,
            session_id=session.id,
            user_id=user.id,
            content=name,
            is_user=True,
        )

        message = honcho.apps.users.sessions.messages.create(
            app_id=app.id,
            session_id=session.id,
            user_id=user.id,
            content=converse_response,
            is_user=False,
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







if __name__ == "__main__":
    main()
