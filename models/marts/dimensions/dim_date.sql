select distinct
    to_char(release_date, 'YYYYMMDD')::integer as date_key,
    release_date,
    extract(year from release_date) as year,
    extract(month from release_date) as month,
    extract(day from release_date) as day,
    trim(to_char(release_date, 'Month')) as month_name,
    extract(quarter from release_date) as quarter
from {{ ref('dim_movie') }}
where release_date is not null