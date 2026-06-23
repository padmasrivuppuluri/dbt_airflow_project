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
    case
        when rating >= 8 then 'Excellent'
        when rating >= 6 then 'Good'
        when rating >= 4 then 'Average'
        else 'Low'
    end as rating_category,
    case
        when popularity >= 500 then 'Very High'
        when popularity >= 300 then 'High'
        when popularity >= 100 then 'Medium'
        else 'Low'
    end as popularity_category
from {{ ref('stg_popular_movies') }}