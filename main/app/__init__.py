from flask import Flask
import redis
from rq import Queue
import rq_dashboard

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix = '/rq')

r = redis.Redis()
q = Queue(connection=r)

from app import views, tasks