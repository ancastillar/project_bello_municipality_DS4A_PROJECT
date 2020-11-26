

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objs as go


class terridata:
    ##funcion donde entre sector, indicador o indicadores y año o años y grafique
    def get_results_td(df, sector, years, indicadores):
        terridata_df_sector = df[(df['sector'] == sector) & (df['year'].isin(years))]
        terridata_df_m_g = terridata_df_sector[['td_indicador','year','td_ind_value']]
        terridata_df_m_g = terridata_df_m_g[terridata_df_m_g.td_indicador.notnull()]
        if terridata_df_m_g.shape[0] > 0:
            graph = terridata_df_m_g.pivot(index='td_indicador',columns='year',values='td_ind_value')
        
        
        
        st.write("## **Indicador {}:**".format(indicadores))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=graph.loc[indicadores,:].T.index,y=graph.loc[indicadores,:].T[indicadores[0]],mode='lines+markers',name=indicadores[0]))
        
        fig.update_layout( xaxis = dict(tickmode = 'linear',tick0 = 2013,dtick = 1),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        
        
        fig.layout.update(legend_title_text='Trend')
        st.plotly_chart(fig)
        
        
        '''
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=graph.loc[indicadores,:].T)
        st.write("## **Indicador {}:**".format(indicadores))
        st.pyplot(fig)
        '''


    ##lista de indicadores por sector: seguridad:18, educacion:1, salud:2, ambiente:10
    def listar_ind_terridata_sector(df, sector):
        td_sector = df[(df['sector'] == sector) & (df.td_indicador.notnull())]
        td_sector_ind = td_sector[['td_indicador']]
        lista_sector = set(td_sector_ind.td_indicador.values.tolist())
        lista_espera = list(lista_sector)
        lista_espera.insert(0, '')
        
        array_sector = np.array(lista_espera)
        return array_sector

        
    def get_results_td1(terridata_df_sector, indicadores):
        
        terridata_df_m_g = terridata_df_sector[['td_indicador','year','td_ind_value']]
        terridata_df_m_g = terridata_df_m_g[terridata_df_m_g.td_indicador.notnull()]
        if terridata_df_m_g.shape[0] > 0:
            graph = terridata_df_m_g.pivot(index='td_indicador',columns='year',values='td_ind_value')
        plt.figure(figsize=(10,10))
        x_variable = graph.loc[indicadores,:].T.index
        y_var = graph.loc[indicadores,:].T

        #y_variable = y_var[indicadores]
        fig = px.scatter(x = x_variable, y = y_var,
                      trendline="lowess",
                     labels=dict(x="Años", y="Valor"))

        fig.update_layout(
         xaxis = dict(
             tickmode = 'linear',
             tick0 = 2013,
             dtick = 1
         ),
        )
        st.plotly_chart(fig)
