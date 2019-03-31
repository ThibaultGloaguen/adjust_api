import os

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from application import create_app

# run : uwsgi --http 127.0.0.1:8000 --wsgi-file app.py --callable app_dispatch
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
app_dispatch = DispatcherMiddleware(app)
