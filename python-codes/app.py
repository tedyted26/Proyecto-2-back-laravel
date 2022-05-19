
#External Imports
from flask import Flask, request, jsonify
#from textblob import TextBlob
from flask_cors import CORS, cross_origin

#Internal Imports
from helpers import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Esto es el inicio de la API"

@app.route('/app-sentiment-analysis', methods=["POST"])
def sentiment_analysis():
    if request.method == 'POST':
        text_input_user = request.json["texto"]
        print(f"Recibido texto: {text_input_user}")
        listaTweets = sentimientoTweets(text_input_user)
        return listaTweets
    else:
        print("\n\nNo es post\n\n")
        return None

if __name__ == '__main__':
    app.run(debug = True)