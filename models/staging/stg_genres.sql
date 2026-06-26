select 
    genre_id,
    genre_name
from {{ source('tmdb', 'raw_genres') }}