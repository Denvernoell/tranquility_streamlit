import streamlit as st
st.title('Tranquillity Data Platform')
import pandas as pd

from sqlalchemy import create_engine,inspect
def connect_to_postgres(username,password,host,database):
	engine = create_engine(f"postgresql://{username}:{password}@{host}:5432/{database}")  
	return engine

def ag_water():
	engine = connect_to_postgres(	
		username='postgres',
		password=st.secrets['password'],
		host=st.secrets['host'],
		database='postgres',
	)
	return engine

# @st.experimental_singleton
def init_connection():
    # return psycopg2.connect(**st.secrets["postgres"])
	con = ag_water()
	st.session_state['con'] = con
	inspector = inspect(con)
	table_names = [i for i in inspector.get_table_names() if i.find('TID_') != -1]
	dfs = {name:pd.read_sql_table(f"{name}",con).drop(columns=["index"]) for name in table_names}
	table_names = [i for i in dfs.keys()]
	st.session_state['dfs'] = dfs
	return con



def login_page():
	with st.form(key='login'):
		user = st.text_input("Username")
		password = st.text_input("Password", type="password")
		submit_button = st.form_submit_button("Log in")

	if submit_button:
		if (user == st.secrets['login_username'] and password == st.secrets['login_password']):
			st.success('Logged in')
			st.session_state['Logged In'] = True
			init_connection()

			# using Excel
			# file_path = r"\\ppeng.com\pzdata\clients\Tranquillity ID-1075\Ongoing-1075\2000-Data Management System\data\cleaned_data_for_database.xlsx"
			# dfs = pd.read_excel(file_path,sheet_name=None)
			# st.session_state['dfs'] = dfs

			# st.markdown("Logged in")

try:
	if st.session_state['Logged In']:
		st.success('Logged in')
	else:
		login_page()
except:
	st.session_state['Logged In'] = False
	login_page()