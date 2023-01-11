# "G:\Tranquillity ID-1075\Ongoing-1075\170-O&M\Data Managment System\10_2020 DMS\Well Locations MASTER.xls"

import streamlit as st
import sys
sys.path.append('..')
from plotly_figures import create_subsidence_figure
# import plotly.graph_objects as go
import pandas as pd

import base64
import io

import arrow

import geopandas as gpd
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
	
def to_decimal_degrees(coord):
	C = coord.split(' ')

	decimal_degree = (float(C[0])) + (float(C[1]) / 60) + (float(C[2]) / 60 / 60)
	if C[3] == 'W':
		return decimal_degree * -1
	else:
		return decimal_degree

import leafmap.foliumap as leafmap
# import leafmap.leafmap as leafmap  # for ipyleaflet only


st.title('Tranquility Subsidence')
table_name = 'TID_subsidence_points'
if st.session_state['Logged In']:
	def plot_positions(df,points_to_use):
		df = df.loc[df['point_id'].isin(points_to_use)]	
		df = df.assign(
			lat = lambda y: y.latitude.apply(to_decimal_degrees),
			lon = lambda y: y.longitude.apply(to_decimal_degrees),
		)

		gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(
			df.lon,
			df.lat,
			crs="EPSG:4326"
			))

		M = leafmap.Map(
			google_map="HYBRID",
			draw_control=False,
		)
		# img_path = r'G:\Tranquillity ID-1075\Ongoing-1075\2000-Data Management System\produced\tranquility_streamlit\pages\K1227.png'
		# # img_path = r'K1227.png'
		# url = f'file://{img_path}'
		# popup = f'<img src="{url}"/>"'
		# # popup = f""

		# popup = folium.Popup()
		M.add_gdf(gdf,layer_name="Monuments",info_mode=False)
		for i,y in gdf.iterrows():
			M.add_marker(
				(y.geometry.y,y.geometry.x),
				# popup=y['point_id'],
				# popup=popup,
				tooltip=y['point_id']
				)

		# https://leafmap.org/notebooks/11_linked_maps/#change-basemaps
		# M.add_marker()
		# file_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\GIS\Feature\TID.shp'
		
		file_path = r'data\TID.shp'
		boundary = gpd.read_file(
			file_path,
			# epsg="EPSG:4326",
			epsg='4326',
			)#.to_crs("EPSG:4326")
			# ! figure out why this doesnt work
		# M.add_gdf(boundary,layer_name="Tranquility Boundary",info_mode=None)

		M.to_streamlit()

	def gse(df,points_to_use):
		data = df.loc[df['point_id'].isin(points_to_use)]
		pivot = pd.pivot_table(data,values=['elevation'],index=['date'],columns=['point_id']).droplevel(0,axis='columns')
		st.plotly_chart(create_subsidence_figure(data))

		# st.dataframe(pivot)
		return points_to_use

	positions = st.session_state.dfs['TID_subsidence_points']
	points = [i for i in positions['point_id'].unique()]
	points_to_use = st.multiselect("Points",points,default=points)
	if points_to_use:
		plot_positions(positions,points_to_use)
		elevations = st.session_state.dfs['TID_subsidence_elevations']
		gse(elevations,points_to_use)

else:
	st.markdown('Not logged in')




