"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st
from listener_twitter import TwStreamListener
import awesome_streamlit as ast
from awesome_streamlit.core.services import resources
from class_PQRS import nlp_pqr
import pandas as pd
import plotly.express as px

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
            
            fig = px.bar(a,x='Año',y='Cantidad de quejas', facet_col='sector',color_discrete_sequence=["lightseagreen"], title='Cantidad de quejas en total por año y sector de interés', labels=dict(x="Año", y="Cantidad de quejas", color="Place", ),height=400, width=800)
            
            fig.update_xaxes(type='category')
            st.plotly_chart(fig)
            path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/Data/consolidado_general_con_sectores_modelos.csv'

            consolidado_general_sectores_modelos=pd.read_csv(path)
            consolidado_general_sectores_modelos = consolidado_general_sectores_modelos.replace({pd.np.nan:''})
             
            nlp=nlp_pqr(consolidado_general_sectores_modelos)
            nlp.patrones(tags)
            nlp.palabras_ngramas(tags)
            with st.spinner("Analizando a mucho mas detalle tus datos ..."):
                nlp.lda_model(tags)
                
                with st.spinner("Analizando la percepción de tu ciudadania."):
                    path = 'https://raw.githubusercontent.com/AdonaiVera/Bello/master/Data/consolidado_para_percepcion.csv'

                    consolidado_general_percepcion=pd.read_csv(path)
                    percept=nlp_pqr(consolidado_general_percepcion)
                    
                    percept.experiencia_user(tags)
    
    tags = None

        

if __name__ == "__main__":
    write()
