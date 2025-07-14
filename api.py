from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2 import pool

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sensors")
async def get_sensor_data(limit: int = 100):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT timestamp, temperature, smoke, smoke_level, distance, light
                FROM sensor_readings
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,)
            )
            rows = cur.fetchall()
            return [
                {
                    "timestamp": row[0],
                    "temperature": row[1],
                    "smoke": row[2],
                    "smoke_level": row[3],
                    "distance": row[4],
                    "light": row[5]
                } for row in rows
            ]
    finally:
        db_pool.putconn(conn)
