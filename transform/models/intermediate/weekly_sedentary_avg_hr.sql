with weekly_sedentary_avg_hr as (
  select avg(daily_avg_hr) as weekly_avg_hr,
  sum(count) as n_readings,
  count(*) as n_days_read,
  date_trunc('week', local_date) as week
  from {{ ref('daily_sedentary_avg_hr') }}
  group by all
)