# database.py

import mysql.connector
from config import DB_CONFIG
from datetime import datetime, timedelta

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        auth_plugin='mysql_native_password'
    )

def fetch_sensor_data(sensor_type=None):
    """Получает все данные для указанного типа датчика или всех датчиков, если sensor_type не указан."""
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
    
    return result

def fetch_sensor_data_last_minute(sensor_type=None):
    """Получает данные за последнюю минуту для указанного типа датчика или всех датчиков, если sensor_type не указан."""
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
    
    return result
