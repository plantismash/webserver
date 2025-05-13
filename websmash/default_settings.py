from os import path

############# Configuration #############
DEBUG = True
SECRET_KEY = "development_key"
RESULTS_PATH = path.join(path.dirname(path.dirname(__file__)), "results")
RESULTS_URL = "/upload"

# Flask-Mail settings
MAIL_SERVER = "mail.example.org"
DEFAULT_MAIL_SENDER = "alice@example.org"
DEFAULT_RECIPIENTS = ["bob@example.org"]

# Flask-Redis settings
REDIS_URL = "redis://localhost:6379/0"

# Version 
VERSION = "0.1.0"

# if you for whatever reason are running the webserver locally,
# these two settings are probably not necessary

# precalculated results location. for sure change this
PRECALCULATED_RESULTS = "/precalc"

# files where the static clusterblast listing will point to
CLUSTERBLAST_FILES = "/clusterblast"

OLD_JOB_COUNT = 0
#########################################
