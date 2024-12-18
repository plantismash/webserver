plantiSMASH web interface
=========================

[![Build Status](http://github.drone.secondarymetabolites.org/api/badges/antismash/ps-web/status.svg)](http://github.drone.secondarymetabolites.org/antismash/ps-web)

This is the web interface powering http://plantismash.secondarymetabolites.org/

Installation
------------

```
conda create -n plantiserver 
conda activate
pip install -r requirements.txt
python run_development_server.py
```

Running the Web Interface
-------------------------

First, create a settings.cfg file:

```
############# Configuration #############
DEBUG = False
SECRET_KEY = "Better put a proper secret here"
# Path to antiSMASH output directory on disk
RESULTS_PATH = '/data/plantismash/upload'
# URL path to antiSMASH results in the webapp
RESULTS_URL = '/upload'

# Flask-Mail settings
DEFAULT_RECIPIENTS = ["alice@example.com", "bob@example.com"]

# Redis settings
REDIS_URL = 'redis://your.redis.database:port/number'
# defaults to redis://localhost:6379/0

# Flask-Downloader settings
# This should be the same as RESULTS_PATH
DEFAULT_DOWNLOAD_DIR = '/data/plantismash/upload'

# Content NCBI likes to return when reading from NCBI fails.
BAD_CONTENT = ('Error reading from remote server', 'Bad gateway', 'Cannot process ID list', 'server is temporarily unable to service your request', 'Service unavailable', 'Server Error')
#########################################
```

Then export the path to the settings file as `WEBSMASH_CONFIG` environment
variable and use a WSGI runner of your choice to run the app (I'm using uwsgi
in this example).

```
export WEBSMASH_CONFIG=/var/www/settings.cfg
uwsgi --pythonpath /var/www --http :5000 --module websmash:app --uid 33 --gid 33 --touch-reload /tmp/reload_websmash --daemonize /var/log/uwsgi.log
```

Now you can connect to the antiSMASH web app at port 5000. Now set up a reverse proxy to serve the web app from port 80.

License
-------

Just like antiSMASH, the web interface is available under the GNU AGPL version 3.
See the `LICENSE.txt` file for details.
