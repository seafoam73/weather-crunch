from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from load import weather_load
import pytz


central = pytz.timezone('America/Chicago')

scheduler = BlockingScheduler()
scheduler.add_job(weather_load, trigger=CronTrigger(hour=8,timezone=central))
scheduler.add_job(weather_load, trigger=CronTrigger(hour=14,timezone=central))
scheduler.add_job(weather_load, trigger=CronTrigger(hour=20,timezone=central))
scheduler.add_job(weather_load, trigger=CronTrigger(hour=2,timezone=central))
scheduler.start()