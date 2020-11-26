"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st
from listener_twitter import TwStreamListener
import awesome_streamlit as ast
from awesome_streamlit.core.services import resources
from class_PQRS import nlp_pqr
import pandas as pd
import plotly.express as px
from streamlit import components
import urllib.request

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def write():
    """Writes content to the app"""
    ast.shared.components.title_awesome("Percepción de los ciudadanos basados en PQRSD")
    st.write("Estamos trabajando para generar mayor valor a tus datos, en proximos días estara disponible esta funcionalidad.")
    
    tags = st.selectbox("Selecciona un sector", ['', 'salud', 'ambiental', 'educacion', 'justicia y seguridad'], format_func=lambda x: 'Selecciona una opción' if x == '' else x)
    
    
    if not tags:
        st.info(
             """Para continuar por favor **selecciona el sector que te gustaria analizar**"""
        )
        
    if tags:
        with st.spinner("Analizando los PQRS de tu municipio: "):
            path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/Data/consolidado_general_con_sectores.csv'
                        
            consolidado_general_sectores=pd.read_csv(path)
            
            ###Solo los sectores de interès
            a=consolidado_general_sectores.groupby(['sector','year']).count()
            a=a[['Medio']]
            
            a.reset_index(inplace=True)
            a=a.rename(columns={'year':'Año','Medio':'Cantidad de quejas'})
            st.write("**Cantidad de quejas en total por año y sector de interés:**")
            fig = px.bar(a,x='Año',y='Cantidad de quejas', facet_col='sector',color_discrete_sequence=["lightseagreen"],  labels=dict(x="Año", y="Cantidad de quejas", color="Place", ),height=400, width=800)
            
            fig.update_xaxes(type='category')
            st.plotly_chart(fig)
            path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/Data/consolidado_general_con_sectores_modelos.csv'

            consolidado_general_sectores_modelos=pd.read_csv(path)
            consolidado_general_sectores_modelos = consolidado_general_sectores_modelos.replace({pd.np.nan:''})
             
            nlp=nlp_pqr(consolidado_general_sectores_modelos)
            nlp.patrones(tags)
            nlp.palabras_ngramas(tags)
            with st.spinner("Analizando a mucho mas detalle tus datos ..."):
                opener = urllib.request.FancyURLopener({})
                path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/html/{}/vis.html'.format(tags)
                st.write("Principales temas en el sector {}".format(tags))
                st.write("Mediante el algoritmo Latent Dirichlet Allocation (LDA) extraemos los temas más relevantes en los textos escritos por los usuarios en cada sector. El tamaño del círculo de la figura representa la relevancia de ese tema en el respectivo sector. Adicionalmente, cada círculo consta de palabras que por medio del score de coherencia fueran agrupadas según su similaridad.")
                f = opener.open(path)
                content = f.read()
                
                components.v1.html(content, width=800, height=700, scrolling=True)


                path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/html/{}/percepcion.html'.format(tags)
                
                st.write("**Percepción de los ciudadanos:**")
                f2 = opener.open(path)
                content2 = f2.read()

                components.v1.html(content2, width=700, height=400, scrolling=True)
                  
                path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/html/{}/wcloud.png'.format(tags)

                st.write("**Nube de palabras por tópicos:**")
                st.write("Permite visualizar las palabras más relevantes de cada uno de los clustérs encontradas en los texto.  Adicionalmente, mediante la nube de palabras podemos identificar de manera rápida el tipo de solicitudes realizadas por los usuarios.")
                st.image(path)

        
    
    tags = None

        

if __name__ == "__main__":
    write()
