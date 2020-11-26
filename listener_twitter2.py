import re
import tweepy
import time
from sqlalchemy import create_engine, text
from textblob import TextBlob
import pandas as pd
import streamlit as st
from classifier import *
clf = SentimentClassifier()
import googletrans
from googletrans import Translator
import keras

# Override tweepy.StreamListener to add logic to on_status
class TwStreamListener(tweepy.StreamListener):
    #engine = create_engine('postgresql+psycopg2://ds4a_ado:ado@ds4a-extended.cqwg91rhslbj.us-east-1.rds.amazonaws.com/twitterdb', max_overflow=20)
    engine = create_engine('postgresql://postgres:vu44qnBW2xQxYXYQNiVv@ds4a-extended.cqwg91rhslbj.us-east-1.rds.amazonaws.com/ds4a_project', max_overflow=20)
    
    # It's not secure but is just for test fast. 
    API_KEY = 'nl9GDREiaV9Dz2qfcIvATgrcP'
    API_SECRET_KEY = 'uJuHvDgWDddRcgt25bDGmqsWSnwbWLfo7I1wNWSxtUbIJ9dcLR'
    

    auth  = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    runtime = 10
    
    def en_translation(x):
        translate=translator.translate(x, dest='en')
        translate=translate.text
        return translate
    
    
    def __init__(self):
        
        '''
        Check if this table exits. If not, then create a new one.
        '''
        try:
            TABLE_NAME = "twitter_deep"
            TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at timestamp, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude double precision, latitude double precision, \
            retweet_count INT, favorite_count INT, municipality VARCHAR(255), sector VARCHAR(255), emotions VARCHAR(255)"
            
            self.sector = ""
            self.start_time = time.time()
            self.limit_time = self.runtime
            self.engine.connect()
            self.mydb = self.engine.raw_connection()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(TABLE_NAME))
            if self.mycursor.fetchone()[0] != 1:
                self.mycursor.execute("CREATE TABLE {} ({})".format(TABLE_NAME, TABLE_ATTRIBUTES))
                self.mydb.commit()
            self.mycursor.close()
        except Exception as error:
            print("Problem connecting to the database: ",error)
    
    def connect(self):
        '''
        Connecting to the API.
        '''
        ACCESS_TOKEN = '2476071968-hoqd0bVbrSNyuSS2pXpzuIToX9OCaVvVjbF7yJU'
        ACCESS_TOKEN_SECRET = 'zKxfdsBgjasyTNrz0t7zZGzY2GoZ3eSfzxBcFUAPtY19m'
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.myStream = tweepy.Stream(auth = self.api.auth, listener = self)
        return None



        

    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        def get_sentiment(model,text):
            text = punctuation(text)
            #tokenize
            twt = token.texts_to_sequences([text])
            twt = sequence.pad_sequences(twt, maxlen=max_len, dtype='int32')
            sentiment = model.predict(twt,batch_size=1,verbose = 2)
            sent = np.round(np.dot(sentiment,100).tolist(),0)[0]
            result = pd.DataFrame([sent_to_id.keys(),sent]).T
            result.columns = ["sentiment","percentage"]
            result=result[result.percentage !=0]
            return result

        translator = Translator(service_urls=['translate.google.com'])

        def en_translation(x):
            translate=translator.translate(x, dest='en')
            translate=translate.text
            return translate
        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = self.deEmojify(status.text)    # Pre-processing the text  
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
 
        user_created_at = status.user.created_at
        #print("User Location: ", status.user.location)
        user_location = self.deEmojify(status.user.location)
        #print("User Location End: ",user_location)
        user_description = self.deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        # Check the emotions.
        text = self.clean_tweet(text)
        nSentimental = clf.predict(text)
        
        if nSentimental>=0.7:
            estado = "Positivo"
        elif nSentimental<=0.5:
            estado = "Negativo"
        else:
            estado = "Neutro"
   
        text_english = en_translation(text)
        
        path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/model/my_model_emtion.h5'
        
        model = keras.models.load_model(path)
        result = get_sentiment(model, text_english)
        
        idx = result['percentage'].idxmax()
        n = result['sentiment'][idx]
        
        print(n)
        if n=='anger':
            estado = 'Enojado'
        if n=='boredom':
            estado = 'desinterés'
        if n=='empty':
            estado = 'vacio'
        if n=='fun':
            estado = 'diversión'
        if n=='happiness':
            estado = 'felicidad'
        if n=='relief':
            estado = 'alivio'
        if n=='neutral':
            estado = 'neutral'
        if n=='worry':
            estado = 'preocupación'
        if n=='love':
            estado = 'amor'
        if n=='sadness':
            estado = 'tristeza'
        if n=='surprise':
            estado = 'sorpresa'
        if n=='hate':
            estado = 'odio'
        if n=='enthusiasm':
            estado = 'entusiasmo'
        if n=='joy':
            estado = 'miedo'
        if n=='fear':
            estado = 'disfrute'
        
        
        # Store all data in Postgres
        try:
            '''
            Check if this table exits. If not, then create a new one.
            '''
            TABLE_NAME = "twitter_deep"
            self.engine.connect()
            self.mydb = self.engine.raw_connection()
            self.mycursor = self.mydb.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count, municipality, sector, emotions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(TABLE_NAME)
            val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
                user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count, "Bello", self.sector, estado)
            
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.mycursor.close()
        except Exception as error:
            print("Error inserting twitter: ",error)
        
        if (time.time() - self.start_time) < self.limit_time:
            #print("Working")
            return True
        else:
            #print("Time Complete")
            return False
    
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop scraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

    def runQuery(self, sql):
        result = self.engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

    def clean_tweet(self, tweet): 
        ''' 
        Use sumple regex statemnents to clean tweet text by removing links and special characters
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def deEmojify(self,text):
        '''
        Strip all non-ASCII characters to remove emoji characters
        '''
        if text:
            return text.encode('ascii', 'ignore').decode('ascii')
        else:
            return None
    
    def disconnect(self):
        self.mydb.close()
        #return print("Stop Streaming")
    
    def run(self, TRACK_WORDS, LOCATION_SEARCH):
        self.sector = TRACK_WORDS[0]
        #print("Start Streaming")
        # Languaje Español: es
        self.myStream.filter(languages=["es"], track = TRACK_WORDS, locations = LOCATION_SEARCH)
        
        
        time.sleep(self.runtime)
        self.disconnect()
        return None
