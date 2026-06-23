{{
    config(
        materialized='incremental',
        unique_key='movie_id',
        incremental_strategy='delete+insert'
    )
}}

select
    movie_id,
    rating,
    vote_count,
    popularity,
    rating_category,
    popularity_category
from {{ ref('int_movies_clean') }}