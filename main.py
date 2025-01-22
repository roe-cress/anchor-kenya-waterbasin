##created by: caroline cress
##for Anchor Environmental Consultants
##program runs a streamlit interface which shows graphs and choropleth map relaying information about Kenyan water basins
##currently this version on my computer is called 'throwaway.py'
import streamlit as st
import pandas as pd
import geopandas as gpd 
import matplotlib
import numpy as np
import json
import plotly.express as px
import streamlit_vertical_slider as svs
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_float import *

##playing around with float and sidebars

st.set_page_config(layout='wide')

##this initialises the float capability
float_init()

df = pd.read_csv("Kenya_MCDA_Criteria_new.csv")
basin_id = df['Basin_ID2']
roi_score = df['ROI score']
pop_dense = df['Normalised Pop density']
pov_distribute = df['Normalized Poverty Distribution  ']
bio_diverse = df['Biodiversity normalised']
climate_vul = df['Climate_Vulnerability']

def filter_table(table_filtering, input_df):
    intermediate_table = sort_table('Overall score in descending order', input_df)
    if table_filtering == '10':
        filtered_table = intermediate_table.iloc[:10]
    elif table_filtering == '20':
        filtered_table = intermediate_table.iloc[:20]
    elif table_filtering == '50':
        filtered_table = intermediate_table.iloc[:50]
    else:
        filtered_table = input_df
    return filtered_table


def sort_table(order_by, input_df):
    intermediate_table = input_df
    ordered_table = pd.DataFrame(columns=['Basin_ID2','Overall_score'])
    if order_by == 'Overall score in descending order':
        ordered_table = input_df.sort_values('Overall_score', ascending=False)
    elif order_by == 'Basin ID in descending order':
        ordered_table = input_df.sort_values('Basin_ID2', ascending=False)
    elif order_by == 'Overall score in ascending order':
        ordered_table = input_df.sort_values('Overall_score', ascending=True)
    elif order_by == 'Basin ID in ascending order':
        ordered_table = input_df.sort_values('Basin_ID2', ascending=True)

    return ordered_table

col2, col1 = st.columns([1,2])
with col2.container(height=1000):
    con1 = st.container(border=True)
    con2 = st.container(border=True)
    with con1:
        st.subheader('Input your weightings:')
        slider1, slider2, slider3, slider4, slider5 = st.columns(5)
        with slider1:
            bio_diverse_weight = svs.vertical_slider(label="Bio-diversity weight", default_value=0, min_value=0, max_value=100, track_color="#7AD15188", slider_color="#7AD151FF", thumb_color="#7AD151FF", value_always_visible=True)
        with slider2:
            pop_dense_weight = svs.vertical_slider(label="Population density weight", default_value=0, min_value=0, max_value=100, track_color="#2A788E88", slider_color="#2A788EFF", thumb_color="#2A788EFF", value_always_visible=True)
        with slider3:
            roi_weight = svs.vertical_slider(label="ROI weight", default_value=0, min_value=0, max_value=100, track_color="#41448788", slider_color="#414487FF", thumb_color="#414487FF", value_always_visible=True)
        with slider4:
            pov_distribute_weight = svs.vertical_slider(label="Poverty distribution weight", default_value=0, min_value=0, max_value=100, track_color="#22A88488", slider_color="#22A884FF", thumb_color="#22A884FF", value_always_visible=True)
        with slider5:
            climate_vul_weight = svs.vertical_slider(label="Climate vulnerability weight", default_value=0, min_value= 0, max_value=100, track_color="#FDE72588", slider_color="#FDE725FF", thumb_color="#FDE725FF", value_always_visible=True)
    with con2:
        st.subheader('View your weightings percentages below:')
        weighted_score = roi_score*roi_weight + pop_dense*pop_dense_weight + pov_distribute*pov_distribute_weight + bio_diverse*bio_diverse_weight + climate_vul*climate_vul_weight
        max_score = max(weighted_score)
        weighted_score = (weighted_score/max_score)*100
        weighted_df = pd.DataFrame(
                {'Basin_ID2': basin_id,
                'Overall_score': weighted_score,
                'ROI': roi_score,
                'Population Density': pop_dense,
                'Poverty Distribution': pov_distribute,
                'Bio-diversity': bio_diverse,
                'Climate Vulnerability': climate_vul}
        )
        aspects_weighted_data = [['ROI', roi_weight],['Population density', pop_dense_weight],['Poverty Distribution', pov_distribute_weight],['Bio-diversity', bio_diverse_weight],['Climate vulnerability', climate_vul_weight]]
        aspects_weighted_df = pd.DataFrame(aspects_weighted_data)
        aspects_weighted_df.columns = ['Aspect', 'Weighting']
        palette = ['#414487FF','#2A788EFF', '#22A884FF', '#7AD151FF', '#FDE725FF']
        pie_c = go.Figure(
            data=[
                go.Pie(
                    labels=aspects_weighted_df['Aspect'],
                    marker={'colors':palette},                                
                    values=aspects_weighted_df['Weighting'],
                )
            ]
        )
        pie_c.update_traces(
            hoverinfo='label+percent',
            textinfo='percent',
            textfont_size=15
        )
        st.plotly_chart(pie_c, use_container_width=True)

col2.float("height: 82%")

with col1:
    up_con = st.container(border=True)
    with up_con:
        up_con_l, up_con_r = st.columns(2)

        with up_con_l:
            sbox_order_label = 'Choose how you would like the table below to be ordered'
            sbox_order_options = ['Overall score in descending order', 'Overall score in ascending order', 'Basin ID in descending order', 'Basin ID in ascending order']
            table_ordering = st.selectbox(sbox_order_label, sbox_order_options)
        with up_con_r:
            sbox_filter_label = 'Choose how many rows should be shown in the table below'       
            sbox_filter_options = ['10', '20', '50', 'all']
            table_filtering = st.selectbox(sbox_filter_label, sbox_filter_options)

        use_this_df = filter_table(table_filtering=table_filtering, input_df=weighted_df)
        use_this_df = sort_table(order_by=table_ordering, input_df=use_this_df)


    innercol_left, innercol_right = st.columns([3,2])
    with innercol_left:
        shapefile= gpd.read_file('WRA_SubBasins_v2_added_variables.shp')
        shapefile = shapefile.merge(weighted_df, on='Basin_ID2')
        fig, ax = plt.subplots(1, figsize=(10, 6))
        ax.axis('off')
        ax.set_facecolor("red")
        ax.set_title('waterbasin investments in kenya', fontdict={'fontsize': '15', 'fontweight' : '3'})
        shapefile.plot(column='Overall_score',
                    cmap='inferno_r',
                    linewidth=0.2,
                    ax=ax,
                    edgecolor='1',
                    legend=True, missing_kwds={
                    "color": "lightgrey",
                    "label": "Missing values",},)
        fig.savefig('look_at_this_graph.jpg',bbox_inches='tight', dpi=300)

        st.pyplot(fig)
    
    with innercol_right:
        st.subheader('Waterbasin Data')
        st.dataframe(use_this_df,
                 column_order=("Basin_ID2", "Overall_score"),
                 width=None,
                 column_config={
                    "Basin_ID2": st.column_config.NumberColumn(
                        "Basin ID",
                    ),
                    "Overall_score": st.column_config.ProgressColumn(
                        'Overall score',
                        help='To sort this column, click at the top of the column to adjust whther it is sorted in ascending or descending order',
                        min_value=0,
                        max_value=100,
                        format='%3.0f'
                     ),},
                     hide_index=True, use_container_width=True
                     
                 )

