import os
import requests
import json

tmdb_api_token = os.getenv("TMDB_API_TOKEN")
print(tmdb_api_token)

if not tmdb_api_token:
    raise ValueError("TMDB_API_TOKEN not found")

headers = {
    "Authorization": f"Bearer {tmdb_api_token}",
    "accept": "application/json"
}
url = "https://api.themoviedb.org/3/movie/popular"

all_movies = []
max_pages = 5
for page in range(1, max_pages+1):
    params = {"page": page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    movies = data.get("results", [])
    all_movies.extend(movies)

    print(f"Extracted page {page}: {len(movies)} movies")

final_data = {
    "page_start": 1,
    "page_end": max_pages,
    "total_movies": len(all_movies),
    "results": all_movies
}

output_path = "/opt/airflow/include/raw/tmdb/popular_movies.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(final_data, file, indent=4)

print(f"Saved file to {output_path}")