# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:04:29 2023

@author: emmylynne

a streamlit app to track Pepper's weight loss
"""

import streamlit as st
import pandas as pd
import altair as alt
# from PIL import Image


# im = Image.open(r'C:\Users\User\OneDrive\Documents\pepper_weight_st\pep_icon.jpg')


st.set_page_config(layout="wide", page_title="Pepper's Weight Tracker") #page_icon = im
hide_default_format = """
       <style>
       
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


pep_df = pd.read_csv('pepper_weight_history.csv')
pep_df['Date'] = pd.to_datetime(pep_df['Date'], 
                                infer_datetime_format=True)
pep_df['Weight'] = pep_df[['Pounds', 'Ounces']].apply(
    lambda x: x[0] + x[1]/16, axis = 1)

pep_df['Weight Loss (from last measurement)'] = pep_df['Weight'].diff()


#build streamlit dashboard
st.title("Pepper's Weight Tracker 🐩")

st.header('Stats')
top_stats = st.columns(3)

latest_weight = pep_df.tail(1)['Weight']
latest_weight_loss = pep_df.tail(1)['Weight Loss (from last measurement)'].item()
top_stats[0].metric(label = 'Latest weight (lbs)', 
                    value = latest_weight,
                    delta = latest_weight_loss,
                    delta_color = 'inverse')

total_weight_loss = pep_df['Weight'].max() - pep_df['Weight'].min()
top_stats[1].metric(label = 'Total weight loss (lbs)',
                          value = total_weight_loss)

with top_stats[2]:
    yay_button = st.button(label = "Yay Pepper!")
    # top_stats[2] = yay_button
    if yay_button:
        st.balloons()

latest_date = pep_df['Date'].max().strftime('%B %d, %Y')
st.info(f"Data current as of {latest_date}")


#charts
left, right = st.columns(2)

weight_hist = alt.Chart(pep_df).mark_line(color = "#738a6b", point=True).encode(
    x="Date",
    y=alt.Y("Weight", scale = alt.Scale(zero=False)),
)
rules = alt.Chart(pd.DataFrame({
  'Date': ['2023-03-13']
})).mark_rule(color = "#6d7070", strokeDash = [1,3]).encode(
  x='Date:T'
)

with left:
    st.header('Weight history')
    
    st.altair_chart(weight_hist + rules, use_container_width=True)


weight_hist = alt.Chart(pep_df).mark_line(color="#a37272", point = True).encode(
    x="Date",
    y=alt.Y("Weight Loss (from last measurement)", 
            scale = alt.Scale(zero=False))
)

with right:
    st.header('Weight loss history')
    st.altair_chart(weight_hist + rules, use_container_width=True)

st.markdown("_Dashed line at March 2023 marks Pepper starting PT._")

st.divider()
st.header('Raw Data')
st.dataframe(pep_df, height = 300)