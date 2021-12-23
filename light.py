import RPi.GPIO as GPIO
import time
import mysql.connector
from mysql.connector import Error

# GPIO numbering
GPIO.setmode(GPIO.BCM)


# function for establishing a connection to the mySQL server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password)
        print("MySQL Database connection successful")
    except Error as err:
        print({err})
    return connection


# function for connecting to the database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password, database=db_name)
        print("MySQL Database connection successful")
    except Error as err:
        print({err})
    return connection


# function for executing queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print({err})


# connecting to mySQL server
create_server_connection("localhost", "{username}", "{password}")
# variable to hold database connection information
connection = create_db_connection("localhost", "{username}", "{password}", "light")


# this section of code is only necessary if table is not created yet
# create_light_table = """
#    CREATE TABLE light (
#    date DATE,
#    time TIME (0),
#    light FLOAT
#    );
# """
# execute_query(connection, create_light_table)

# function that reads current light level and stores it in the database
def readlight():
    # GPIO setup
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.LOW)
    time.sleep(0.3)
    GPIO.setup(19, GPIO.IN)

    t1 = time.time()
    # while voltage across pin 19 is low / capacitor is not charged
    while GPIO.input(19) == GPIO.LOW:
        continue
    t2 = round((time.time() - t1) * 1000, 3)
    # t2 is the total time it took to charge the capacitor

    # storing data to database
    pop_light = """
        INSERT INTO light VALUES
        (""" + str(time.strftime("%Y%m%d", time.localtime())) + """,
         """ + str(time.strftime("%H%M%S", time.localtime())) + """,
         """ + str(t2) + """)
    """
    execute_query(connection, pop_light)

    return t2


# runs until user intervention
while True:
    readlight()
    time.sleep(2)
