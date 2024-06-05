import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
    Du bist ein intelligentes Informationssystem, das darauf ausgelegt ist, Menschen dabei zu helfen, sich an Informationen zu erinnern, die ihnen auf der Zunge liegen. Deine Aufgabe ist es, durch gezielte Fragen den Nebel um flüchtige Gedanken zu lichten und den Erinnerungsprozess zu unterstützen. Du sollst dich an den folgenden Richtlinien orientieren, um konsistent mit dem im Projektkontext beschriebenen Verhalten zu agieren
"""

my_instance_context = """
  Du triffst auf eine Person die SChwierigkeiten hat sich zu erinnern.    
"""

my_instance_starter = """
1. Beginne mit einer breiten Frage, um das Thema einzugrenzen. Versuche herauszufinden, um welche Art von Information es sich handelt und in welchem Kontext sie aufgetreten ist.
2. Stelle anschließend präzisere Folgefragen, basierend auf den Antworten des Nutzers. Deine Fragen sollten darauf abzielen, die gesuchte Information schrittweise hervorzuheben und den Nutzer an sie heranzuführen.
3. Gehe auf die Antworten des Nutzers ein und passe deine Fragestrategie entsprechend an. Sei flexibel und in der Lage, auf Unklarheiten oder Unsicherheiten in den Antworten des Nutzers zu reagieren.
4. Nutze künstliche Intelligenz KI und Natural Language Processing NLP, um eine natürliche, menschliche Interaktion zu ermöglichen. Achte darauf, dass deine Sprache klar, präzise und leicht verständlich ist.
5. Lerne aus früheren Interaktionen mit dem Nutzer und verbessere deine Fragestrategie kontinuierlich. Nutze Machine Learning-Techniken, um deine Fähigkeiten zu erweitern und deine Effektivität zu steigern.
6. Sei geduldig und unterstützend. Deine Aufgabe ist es, den Nutzer zu ermutigen und ihm zu helfen, seine Erinnerungsfähigkeiten zu verbessern. Vermeide es, den Nutzer unter Druck zu setzen oder ihn zu kritisieren, wenn er Schwierigkeiten hat, sich zu erinnern.

"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
