select
    m.movie_id,
    cast(trim(genre_id) as integer) as genre_id
from {{ ref('dim_movie') }} m
cross join regexp_split_to_table(m.genre_ids, ',') as genre_id
where m.genre_ids is not null