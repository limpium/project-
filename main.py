from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from config import DATABASE_NAME, USER, PASSWORD, HOST, PORT

app = FastAPI()

class Satellite(BaseModel):
    name: str
    lifetime: int
    orbit_radius: float

class TvChannel(BaseModel):
    name: str
    language: str
    specifics: str
    company: str

class Broadcast(BaseModel):
    coverage_from: float
    coverage_to: float
    satellite_id: int
    tv_channel_id: int

def get_db_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

@app.get("/satellites/")
def get_satellites():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Satellites;")
    satellites = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"satellites": satellites}

@app.get("/satellites/{satellite_id}")
def get_satellite(satellite_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Satellites WHERE id = %s;", (satellite_id,))
    satellite = cursor.fetchone()
    cursor.close()
    conn.close()
    if satellite is None:
        raise HTTPException(status_code=404, detail="Satellite not found")
    return {"satellite": satellite}

@app.post("/satellites/")
def create_satellite(satellite: Satellite):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Satellites (name, lifetime, orbit_radius)
        VALUES (%s, %s, %s) RETURNING id;
    """, (satellite.name, satellite.lifetime, satellite.orbit_radius))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": new_id, "satellite": satellite}

@app.put("/satellites/{satellite_id}")
def update_satellite(satellite_id: int, satellite: Satellite):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Satellites
        SET name = %s, lifetime = %s, orbit_radius = %s
        WHERE id = %s;
    """, (satellite.name, satellite.lifetime, satellite.orbit_radius, satellite_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Satellite updated successfully"}

@app.delete("/satellites/{satellite_id}")
def delete_satellite(satellite_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Satellites WHERE id = %s;", (satellite_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Satellite deleted successfully"}


@app.get("/tv_channels/")
def get_tv_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TvChannels;")
    tv_channels = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"tv_channels": tv_channels}

@app.get("/tv_channels/{tv_channel_id}")
def get_tv_channel(tv_channel_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TvChannels WHERE id = %s;", (tv_channel_id,))
    tv_channel = cursor.fetchone()
    cursor.close()
    conn.close()
    if tv_channel is None:
        raise HTTPException(status_code=404, detail="TV Channel not found")
    return {"tv_channel": tv_channel}

@app.post("/tv_channels/")
def create_tv_channel(tv_channel: TvChannel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TvChannels (name, language, specifics, company)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (tv_channel.name, tv_channel.language, tv_channel.specifics, tv_channel.company))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": new_id, "tv_channel": tv_channel}

@app.put("/tv_channels/{tv_channel_id}")
def update_tv_channel(tv_channel_id: int, tv_channel: TvChannel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TvChannels
        SET name = %s, language = %s, specifics = %s, company = %s
        WHERE id = %s;
    """, (tv_channel.name, tv_channel.language, tv_channel.specifics, tv_channel.company, tv_channel_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "TV Channel updated successfully"}

@app.delete("/tv_channels/{tv_channel_id}")
def delete_tv_channel(tv_channel_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TvChannels WHERE id = %s;", (tv_channel_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "TV Channel deleted successfully"}


@app.get("/broadcasts/")
def get_broadcasts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Broadcasts;")
    broadcasts = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"broadcasts": broadcasts}

@app.get("/broadcasts/{broadcast_id}")
def get_broadcast(broadcast_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Broadcasts WHERE id = %s;", (broadcast_id,))
    broadcast = cursor.fetchone()
    cursor.close()
    conn.close()
    if broadcast is None:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    return {"broadcast": broadcast}

@app.post("/broadcasts/")
def create_broadcast(broadcast: Broadcast):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Broadcasts (coverage_from, coverage_to, satellite_id, tv_channel_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (broadcast.coverage_from, broadcast.coverage_to, broadcast.satellite_id, broadcast.tv_channel_id))
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": new_id, "broadcast": broadcast}

@app.put("/broadcasts/{broadcast_id}")
def update_broadcast(broadcast_id: int, broadcast: Broadcast):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Broadcasts
        SET coverage_from = %s, coverage_to = %s, satellite_id = %s, tv_channel_id = %s
        WHERE id = %s;
    """, (broadcast.coverage_from, broadcast.coverage_to, broadcast.satellite_id, broadcast.tv_channel_id, broadcast_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Broadcast updated successfully"}

@app.delete("/broadcasts/{broadcast_id}")
def delete_broadcast(broadcast_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Broadcasts WHERE id = %s;", (broadcast_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Broadcast deleted successfully"}

