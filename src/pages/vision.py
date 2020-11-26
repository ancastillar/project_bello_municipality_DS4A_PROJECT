"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st
from listener_twitter import TwStreamListener
import awesome_streamlit as ast
from awesome_streamlit.core.services import resources
from database_process import DATABASE
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from terridata_proces import terridata
import datetime
from datetime import datetime, date, time
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
from graficar import graph_sam

def write():
    """Writes content to the app"""
    ast.shared.components.title_awesome("Análisis detallado")
    
    tags = ast.shared.components.multiselect(
        "Selecciona los años que deseas visualizar", options=['2013', '2014', '2015', '2016', '2017', '2018', '2019'], default=['2013', '2014', '2015', '2016', '2017', '2018', '2019']
    )
    
    author = st.selectbox("Selecciona un sector", options=['Salud', 'Medio ambiente', 'Educación', 'Seguridad'])
    
    
    if not tags:
        st.info(
             """Para continuar por favor **selecciona el municipio que te gustaria analizar**"""
        )
        
    if tags and author:
        with st.spinner("Analizando tu historico en tiempo real ..."):
            db_obj = DATABASE('ds4a-extended.cqwg91rhslbj.us-east-1.rds.amazonaws.com', 'postgres', 'vu44qnBW2xQxYXYQNiVv', 'ds4a_project')
            df_total = db_obj.db_read('SELECT * FROM main')
            
            
            fig, ax = plt.subplots(figsize=(12, 5))
            if author == 'Salud':
                nSector = 2
            elif author == 'Medio ambiente':
                nSector = 10
            elif author == 'Educación':
                nSector = 1
            else:
                nSector = 18
                        
            st.write("## **Avance general por sectores y años:**")
            df_total['ratio_avance'] = df_total['valor_esperado'] / df_total['valor_ejecutado']
            df_general = df_total[df_total['year'].isin(tags) == True]
            
            
            sector_list = sorted(df_general.sector.unique().tolist())
            df_sectors = db_obj.db_read('SELECT sector, nombre_corto FROM sectors')
            sector_labels = [df_sectors.set_index('sector').at[x, 'nombre_corto'] for x in sector_list]

            year_labels = [str(int(x)) for x in sorted(df_general.year.unique().tolist())]
            
            graph_sam.plotly_bars(df_general, 'sector', 'ratio_avance', 'year', year_labels, sector_labels, 'mean', '', 'Percent [%]')
            
            
            
            st.write("## **Avance segmentado por sector {}:**".format(author))
            
            df_salud = df_total[df_total['sector'] == nSector].copy()
            df_salud = df_salud[df_salud['year'].isin(tags) == True]
            
            sector_list = sorted(df_salud.sector.unique().tolist())
            df_sectors = db_obj.db_read('SELECT sector, nombre_corto FROM sectors')
            sector_labels = [df_sectors.set_index('sector').at[x, 'nombre_corto'] for x in sector_list]

            year_labels = [str(int(x)) for x in sorted(df_salud.year.unique().tolist())]
            
            graph_sam.plotly_bars(df_salud, 'sector', 'ratio_avance', 'year', year_labels, sector_labels, 'mean', '', 'Percent [%]')
            
            
            st.write("## **Rango de clasificación por años:**")
            
            df_sectors = db_obj.db_read('SELECT sector, nombre_corto FROM sectors')
            df_clasificacion = df_total[df_total['sector'] == nSector].copy()
            df_clasificacion = df_clasificacion[df_clasificacion['year'].isin(tags) == True]
            graph_sam.clasificacion(df_clasificacion, df_sectors)
            
    
    
            df_presupuesto = df_total[df_total['sector'] == nSector].copy()
            df_presupuesto = df_presupuesto[df_presupuesto['year'].isin(tags) == True]
            
            sector_list = sorted(df_presupuesto.sector.unique().tolist())
            df_sectors = db_obj.db_read('SELECT sector, nombre_corto FROM sectors')
            sector_labels = [df_sectors.set_index('sector').at[x, 'nombre_corto'] for x in sector_list]

            year_labels = [str(int(x)) for x in sorted(df_presupuesto.year.unique().tolist())]
            
            auth_sect = st.selectbox("Selecciona un tipo de grafica para visualizar el presupuesto", options=['Año', 'Sector'])
            
            if auth_sect == 'Año':
                graph_sam.plotly_bars(df_presupuesto, 'year', 'ejec_total', 'sector', sector_labels, year_labels, 'sum', 'Total resources by Year', 'Billion $COP', b_mode='stack', color='clown')
            else:
                graph_sam.plotly_bars(df_presupuesto, 'sector', 'ejec_total', 'year', year_labels, sector_labels, 'sum', 'Total resources by Sector and Year', 'Billion $COP')
            
            
            
            list_indicadores =  terridata.listar_ind_terridata_sector(df_total, nSector)
            
            indicador = st.selectbox("Selecciona el indicador", list_indicadores, format_func=lambda x: 'Selecciona una opción' if x == '' else x)
            
            
            if indicador:
                with st.spinner("Analizando el indicador {}: ".format(indicador)):
                    
                    st.write("** Analisis de {}:**".format(indicador))
                    terridata_df = df_total[df_total['sector'] == nSector].copy()
                    terridata_df = terridata_df[terridata_df['year'].isin(tags) == True]
                    terridata.get_results_td1(terridata_df,indicador)
                
            
    
    tags = None


if __name__ == "__main__":
    write()
