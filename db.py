import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="alaskaki",
    user="postgres",
    password="postgres"
)
