select
    movie_id,
    movie_title,
    original_title,
    language_code,
    overview,
    popularity,
    release_date,
    extract(year from release_date) as release_year,
    rating,
    vote_count,
    adult,
    genre_ids,
    {{ get_rating_category('rating') }} as rating_category,
    {{ get_popularity_category('popularity') }} as popularity_category
from {{ ref('stg_popular_movies') }}