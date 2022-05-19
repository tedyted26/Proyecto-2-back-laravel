#External Imports
from textblob import TextBlob
from deep_translator import GoogleTranslator
import tweepy
from datetime import date, timedelta


def extractTweets(busqueda):
    consumer_key = "K5CQ385KRpL8nlsHnoLpqcyaT"
    consumer_secret = "VZkRXTLwjE3KOcl0BAMdlwprPBtWpIB5bWN8HjjuVKqmrN4pEo"
    access_token = "1448336514455330827-LoK6OnU8sUpjW3HzwlNH25E0rap1NY"
    access_token_secret = "GqvoYfGAQphlZfotRhQL93hHMh5xdtvfsRpxUXHE0o6pm"

    #Autenticacion de la API de Twitter con las credenciales dadas
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    listaTweets = tweepy.Cursor(api.search_tweets, q=f'{busqueda} -filter:retweets').items(100)
    listatextos = []

    fechaAyer = date.today() - timedelta(days=1)
    contador = 0

    totalMg = 0
    totalRt = 0

    for tweet in listaTweets:
        contador += 1
        print(str(contador)+": "+str(tweet.created_at.date()))
        #print(tweet.text)
        '''
        try:
            print(tweet.retweet_count)
            print(tweet.favorite_count)
        except:
            None
        '''

        if tweet.created_at.date() >= fechaAyer:
            totalMg += tweet.favorite_count
            totalRt += tweet.retweet_count
            status = api.get_status(tweet.id, tweet_mode="extended")
            try:
                listatextos.append(status.retweeted_status.full_text)
            except AttributeError:  # Not a Retweet
                listatextos.append(status.full_text)
    
    return listatextos, totalMg, totalRt

def calculoSent(list_of_text, totalMg, totalRt, busqueda):
    polaridadTotal = 0
    positivos = 0
    negativos = 0
    neutros = 0

    list_objects = []
    id = 0
    cont = 0
    for tweet in list_of_text:
        cont += 1
        try:
            id += 1
            translated = GoogleTranslator(source='auto', target='en').translate(tweet)
            traduccion = TextBlob(translated)
            #print(traduccion.words)
            sentimiento = traduccion.sentiment[0]
            '''
            tweet_object = {
                'id':id,
                "texto":tweet,
                "traduccion":traduccion,
                'sentimiento':sentimiento
            }
            '''
            polaridadTotal = polaridadTotal+sentimiento
            
            if sentimiento == 0:
                neutros += 1
            elif sentimiento > 0:
                positivos += 1
            elif sentimiento < 0:
                negativos += 1
                
            #list_objects.append(str(tweet_object))
             
            print(str(cont)+": "+str(sentimiento))
            
        except:
            print("Error de traducción")
    print('\n..........\n')
            

    print("Suma de polaridades: "+str(polaridadTotal))
    print("Polaridad media: "+str(polaridadTotal/(negativos+positivos)))
    print("Tweets negativos: " + str(negativos))
    print("Tweets positivos: " + str(positivos))
    print("Tweets neutros: " + str(neutros))

    resultados = {
                "busqueda": busqueda,
                'tweetsAnalizados':len(list_of_text),
                "polaridadMedia":polaridadTotal/(negativos+positivos),
                "positivos":positivos,
                'negativos':negativos,
                "neutros": neutros,
                "totalMg": totalMg,
                "totalRt": totalRt
            }
    
    return resultados

def sentimientoTweets(busqueda):
    tweets, totalMg, totalRt = extractTweets(busqueda)
    listaTweets = calculoSent(tweets, totalMg, totalRt, busqueda)
    return str(listaTweets)