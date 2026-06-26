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
url = "https://api.themoviedb.org/3/genre/movie/list"

response = requests.get(url, headers=headers)
print(response.status_code)
data = response.json()

output_path = "/opt/airflow/include/raw/tmdb/genres.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print(f"Saved file to {output_path}")

