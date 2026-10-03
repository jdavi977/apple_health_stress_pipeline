
select
    localDate::date as local_date,
    startDate as start_date,
    value as hrv_ms
from {{ source('health', 'hrv') }}