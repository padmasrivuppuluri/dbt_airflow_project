{% snapshot raw_popular_movies_snapshot %}

{{
    config(
        target_schema='tmdb',
        unique_key='movie_id',
        strategy='check',
        check_cols=['vote_average', 'popularity', 'vote_count']
    )
}}

select *
from {{ source('tmdb', 'raw_popular_movies') }}

{% endsnapshot %}