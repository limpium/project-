import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DATABASE_NAME, USER, PASSWORD, HOST, PORT

def initialize_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE {DATABASE_NAME} OWNER {USER};")
        print(f"Database'{DATABASE_NAME}'  with owner {USER} created successfully.")

        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error: {error}")

def setup_tables():
    try:
        connection = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE Satellites (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            lifetime INT,
            orbit_radius FLOAT 
        );
        """)

        cursor.execute("""
        CREATE TABLE TvChannels (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            language VARCHAR(100),
            specifics VARCHAR(255),
            company VARCHAR(255)
        );
        """)

        cursor.execute("""
        CREATE TABLE Broadcasts (
            id SERIAL PRIMARY KEY,
            coverage_from FLOAT,
            coverage_to FLOAT,
            satellite_id INT,
            tv_channel_id INT,
            FOREIGN KEY (satellite_id) REFERENCES Satellites(id),
            FOREIGN KEY (tv_channel_id) REFERENCES TvChannels(id)
        );
        """)

        print("Tables'Satellites', 'TvChannels' и 'Broadcasts' suc")

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    initialize_database()  
    setup_tables()      
