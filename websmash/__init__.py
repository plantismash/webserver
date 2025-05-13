from flask import Flask, g
from flask.ext.mail import Mail
from werkzeug import SharedDataMiddleware
from os import path
from urlparse import urlparse
from redis import Redis
from redis.sentinel import Sentinel

app = Flask(__name__)
import websmash.default_settings
app.config.from_object(websmash.default_settings)
app.config.from_envvar('WEBSMASH_CONFIG', silent=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                    {app.config['RESULTS_URL']: app.config['RESULTS_PATH'],
                                     '/robots.txt': path.join(path.join(app.root_path, 'static'), 'robots.txt'),
                                     '/favicon.ico': path.join(app.root_path, 'static', 'images', 'favicon.ico')})
mail = Mail(app)

@app.context_processor
def inject_version():
    return dict(version=app.config.get('VERSION', 'dev'))

print("VERSION from config:", app.config.get('VERSION'))

def get_db():
    redis_store = getattr(g, '_database', None)
    if redis_store is None:
        if 'FAKE_DB' in app.config and app.config['FAKE_DB']:
            from mockredis import mock_redis_client
            redis_store = g._database = mock_redis_client()
        else:
            if app.config['REDIS_URL'].startswith('redis://'):
                redis_store = g._database = Redis.from_url(app.config['REDIS_URL'])
            elif app.config['REDIS_URL'].startswith('sentinel://'):
                parsed_url = urlparse(app.config['REDIS_URL'])
                service = parsed_url.path.lstrip('/')
                port = 26379
                if ':' in parsed_url.netloc:
                    host, str_port = parsed_url.netloc.split(':')
                    port = int(str_port)
                else:
                    host = parsed_url.netloc
                sentinel = Sentinel([(host, port)], socket_timeout=0.1)
                redis_store = sentinel.master_for(service, redis_class=Redis, socket_timeout=0.1)
    return redis_store

import websmash.models
import websmash.views
