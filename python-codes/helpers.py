#External Imports
#import tweepy
from textblob import TextBlob
from flask import jsonify, make_response
import datetime

#Internal Imports
#from tweepy import OAuthHandler

# No usamos twitter de momento
'''
def twitter_data_access():
    consumer_key = "K5CQ385KRpL8nlsHnoLpqcyaT"
    consumer_secret = "VZkRXTLwjE3KOcl0BAMdlwprPBtWpIB5bWN8HjjuVKqmrN4pEo"
    access_token = "1448336514455330827-LoK6OnU8sUpjW3HzwlNH25E0rap1NY"
    access_token_secret = "GqvoYfGAQphlZfotRhQL93hHMh5xdtvfsRpxUXHE0o6pm"

    #Autenticacion de la API de Twitter con las credenciales dadas
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    listaTweets = tweepy.Cursor(api.search_tweets, q='ucrania -filter:retweets').items(50)
    listatextos = []
    for tweet in listaTweets:
        print(tweet.text)
        status = api.get_status(tweet.id, tweet_mode="extended")
        try:
            listatextos.append(status.retweeted_status.full_text)
        except AttributeError:  # Not a Retweet
            listatextos.append(status.full_text)
        
    return listatextos
'''

def preprocessing_input_user(text_to_process):
    texto = TextBlob(text_to_process)
    traduccion = TextBlob(str(texto.translate(to='en')))
    polaridadTotal = 0
    if (traduccion.sentiment[0]>0):
        polaridadTotal = polaridadTotal+traduccion.sentiment[0]
        text_object = {
                
                "polaridad":polaridadTotal,
                "type_text": "positivo",
            }
    
    elif (traduccion.sentiment[0]<0):
        polaridadTotal = polaridadTotal+traduccion.sentiment[0]
        text_object = {
                
                
                "polaridad":polaridadTotal,
                "type_text": "negativo",
            }

    elif (traduccion.sentiment[0]==0):
        polaridadTotal = polaridadTotal+traduccion.sentiment[0]
        text_object = {

                "polaridad":polaridadTotal,
                "type_text": "neutro",
            }
    print(text_object)
    return jsonify(text_object)


'''
def preprocessing(list_of_text):
    polaridadTotal = 0
    positivos = 0
    negativos = 0
    neutros = 0

    list_objects = []
    id = 0
    for tweet in list_of_text:
        try:
            id += 1
            texto = TextBlob(tweet)
            traduccion = TextBlob(str(texto.translate(to='en')))
            print(traduccion.words)
            if (traduccion.sentiment[0]>0):
                positivos += 1
                tweet_object = {
                'id':id,
                "texto":texto,
                "traduccion":traduccion,
                'type_tweet': "positivo"
            }
                polaridadTotal = polaridadTotal+traduccion.sentiment[0]
            elif (traduccion.sentiment[0]<0):
                negativos += 1
                tweet_object = {
                'id':id,
                "texto":texto,
                "traduccion":traduccion,
                'type_tweet': "negativo"
            }
                polaridadTotal = polaridadTotal+traduccion.sentiment[0]
            elif (traduccion.sentiment[0]==0):
                neutros += 1
                tweet_object = {
                'id':id,
                "texto":texto,
                "traduccion":traduccion,
                'type_tweet':"neutro"
            }
            list_objects.append(str(tweet_object))
             
            print(traduccion.sentiment[0])
            
        except:
            print("Error de traducción")
    print('\n..........\n')
            

    print("Suma de polaridades: "+str(polaridadTotal))
    print("Polaridad media: "+str(polaridadTotal/(positivos+negativos)))
    print("Tweets negativos: " + str(negativos))
    print("Tweets positivos: " + str(positivos))
    print("Tweets neutros: " + str(neutros))
    
    return jsonify(list_objects)
'''