select
    movie_id,
    movie_title,
    original_title,
    language_code,
    release_date,
    release_year,
    adult,
    genre_ids
from {{ ref('int_movies_clean') }}