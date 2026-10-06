with daily_sedentary_avg_hr as (
  select avg(hr_bpm) as daily_avg_hr, count(hr_bpm) as count, local_date
  from ref('stg_heart_rate')
  where motion_context = 1
  group by all
)