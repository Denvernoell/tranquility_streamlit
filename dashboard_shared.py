import streamlit as st
import sys
# sys.path.append('..')
# from plotly_figures import create_extractions_figure
import plotly.graph_objects as go
import pandas as pd

import base64
import io
import webbrowser

import arrow

class Components:
	def __init__(self,name):
		self.name = name
	def header(self):
		st.title(f"{self.name} Data Management System")
	def footer(self):
		st.markdown(f"Provost & Pritchard Consulting Group - 2023")


def export_df(df,file_name,index=True,header=True):
	towrite = io.BytesIO()
	downloaded_file = df.to_excel(towrite, encoding='utf-8', index=index, header=header)
	towrite.seek(0)  # reset pointer
	b64 = base64.b64encode(towrite.read()).decode()  # some strings
	linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download excel file</a>'
	# return linko
	st.markdown(linko, unsafe_allow_html=True)


def show_pdf(file_path):
	with open(file_path,"rb") as f:
		base64_pdf = base64.b64encode(f.read()).decode('utf-8')
		pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'		
		st.markdown(pdf_display, unsafe_allow_html=True)

def download_pdf(file_path):
		
	with open(file_path, "rb") as pdf_file:
		PDFbyte = pdf_file.read()

	st.download_button(label="Download PDF Tutorial", 
			data=PDFbyte,
			file_name="pandas-clean-id-column.pdf",
			mime='application/octet-stream')


def convert_date(df,col):
	df[col] = df[col].pipe(pd.to_datetime)
	return df

class Table:
	def __init__(self,client,table_name):
		"""
		client: supabase connection
		table_name: table name of supabase table
		"""
		self.client = client
		self.table_name = table_name
		self.refresh()
	
	def __repr__(self) -> str:
		return f"Table Name = {self.table_name}"
	
	def refresh(self):
		self.df = pd.DataFrame(self.client.table(self.table_name).select('*').execute().data)
	
	def append(self,data):
		"""
		data; dict {"client":"Aliso"}
		"""
		self.client.table(self.table_name).insert(data).execute()
		self.refresh()

	def edit(self,data,locator):
		"""
		data: dict {"client":"Aliso"}
		locator: list ["id",1]
		"""
		self.client.table(self.table_name).update(data).eq(locator).execute()
		self.refresh()

	def delete(self,locator):
		"""
		locator: list ["id",1]
		"""
		self.client.table(self.table_name).delete().eq(locator).execute()
		self.refresh()