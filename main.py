from decouple import config
from flask import Flask
from flask_restful import Api
from flask_apscheduler import APScheduler
import requests

from tasks import job2

lat = 43.5726
lon = 27.8273
API_key = config('API_KEY')


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

api = Api(app)
scheduler = APScheduler()


@scheduler.task("interval", id="do_job_1", seconds=60, misfire_grace_time=900)
def job1():
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_key}"
    )
    resp_json = r.json()
    print(resp_json)
    print(f'{resp_json["main"]["temp"]} C')

scheduler.add_job(func=job2, trigger="interval", seconds=10, id="do_job_2",)

scheduler.init_app(app)
scheduler.start()


if __name__ == "__main__":
    app.run()
