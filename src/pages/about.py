"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st
from listener_twitter import TwStreamListener
import awesome_streamlit as ast
from awesome_streamlit.core.services import resources
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import plotly.express as px
import os
from collections import defaultdict
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

def emotion_count(text,vocab):
    # Separamos las palábras por espacios.
    words=text.split(" ")
    # Creamos un diccionario donde se guardarán los conteos por cada emoción.
    counts={i:0 for i in list(vocab.keys())}
    # Creamos un diccionario donde se guardarán las palabras coincidentes con cada léxico.
    words_per_emo={i:[] for i in list(vocab.keys())}
    # Iteramos para cada una de las palábras dentro del texto.
    for word in words:
        # Iteramos para cada una de las emociones del léxico.
        for emo in vocab:
            # Evalúamos si la palabra está dentro del léxico de cada emoción
            if word in vocab[emo]:
                # Si la palabra está en el léxico de la emoción, sumamos 1 al conteo acumulado.
                counts[emo]+=1
                # También agregamos la palabra coincidente.
                words_per_emo[emo].append(word)
    return counts, words_per_emo


def write():
    """Writes content to the app"""
    ast.shared.components.title_awesome("Análisis Twitter")
        
    tags = st.selectbox("Selecciona el sector que deseas analizar", options = ['Salud', 'Medio ambiente', 'Educacion', 'Seguridad'])
    

    author_all = ast.shared.models.Author(name="Todos", url="")
    author = st.selectbox("Selecciona tu municipio", options=['Municipio de Bello'])
    if author == author_all:
        author = None
    
    if not tags:
        st.info(
             """Para continuar por favor **selecciona el sector que te gustaria analizar**"""
        )
        
    if tags:
        with st.spinner("Analizando post de tu comunidad en tiempo real en Twitter ..."):
            engine = create_engine('postgresql://postgres:vu44qnBW2xQxYXYQNiVv@ds4a-extended.cqwg91rhslbj.us-east-1.rds.amazonaws.com/ds4a_project', max_overflow=20)
            query = 'SELECT * FROM twitter_deep'
            df_total = pd.read_sql(query, engine)
            df_clasificacion = df_total[df_total['sector'] == tags].copy()
            st.write("**Diez ultimos post del sector {}:**".format(tags))
            df_clasificacion = df_clasificacion.reset_index(drop=True)
            st.table(df_clasificacion['text'].tail(10))
            
 
            b = len(df_clasificacion[df_clasificacion['emotions']=='Positivo'])
            a = len(df_clasificacion[df_clasificacion['emotions']=='Negativo'])
            c = len(df_clasificacion[df_clasificacion['emotions']=='Neutro'])

            sizes=[a, b, c]

            df0=pd.DataFrame()
            df0['experiencia']=[ 'Negativos', 'Positivos', 'Neutrales']
            df0['cantidad']=sizes
            
            fig, ax = plt.subplots(figsize=(12, 5))
            fig = px.pie(df0, values='cantidad', names='experiencia',hole=0.5,title='ANÁLISIS DE LA PERCEPCIÓN DEL USUARIO EN EL SECTOR:'+' '+str.upper(tags),color_discrete_sequence=["lightseagreen","palegoldenrod","darkseagreen"])
            
            st.plotly_chart(fig)
            
            
            
            vocab={}
            # Iteramos para cada una de las emociones de EmoLex.
            for lexicon in os.listdir("EmoLex/"):
                # Se abre cada .txt, se extraen todas las palabras y se eliminan saltos de línea.
                with open("EmoLex/"+lexicon,"r") as f:
                    vocab[lexicon.split(".")[0]]=[i[:-1] for i in f.readlines()]

            
            
            ######LINEAS A CAMBIAR#########################################################
            
            df_emotionals = df_total[df_total['sector'] == tags].copy()
            df_emotionals['counts,detected_words']=df_emotionals['text'].apply(lambda x: emotion_count(x,vocab)[0])
            ################################################################################

            dd = defaultdict(list)
            list_emotions=df_emotionals['counts,detected_words'].tolist()
            for d in (list_emotions):
                 for key, value in d.items():
                     dd[key].append(value)


            for name, value in dd.items():
                dd[name]=sum(value)

            dd0={}
            for name, value in dd.items():
                if name=='anger':
                    name='enojo'
                    dd0[name]=value

                if name=='fear':
                    name='ansiedad'
                    dd0[name]=value

                if name=='trust':
                    name='confianza'
                    dd0[name]=value

                if name=='negative':
                    name='negativa'
                    dd0[name]=value

                if name=='anticipation':
                    name='anticipación'
                    dd0[name]=value

                if name=='disgust':
                    name='disgusto'
                    dd0[name]=value

                if name=='positive':
                    name='positiva'
                    dd0[name]=value

                if name=='joy':
                    name='disfrute'
                    dd0[name]=value

                if name=='surprise':
                    name='sorpresa'
                    dd0[name]=value

                if name=='sadness':
                    name='tristeza'
                    dd0[name]=value
            df_p=pd.DataFrame(dd0, index=range(0,11))
            df_p=df_p.T
            df_p=df_p.rename(columns={0:'Frecuencia'})
            df_p=df_p[['Frecuencia']]
            df_p=df_p.sort_values(by='Frecuencia', ascending=False)

            fig=px.bar( x=df_p.index,color_discrete_sequence=["darkgreen","gold","yellowgreen"], y=df_p.Frecuencia, title='Ámbito de las expresiones utilizadas en twitter: {}'.format(tags),  labels=dict(x="Tipología de las palabras empleadas", y="Frecuencia", color="Place"))
            st.plotly_chart(fig)
            
            
            df_cloud = df_total[df_total['sector'] == tags].copy()
            df_cloud = df_cloud.reset_index(drop=True)
            df_cloud['text']=df_cloud['text'].apply(lambda x: x.split())
            
            
            lista_mensajeuser=[]
            for i in range(len(df_cloud)):
                lista_mensajeuser+=df_cloud['text'][i]
            long_string=','.join(lista_mensajeuser)
            #Creacion lista stop words
            wordcloud = WordCloud(width=1000, height=500,background_color="white",min_font_size=3, max_font_size=150, max_words=700, contour_width=80, contour_color='steelblue', margin=15, stopwords=stopwords.words('spanish') + ['RT','UU', 'EE'])
            #Crear el word cloud
            wordcloud.generate(long_string)
            #Visualizar el word cloud
            plt.figure(figsize=(15,10))
            plt.imshow(wordcloud, interpolation='bilinear', resample=True)
            plt.axis("off")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.write("**Nube de palabras sector {}:**".format(tags))
            st.pyplot()
            
        
            
            sentimental = st.selectbox("Selecciona el estado de animo:", options=['Positivo', 'Negativo', 'Neutro'])
            
            
            if sentimental:
                with st.spinner("Analizando tweets {} de tu comunidad ...".format(sentimental)):
                    df_sent = df_clasificacion[df_total['emotions'] == sentimental].copy()
                    df_sent = df_sent.reset_index(drop=True)
                    st.table(df_sent['text'].tail(10))
                    
                    
            
                    
    
    tags = None


if __name__ == "__main__":
    write()
