import mysql.connector

def get_alerts_connection():
    # Connect to Alerts database
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="waNdeRingmAn8996",
        database="alerts"
    )
    return conn

def get_camera_connection():
    # Connect to Camera database
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="waNdeRingmAn8996",
        database="camera"
    )
    return conn
