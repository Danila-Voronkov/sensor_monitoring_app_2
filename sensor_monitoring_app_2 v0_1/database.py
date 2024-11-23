# database.py

import mysql.connector
from config import DB_CONFIG
from datetime import datetime, timedelta
from flask_socketio import emit

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        auth_plugin='mysql_native_password'
    )

def process_datetime(records):
    """Обрабатывает объекты datetime, преобразуя их в строки."""
    for record in records:
        if 'time' in record and isinstance(record['time'], datetime):
            record['time'] = record['time'].strftime('%Y-%m-%d %H:%M:%S')
    return records

def fetch_sensor_data_range(sensor_type, start_time, end_time):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    
    query = 'SELECT * FROM sensor_data WHERE Sensor_id = %s AND Time BETWEEN %s AND %s ORDER BY Time'

    cursor.execute(query, (sensor_type, start_time, end_time))
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return process_datetime(result)

def fetch_sensor_data(sensor_type=None):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    
    if sensor_type:
        query = "SELECT * FROM sensor_data WHERE Sensor_id = %s ORDER BY Time"
        cursor.execute(query, (sensor_type,))
    else:
        query = "SELECT * FROM sensor_data ORDER BY Time"
        cursor.execute(query)
        
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return process_datetime(result)

def fetch_sensor_data_last_minute(sensor_type=None):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    
    time_threshold = datetime.now() - timedelta(minutes=1)
    
    if sensor_type:
        query = "SELECT * FROM sensor_data WHERE Sensor_id = %s AND Time >= %s ORDER BY Time"
        cursor.execute(query, (sensor_type, time_threshold))
    else:
        query = "SELECT * FROM sensor_data WHERE Time >= %s ORDER BY Time"
        cursor.execute(query, (time_threshold,))
        
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return process_datetime(result)