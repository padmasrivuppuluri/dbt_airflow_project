select
    movie_id,
    movie_title,
    original_title,
    language_code,
    release_date,
    to_char(release_date, 'YYYYMMDD')::integer as date_key,
    release_year,
    adult,
    genre_ids
from {{ ref('int_movies_clean') }}