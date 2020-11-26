

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objs as go


class graph_sam:

    def plotly_bars(temp_df, x_var, y_var, hue_var, hue_labels, x_labels, estimator, title, y_title, b_mode='group', color='Default'):
        colors_1 = {
            0 : 'rgb(213, 187, 103)', # amarillo
            1 : 'rgb(72, 120, 208)',  # azul
            2 : 'rgb(214, 95, 95)',   # rojo
            3 : 'rgb(106, 204, 100)', # verde
            4 : 'rgb(140, 97, 60)',   # cafe
            5 : 'rgb(130, 198, 226)', # azul claro
            6 : 'rgb(238, 133, 74)',  # naranja
            7 : 'rgb(149, 108, 180)', # morado
            8 : 'rgb(220, 126, 192)', # rosa
            9 : 'rgb(121, 121, 121)'  # gris
        }
        colors_2 = {
            0 : 'rgb(69, 13, 84)',
            1 : 'rgb(72, 40, 120)',
            2 : 'rgb(62, 74, 137)',
            3 : 'rgb(48, 104, 142)',
            4 : 'rgb(37, 130, 142)',
            5 : 'rgb(31, 158, 137)',
            6 : 'rgb(53, 183, 121)',
            7 : 'rgb(109, 205, 89)',
            8 : 'rgb(180, 222, 44)',
            9 : 'rgb(253, 231, 37)'
        }
        if color == 'clown':
            colors = colors_1
        else:
            colors = colors_2

        hue_list = sorted(temp_df[hue_var].unique().tolist())
        
        fig = go.Figure()
        for i, h in enumerate(hue_list):
            data = temp_df[temp_df[hue_var] == h].groupby(x_var)[y_var].agg(estimator).sort_index().tolist()
            fig.add_trace(go.Bar(x=x_labels,
                        y=data,
                        name=hue_labels[i],
                        marker_color=colors[i]
                        ))

        fig.update_layout(
            width=750,
            height=600,
            xaxis_tickfont_size=14,
            yaxis=dict(
                title=y_title,
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode=b_mode,
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        st.plotly_chart(fig)


    def clasificacion(df_total, df_sectors):
        r_cal = df_total.groupby('rango_calificacion')['producto'].count().sort_index().reset_index()['rango_calificacion'].tolist()
        #sectors = [df_sectors.set_index('sector').at[x, 'nombre_corto'] for x in sorted(df_total.sector.unique().tolist())]
        years = sorted(df_total.year.unique().tolist())
        colors = {
            0 : 'rgb(69, 13, 84)',
            1 : 'rgb(72, 40, 120)',
            2 : 'rgb(62, 74, 137)',
            3 : 'rgb(48, 104, 142)',
            4 : 'rgb(37, 130, 142)',
            5 : 'rgb(31, 158, 137)',
            6 : 'rgb(53, 183, 121)',
            7 : 'rgb(109, 205, 89)',
            8 : 'rgb(180, 222, 44)',
            9 : 'rgb(253, 231, 37)'
        }

        fig = go.Figure()
        for i, y in enumerate(years):
            data_dict = df_total[df_total['year'] == y].groupby('rango_calificacion')['producto'].count().reset_index().set_index('rango_calificacion')['producto'].to_dict()
            ratio_list = []
            for c in r_cal:
                try:
                    ratio_list.append(data_dict[c])
                except:
                    ratio_list.append(0)
            fig.add_trace(go.Bar(x=r_cal,
                        y=ratio_list,
                        name=str(int(y)),
                        marker_color=colors[i]
                        ))

        fig.update_layout(
            width=750,
            height=600,
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Quantity of products',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        st.plotly_chart(fig)

    
