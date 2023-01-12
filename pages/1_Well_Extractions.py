import streamlit as st
import sys
sys.path.append('..')
from plotly_figures import create_extractions_figure
import plotly.graph_objects as go
import pandas as pd

import base64
import io
import webbrowser

import arrow

def export_df(df,file_name):
	towrite = io.BytesIO()
	# downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
	downloaded_file = df.to_excel(towrite, encoding='utf-8', index=True, header=True)
	towrite.seek(0)  # reset pointer
	b64 = base64.b64encode(towrite.read()).decode()  # some strings
	linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download excel file</a>'
	# return linko
	st.markdown(linko, unsafe_allow_html=True)
	
def get_table(table_name):
	return pd.DataFrame(st.session_state['client'].table(table_name).select('*').execute().data)

st.title('Tranquillity Wells')
if st.session_state['Logged In']:
	df = get_table('TID_extractions_monthly_AF')
	# df = st.session_state.dfs['TID_extractions_monthly_AF']
	wells = [i for i in df['well_id'].unique()]
	wells_to_use = st.multiselect("Wells",wells,default=wells)
	if wells_to_use:
		data = df.loc[df['well_id'].isin(wells_to_use)]
		get_date = lambda year,month: arrow.get(f"{year}-{month}","YYYY-M")#.format("MMMM YYYY")
		add_date = lambda df: df.assign(date = [get_date(y['year'],y['month']) for i,y in df.iterrows()])
		data = data.pipe(add_date)
		st.plotly_chart(create_extractions_figure(data))

		pivot = pd.pivot_table(data,values=['monthly_extraction_AF'],index=['date'],columns=['well_id'],margins=True,margins_name="Total",aggfunc=sum).droplevel(0,axis='columns')

		
		# to_month_year = lambda y: arrow.get(y).format("M YYYY")
		pivot.index = [i.format('MMMM YYYY') for i in pivot.index]

		# if st.button('Graph'):
		# if st.button('Table'):
		# st.dataframe(pivot.style.applymap(lambda x: 'color: transparent' if pd.isnull(x) else '').format(formatter="{:.2f}"))
		st.dataframe(pivot.style.applymap(lambda x: 'color: transparent' if x == 0 or pd.isnull(x) else '').format(formatter="{:.2f}"))
		# st.markdown(pivot.index)

			# st.dataframe(data)

		# if st.button('Download'):
		# export_df(data,"Extractions.xlsx")
		export_df(pivot,"Extractions.xlsx")
		# st.download_button('Download',link)
	
else:
	st.markdown('Not logged in')

