import streamlit as st
import sys
sys.path.append('..')
from plotly_figures import create_dtw_figure
import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow
get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M").format("MMMM YYYY")
add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])

def export_df(df,file_name):
	towrite = io.BytesIO()
	downloaded_file = df.to_excel(towrite, encoding='utf-8', index=True, header=True)
	towrite.seek(0)  # reset pointer
	b64 = base64.b64encode(towrite.read()).decode()  # some strings
	linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download excel file</a>'
	# return linko
	st.markdown(linko, unsafe_allow_html=True)
	


st.title('Tranquillity Wells')
table_name = 'TID_extractions_monthly_AF'
if st.session_state['Logged In']:
	df = st.session_state.dfs[table_name]
	
else:
	st.markdown('Not logged in')

