select
    localDate::date as local_date,
    creationDate as creation_date,
    value as resting_hr_bpm
from {{ source('health', 'resting_hr')}}
