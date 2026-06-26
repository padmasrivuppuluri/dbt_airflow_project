import json
import psycopg2

json_file_path = "/opt/airflow/include/raw/tmdb/genres.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

genres = data["genres"]

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    database="airflow",
    user="airflow",
    password="airflow"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tmdb.raw_genres (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

for genre in genres:
    cursor.execute(
        """
        INSERT INTO tmdb.raw_genres (
            genre_id,
            genre_name
        )
        VALUES (%s, %s)
        ON CONFLICT (genre_id) DO UPDATE SET
            genre_name = EXCLUDED.genre_name,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            genre.get("id"),
            genre.get("name")
        )
    )

conn.commit()
cursor.close()
conn.close()

print(f"Loaded {len(genres)} genres into tmdb.raw_genres")