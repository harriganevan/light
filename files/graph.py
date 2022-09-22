import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password)
        print("MySQL Database connection successful")
    except Error as err:
        print({err})
    return connection


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password, database=db_name)
        print("MySQL Database connection successful")
    except Error as err:
        print({err})
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print({err})


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print({err})


create_server_connection("{Raspberry Pi IP address}", "{username}", "{password}")
connection = create_db_connection("{Raspberry Pi IP address}", "{username}", "{password}", "light")

q1 = "SELECT * FROM light;"
results = read_query(connection, q1)

data = []

for i in results:
    data.append(list(i))

q2 = "SELECT COUNT(*) FROM light;"
length = read_query(connection, q2)


def graph(data):
    plt.ion()
    x = [matplotlib.dates.date2num(datetime.combine(i[0], datetime.min.time()) + i[1]) for i in data]
    y = [i[2] for i in data]

    plt.clf()

    ax = plt.axes()
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))

    ax.plot_date(x, y, 'b-')
    ax.invert_yaxis()

    plt.show(block=True)


graph(data)
