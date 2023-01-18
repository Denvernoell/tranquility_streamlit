import streamlit as st
import pandas as pd
import supabase

from dashboard_shared import Table,Components

C = Components("Tranquillity")
C.header()


def login_page():
	with st.form(key='login'):
		user = st.text_input("Username")
		password = st.text_input("Password", type="password")
		submit_button = st.form_submit_button("Log in")

	if submit_button:
		if (user == st.secrets['login_username'] and password == st.secrets['login_password']):
			st.success('Logged in')
			st.session_state['Logged In'] = True
			st.session_state['client'] = supabase.create_client(st.secrets['supabase_url'],st.secrets['supabase_key'])

try:
	if st.session_state['Logged In']:
		st.success('Logged in')
	else:
		login_page()
except:
	st.session_state['Logged In'] = False
	login_page()

C.footer()