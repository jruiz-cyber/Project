import mysql.connector

def get_camera_connection():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="waNdeRingmAn8996",
        database="camera"      
    )
