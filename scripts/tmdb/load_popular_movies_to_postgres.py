import json
import psycopg2
from datetime import date

json_file_path = "/opt/airflow/include/raw/tmdb/popular_movies.json"

with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

movies = data["results"]

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    database="airflow",
    user="airflow",
    password="airflow"
)

cursor = conn.cursor()

for movie in movies:
    cursor.execute(
        """
        INSERT INTO tmdb.raw_popular_movies (
            movie_id,
            title,
            original_title,
            original_language,
            overview,
            popularity,
            release_date,
            vote_average,
            vote_count,
            adult,
            video,
            softcore,
            backdrop_path,
            poster_path,
            genre_ids,
            last_ingestion_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        ON CONFLICT (movie_id) DO UPDATE SET
            title = EXCLUDED.title,
            original_title = EXCLUDED.original_title,
            original_language = EXCLUDED.original_language,
            overview = EXCLUDED.overview,
            popularity = EXCLUDED.popularity,
            release_date = EXCLUDED.release_date,
            vote_average = EXCLUDED.vote_average,
            vote_count = EXCLUDED.vote_count,
            adult = EXCLUDED.adult,
            video = EXCLUDED.video,
            softcore = EXCLUDED.softcore,
            backdrop_path = EXCLUDED.backdrop_path,
            poster_path = EXCLUDED.poster_path,
            genre_ids = EXCLUDED.genre_ids,
            updated_at = CURRENT_TIMESTAMP,
            last_ingestion_date = CURRENT_DATE
        """,
        (
            movie.get("id"),
            movie.get("title"),
            movie.get("original_title"),
            movie.get("original_language"),
            movie.get("overview"),
            movie.get("popularity"),
            movie.get("release_date") or None,
            movie.get("vote_average"),
            movie.get("vote_count"),
            movie.get("adult"),
            movie.get("video"),
            movie.get("softcore"),
            movie.get("backdrop_path"),
            movie.get("poster_path"),
            ",".join(map(str, movie.get("genre_ids", []))),
            date.today()
        )
    )

conn.commit()
cursor.close()
conn.close()

print(f"Loaded {len(movies)} movies into tmdb.raw_popular_movies")