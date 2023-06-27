import mysql.connector
import csv
import pandas as pd
import streamlit as st
import pymysql
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import json
import plotly.express as px
import pydeck as pdk
from urllib.request import urlopen

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin1",
    database='Phonepepulse'
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

CREATE_TABLE_QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS AggregatedTransaction (
        type VARCHAR(50),
        count INT,
        amount INT,
        name VARCHAR(50),
        state VARCHAR(50),
        year INT,
        file_number INT

    )
    """,
    """
    CREATE TABLE IF NOT EXISTS AggregatedUser (
        brand VARCHAR(50),
        count INT,
        percentage FLOAT,
        name VARCHAR(50),
        state VARCHAR(50),
        year INT,
        file_number INT
    )
    """,
    """
        CREATE TABLE IF NOT EXISTS MapTransaction (
            district VARCHAR(50),
            count INT,
            amount FLOAT,
            state VARCHAR(50),
            year INT,
            file_number INT
        )
        """,
    """
        CREATE TABLE IF NOT EXISTS MapUser (
            district VARCHAR(50),
            registeredUsers INT,
            appOpens INT,
            state VARCHAR(50),
            year INT,
            file_number INT
        )
        """,
    """
        CREATE TABLE IF NOT EXISTS TopTransaction (
            district VARCHAR(50),
            count INT,
            amount FLOAT,
            state VARCHAR(50),
            year INT,
            file_number INT
        )
        """,
    """
        CREATE TABLE IF NOT EXISTS TopUser (
            district VARCHAR(50),
            registeredUsers INT,
            state VARCHAR(50),
            year INT,
            file_number INT
        )
        """

    # Add more CREATE TABLE statements for each table
]

# Create tables
for query in CREATE_TABLE_QUERIES:
    cursor.execute(query)

# Commit the changes to the database
connection.commit()


def insert_csv_data(table_name, csv_file_path):
    # Establish a connection to the MySQL database
    # Open the CSV file
    with open(csv_file_path, 'r') as file:
        csv_data = csv.reader(file)
        header = next(csv_data)

        query = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ({', '.join(['%s'] * len(header))})"

        # Insert each row into the MySQL table
        for row in csv_data:
            # Prepare the INSERT query
            # query = f"INSERT INTO {table_name} VALUES (%s, %s, %s)"

            # Execute the query with row values
            cursor.execute(query, tuple(row))

        # Commit the changes to the database
        connection.commit()

    # Close the cursor and the connection


# Call the insert_csv_data function for each CSV file
csv_files = {
    'AggregatedTransaction': 'D:\ML DSM\Phonepe Project/AggregatedTransaction.csv',
    'AggregatedUser': 'D:\ML DSM\Phonepe Project/AggregatedUser.csv',
    'MapTransaction': 'D:\ML DSM\Phonepe Project/MapTransaction.csv',
    'MapUser': 'D:\ML DSM\Phonepe Project/MapUser.csv',
    'TopTransaction': 'D:\ML DSM\Phonepe Project/TopTransaction.csv',
    'TopUser': 'D:\ML DSM\Phonepe Project/TopUser.csv',
}

for table_name, csv_file_path in csv_files.items():
    insert_csv_data(table_name, csv_file_path)

# def fetch_data(query):
# Execute the query
# cursor.execute(query)

# Fetch all rows of the result
# rows = cursor.fetchall()

# Print or process the fetched data as needed
# df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
# print(df)

# Example queries
# query1 = "SELECT * FROM MapTransaction"
# Call the fetch_data function with the queries

# fetch_data(query1)
# fetch_data(query2)
# fetch_data(query3)

st.title('Phone pe pulse')
# Set the background image CSS style
background_style = """
<style>
body {
    background-color: #391c59;  /* Replace with your desired background color */
}
</style>
"""

# Render the background color style using Streamlit
st.markdown(background_style, unsafe_allow_html=True)

st.subheader('Data base Queries')
question_tosql = st.selectbox('**Select your Question**',
                              ('--Select--',
                               '1. What are the Top 5 Transactions made in Andhra Pradesh?',
                               '2. In 2022, Display the Top 10 Mobile Brands?',
                               '3. Display the Top 10 Transaction names?',
                               '4. What are the Top 10 Transactions for year 2020?',
                               '5. What are Top 5 states where Samsung is used most?',
                               '6. Which district has more Transactions?',
                               '7. Top Registerd Users in each district with app Open?',
                               '8. Top Registerd Users in each district?',
                               '9. Top transactioned Amount by each state?',
                               '10. Top users from each state?'),
                              key='collection_question')

# Creating an connection to SQL
connect_for_question = pymysql.connect(host='localhost', user='root', password='Admin1', db='phonepepulse')
cursor = connect_for_question.cursor()

# Q1
if question_tosql == '1. What are the Top 5 Transactions made in Andhra Pradesh?':
    col1, col2 = st.columns(2)
    with col1:
        cursor.execute(
            "SELECT name,state, COUNT(*) AS name_count FROM AggregatedTransaction WHERE state = 'Andhra Pradesh' GROUP BY name ORDER BY name_count DESC LIMIT 10;")
        result_1 = cursor.fetchall()
        df1 = pd.DataFrame(result_1, columns=['name', 'state', 'name_count']).reset_index(drop=True)
        df1.index += 1
        st.dataframe(df1)
    with col2:
        fig_vc = px.bar(df1, y='name_count', x='name', text_auto='.2s', title="Top users in states", )
        fig_vc.update_traces(textfont_size=16, marker_color='#1308C2')
        fig_vc.update_layout(title_font_color='#E6064A ', title_font=dict(size=30))
        st.plotly_chart(fig_vc, use_container_width=True)


# Q2
elif question_tosql == '2. In 2022, Display the Top 10 Mobile Brands?':

    cursor.execute(
        "SELECT brand, year, COUNT(*) As usage_count FROM AggregatedUser WHERE year=2022 GROUP BY brand ORDER BY usage_count DESC LIMIT 10;")
    result_2 = cursor.fetchall()
    df2 = pd.DataFrame(result_2, columns=['brand', 'usage_count', 'year']).reset_index(drop=True)
    df2.index += 1
    st.dataframe(df2)

# Q3
elif question_tosql == '3. Display the Top 10 Transaction names?':

    cursor.execute("SELECT name, amount, count, state, year FROM AggregatedTransaction ORDER BY count DESC LIMIT 10;")
    result_3 = cursor.fetchall()
    df3 = pd.DataFrame(result_3, columns=['name', 'amount', 'count', 'state', 'year']).reset_index(drop=True)
    df3.index += 1
    st.dataframe(df3)

# Q4
elif question_tosql == '4. What are the Top 10 Transactions for year 2020?':

    cursor.execute(
        "SELECT name, year, state FROM AggregatedTransaction WHERE year=2020 GROUP BY name, state ORDER BY count(*) LIMIT 10;")
    result_4 = cursor.fetchall()
    df4 = pd.DataFrame(result_4, columns=['name', 'year', 'state']).reset_index(drop=True)
    df4.index += 1
    st.dataframe(df4)

# Q5
elif question_tosql == '5. What are Top 5 states where Samsung is used most?':
    col1, col2 = st.columns(2)
    with col1:
        cursor.execute(
            "SELECT brand, state FROM AggregatedUser WHERE brand='Samsung' GROUP BY state ORDER BY count(*) DESC LIMIT 5;")
        result_5 = cursor.fetchall()
        df5 = pd.DataFrame(result_5, columns=['brand', 'state']).reset_index(drop=True)
        df5.index += 1
        st.dataframe(df5)
    with col2:
        fig_vc = px.pie(df5, names='state')
        st.plotly_chart(fig_vc, use_container_width=True)

# Q6
elif question_tosql == '6. Which district has more Transactions?':

    cursor.execute(
        "SELECT district, transaction_count FROM (SELECT district, COUNT(*) AS transaction_count, 'MapTransaction' AS table_name FROM MapTransaction GROUP BY district ORDER BY transaction_count DESC LIMIT 5 ) AS mt UNION ALL SELECT district, transaction_count FROM ( SELECT district, COUNT(*) AS transaction_count, 'TopTransaction' AS table_name FROM TopTransaction GROUP BY district ORDER BY transaction_count DESC LIMIT 5) AS tt ORDER BY transaction_count DESC;")
    result_6 = cursor.fetchall()
    df6 = pd.DataFrame(result_6, columns=['district', 'transaction_count']).reset_index(drop=True)
    df6.index += 1
    st.dataframe(df6)

# Q7
elif question_tosql == '7. Top Registerd Users in each district with app Open?':

    cursor.execute(
        "SELECT district, MAX(registeredUsers) AS maxRegisteredUsers, MAX(appOpens) AS maxAppOpens FROM MapUser GROUP BY district ORDER BY maxRegisteredUsers DESC LIMIT 10;")
    result_7 = cursor.fetchall()
    df7 = pd.DataFrame(result_7, columns=['district', 'registeredUsers', 'appOpens']).reset_index(drop=True)
    df7.index += 1
    st.dataframe(df7)

# Q8
elif question_tosql == '8. Top Registerd Users in each district?':

    cursor.execute(
        "SELECT district, MAX(registeredUsers) AS maxRegisteredUsers FROM MapUser GROUP BY district ORDER BY maxRegisteredUsers DESC LIMIT 10;")
    result_8 = cursor.fetchall()
    df8 = pd.DataFrame(result_8, columns=['district', 'maxRegisteredUsers']).reset_index(drop=True)
    df8.index += 1
    st.dataframe(df8)

# Q9
elif question_tosql == '9. Top transactioned Amount by each state?':

    col1, col2 = st.columns(2)
    with col1:
        cursor.execute(
            "SELECT state, MAX(amount) AS maxAmount FROM TopTransaction GROUP BY state")
        result_9 = cursor.fetchall()
        df9 = pd.DataFrame(result_9, columns=['state', 'maxAmount']).reset_index(drop=True)
        df9.index += 1
        st.dataframe(df9)

    with col2:
        fig_vc = px.bar(df9, y='maxAmount', x='state', text_auto='.2s', title="Top users in states", )
        fig_vc.update_traces(textfont_size=16, marker_color='#1308C2')
        fig_vc.update_layout(title_font_color='#E6064A ', title_font=dict(size=30))
        st.plotly_chart(fig_vc, use_container_width=True)

# Q10
elif question_tosql == '10. Top users from each state?':

    col1, col2 = st.columns(2)
    with col1:
        cursor.execute(
            "SELECT state, MAX(registeredUsers) AS maxUsers FROM TopUser GROUP BY state")
        result_10 = cursor.fetchall()
        df10 = pd.DataFrame(result_10, columns=['state', 'maxUsers']).reset_index(drop=True)
        df10.index += 1
        st.dataframe(df10)

    with col2:
        fig_vc = px.bar(df10, y='maxUsers', x='state', text_auto='.2s', title="Top users in states", )
        fig_vc.update_traces(textfont_size=16, marker_color='#1308C2')
        fig_vc.update_layout(title_font_color='#E6064A ', title_font=dict(size=30))
        st.plotly_chart(fig_vc, use_container_width=True)

cursor.close()
connection.close()

connect_for_question.close()