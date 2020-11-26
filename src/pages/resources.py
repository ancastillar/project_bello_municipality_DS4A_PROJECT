"""Esta página te permite convertir excel en datos valiosos con un solo clic"""
import logging

import streamlit as st
from listener_twitter import TwStreamListener
import awesome_streamlit as ast
from awesome_streamlit.core.services import resources
import pandas as pd
from Preprocess import DF_prep
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from graficar import graph_sam

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
bBandera = True

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

def write():
    global bBandera
    global df_total_x
    """Writes content to the app"""
    ast.shared.components.title_awesome("Estadistica general")

    
    tags = ast.shared.components.multiselect(
        "Selecciona la fuente de los datos", options=['SIEE'], default=[]
    )

    if not tags:
        st.info(
             """Para continuar por favor **selecciona la fuente de datos que te gustaria analizar**"""
        )
    if tags:
        
        if bBandera:
            st.info(__doc__)
            st.markdown(STYLE, unsafe_allow_html=True)
            file = st.file_uploader("Sube el archivo del SIEE", type=["xlsx"])
            show_file = st.empty()
            if not file:
                show_file.info("Por favor sube el archivo en formato: " + ", ".join(["xlsx"]))
                return

            
        with st.spinner("Analizando tu data en segundos  ..."):

            years = st.multiselect(
                "Selecciona los años que deseas visualizar", options=['2016', '2017', '2018', '2019'], default=['2016', '2017', '2018', '2019']
            )

            author = st.selectbox("Selecciona un sector", options=['Salud', 'Medio ambiente', 'Educación', 'Seguridad'])
            
            if not years:
                st.info(
                     """Para continuar por favor **selecciona los años que te gustaria analizar**"""
                )
            if years:
                if bBandera:
                   cleaner_obj = DF_prep()
                   cleaner_obj.load_file(file)
                   df_total_x = cleaner_obj.get_concat_df()
                   bBandera = False
                
                fig, ax = plt.subplots(figsize=(12, 5))
                
                if author == 'Salud':
                    nSector = 2
                elif author == 'Medio ambiente':
                    nSector = 10
                elif author == 'Educación':
                    nSector = 1
                else:
                    nSector = 18
                    
                    
                
                df_total = df_total_x
                
                
                #st.write("## **Avance general por sectores y años::**")
                df_total['ratio_avance'] = df_total['valor_esperado'] / df_total['valor_ejecutado']
                df_general = df_total[df_total['year'].isin(years) == True]
                
                
                
                sector_labels = ['Salud', 'Medio ambiente', 'Educación', 'Seguridad']
                year_labels = years
       
                #graph_sam.plotly_bars(df_general, 'sector', 'ratio_avance', 'year', year_labels, sector_labels, 'mean', '', 'Percent [%]')
                           
            
                #st.write("## **Avance general por sectores y años::**")
                df_total['ratio_avance'] = df_total['valor_esperado'] / df_total['valor_ejecutado']
                df_general = df_total[df_total['year'].isin(years) == True]

                sector_labels = [author]

                year_labels = years
            
                #graph_sam.plotly_bars(df_general, 'sector', 'ratio_avance', 'year', year_labels, sector_labels, 'mean', '', 'Percent [%]')

                
                st.write("## **Rango de clasificación por años:**")
                
                df_sectors = [author]
                df_clasificacion = df_total[df_total['sector'] == nSector].copy()
                df_clasificacion = df_clasificacion[df_clasificacion['year'].isin(years) == True]
                graph_sam.clasificacion(df_clasificacion, df_sectors)
                           
                
                
                df_presupuesto = df_total[df_total['sector'] == nSector].copy()
                df_presupuesto = df_presupuesto[df_presupuesto['year'].isin(years) == True]
                
                
                sector_labels = [author]

                year_labels = years
                
                auth_sect = st.selectbox("Selecciona un tipo de grafica para visualizar el presupuesto", options=['Año', 'Sector'])
                
        
                
                if auth_sect == 'Año':
                    st.write("## **Total de recursos por año:**")
                    graph_sam.plotly_bars(df_presupuesto, 'year', 'ejec_total', 'sector', sector_labels, year_labels, 'sum', '', 'Billion $COP', b_mode='stack', color='clown')
                else:
                    st.write("## **Total de recursos por sector y año:**")
                    graph_sam.plotly_bars(df_presupuesto, 'sector', 'ejec_total', 'year', year_labels, sector_labels, 'sum', '', 'Billion $COP')
                    
                    
            

    
    tags = None
    

if __name__ == "__main__":
    
    write()
