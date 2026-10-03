select
    localDate::date as local_date,
    startDate as start_date,
    endDate as end_date,
    value as hr_bpm,
    motionContext as motion_context
from
    {{ source('health', 'heart_rate') }}
