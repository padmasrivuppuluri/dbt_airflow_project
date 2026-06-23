select 
    movie_id,
    title as movie_title,
    original_title,
    original_language as language_code,
    overview,
    popularity,
    release_date,
    vote_average as rating,
    vote_count,
    adult,
    genre_ids
from {{ source('tmdb', 'raw_popular_movies') }}