plantiSMASH web interface
=========================

This is the web interface powering https://plantismash.bioinformatics.nl

Installation
------------

1. Clone the repository and move in the directory of the repository

``` 
cd webserver 
```

2. Create a virtual environment and install requirements

```
conda create -n plantiserver 
conda activate plantiserver 
pip install -r requirements.txt
```

3. Run the webserver

```
python run_development_server.py
```

Running the Web Interface
-------------------------

Create a settings.cfg file:

```
############# Configuration #############
DEBUG = False
SECRET_KEY = "Better put a proper secret here"
# Path to plantiSMASH output directory on disk
RESULTS_PATH = '/data/plantismash/upload'
# URL path to plantiSMASH results in the webapp
RESULTS_URL = '/upload'

# Flask-Mail settings
DEFAULT_RECIPIENTS = ["alice@example.com", "bob@example.com"]

# Redis settings
REDIS_URL = 'redis://your.redis.database:port/number'
# defaults to redis://localhost:6379/0

# Version of antiSMASH to use
VERSION = '2.0-beta'

# Flask-Downloader settings
# This should be the same as RESULTS_PATH
DEFAULT_DOWNLOAD_DIR = '/data/plantismash/upload'

# if you for whatever reason are running the webserver locally,
# these two settings are probably not necessary

# precalculated results location. for sure change this
PRECALCULATED_RESULTS = "/precalc"

# files where the static clusterblast listing will point to
CLUSTERBLAST_FILES = "/clusterblast"

# Content NCBI likes to return when reading from NCBI fails.
BAD_CONTENT = ('Error reading from remote server', 'Bad gateway', 'Cannot process ID list', 'server is temporarily unable to service your request', 'Service unavailable', 'Server Error')

#########################################
```

This file is not tracked by Git (see [.gitignore](./.gitignore)). 

Then export the path to the settings file as `WEBSMASH_CONFIG` environment
variable and use a WSGI runner of your choice to run the app (I'm using uwsgi
in this example).

```
export WEBSMASH_CONFIG=/var/www/settings.cfg
uwsgi --pythonpath /var/www --http :5000 --module websmash:app --uid 33 --gid 33 --touch-reload /tmp/reload_websmash --daemonize /var/log/uwsgi.log
```

Now you can connect to the plantiSMASH web app at port 5000. Now set up a reverse proxy to serve the web app from port 80.

License
-------

Just like antiSMASH, the web interface is available under the GNU AGPL version 3.
See [LICENSE.txt](./LICENSE.txt) for details.
