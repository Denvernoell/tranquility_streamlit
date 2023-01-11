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
	


st.title('Tranquility Depth to water')
table_name = 'TID_well_depth_to_water_ft'
if st.session_state['Logged In']:
	df = st.session_state.dfs[table_name]
	wells = [i for i in df['well_id'].unique()]
	wells_to_use = st.multiselect("Wells",wells,default=wells)

	# min_date = df['Date'].sort_values().min
	# max_date = df['Date'].sort_values().max
	# dates_to_use = [
	# 	st.date_input("Start",value=min_date,min_value=min_date,max_value=max_date),
	# 	st.date_input("Stop",value=max_date,min_value=min_date,max_value=max_date)
	# 	]

	data = df.loc[df['well_id'].isin(wells_to_use)]
	# data = data.pipe(add_date)
	pivot = pd.pivot_table(data,values=['dtw_ft'],index=['date'],columns=['well_id']).droplevel(0,axis='columns')
	# if st.button('Graph'):
	st.plotly_chart(create_dtw_figure(data))
	# if st.button('Table'):
	to_month_year = lambda y: arrow.get(y).format("MMMM D, YYYY")
	pivot.index = [to_month_year(i) for i in pivot.index]

	st.dataframe(pivot.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '').format(formatter="{:.2f}"))
	export_df(pivot,"DTW.xlsx")
else:
	st.markdown('Not logged in')

