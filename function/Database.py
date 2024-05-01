import psycopg2
from ast import literal_eval
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import io
import sys
class Database:
	def __init__(self,db_config,project_config=None):
		self.con = psycopg2.connect(**db_config)
		if project_config!=None:
			self.projectId = project_config['project_id']
			self.calibrationId = project_config['calibration_id']
			self.deploymentId = project_config['deployment_id'] 
		self.cur = self.con.cursor()
	def get_all_projects(self,):
		query = f"SELECT id,project_name FROM projects;"
		self.cur.execute(query)
		rows = self.cur.fetchall()
		ids = []
		project_names = []
		for row in rows:
			project_names.append(row[1])
			ids.append(row[0])
		return project_names,ids
	def get_camaeras_of_a_project(self, project_id):
		query = f"SELECT id,camera_name,camera_setting FROM cameras WHERE project_id='{project_id}';"
		self.cur.execute(query)
		rows = self.cur.fetchall()
		ids = []
		camera_names = []
		camera_setting = []
		for row in rows:
			camera_names.append(row[1])
			ids.append(row[0])
			camera_setting.append(row[2])
		return camera_names,ids,camera_setting
	def get_cc_counts(self,pid,cam_id):
		time_start = datetime.now() - timedelta(minutes=30)
		query = f"SELECT timestamp, value FROM cumulativecounters WHERE project_id='{pid}' AND camera_id='{cam_id}' AND timestamp>='{time_start}' ORDER BY timestamp DESC;"
		self.cur.execute(query)
		rows = self.cur.fetchall()
		return rows
	def get_image(self,pid,cam_id):
		query = f"SELECT url FROM frames WHERE project_id='{pid}' AND camera_id='{cam_id}' ORDER BY timestamp DESC LIMIT 1;"
		self.cur.execute(query)
		result = self.cur.fetchone()
		return result
	def count_insert(self,data):
			self.cur.execute("""
					INSERT INTO cumulativecounters (timestamp, value,camera_id,project_id) 
					VALUES (%s,%s,%s,%s) 
			""", data)
			self.con.commit()
	def get_data(self,start_time,end_time):
		# end_time = datetime.now()
		# start_time = end_time - timedelta(hours=5)
		# Format timestamps for the SQL query
		start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
		end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

		# SQL query to retrieve data for the last 5 hours
		query = f"SELECT timestamp, value FROM your_table WHERE timestamp BETWEEN '{start_time_str}' AND '{end_time_str}';"

		# Fetch data into a DataFrame
		df = pd.read_sql_query(query, conn)
		return df


