from flask import redirect, send_file, url_for, request, abort, \
                  render_template, jsonify
from flask.ext.mail import Message
import os
from os import path
from werkzeug import secure_filename
from websmash import app, mail, get_db
from websmash.utils import generate_confirmation_mail
from websmash.models import Job, Notice
import telnetlib


def _submit_job(redis_store, job):
    """Submit a new job"""
    redis_store.hmset(u'job:%s' % job.uid, job.get_dict())

    queue = "jobs:queued"

    redis_store.lpush(queue, job.uid)

@app.route('/', methods=['GET', 'POST'])
def new():
    redis_store = get_db()
    error = None
    results_path = app.config['RESULTS_URL']
    old_email = ''
    try:
        if request.method == 'POST':
            kwargs = {}
            kwargs['ncbi'] = request.form.get('ncbi', '').strip()
            kwargs['email'] = request.form.get('email', '').strip()
            old_email = kwargs['email']

            # This webapi is for plantiSMASH, so create plantiSMASH jobs
            kwargs['jobtype'] = 'plantismash'

            clusterblast = request.form.get('clusterblast', u'off')
            knownclusterblast = request.form.get('knownclusterblast', u'off')
            subclusterblast = request.form.get('subclusterblast', u'off')
            fullhmmer = request.form.get('fullhmmer', u'off')
            coexpress_mad = request.form.get('coexpress_mad', u'')

            kwargs['cdh_cutoff'] = request.form.get('cdh_cutoff', 0.5, type=float)
            kwargs['min_domain_number'] = request.form.get('min_domain_number', 2, type=int)

            # Use boolean values instead of "on/off" strings
            kwargs['clusterblast'] = (clusterblast == u'on')
            kwargs['knownclusterblast'] = (knownclusterblast == u'on')

            try:
                kwargs['min_mad'] = int(coexpress_mad)
            except ValueError:
                pass

            job = Job(**kwargs)
            dirname = path.join(app.config['RESULTS_PATH'], job.uid)
            os.mkdir(dirname)
            upload = None

            if kwargs['ncbi'] != '':
                job.download = kwargs['ncbi']
            else:
                upload = request.files['seq']

                if upload is not None:
                    filename = secure_filename(upload.filename)
                    upload.save(path.join(dirname, filename))
                    if not path.exists(path.join(dirname, filename)):
                        raise Exception("Could not save file!")
                    job.filename = filename
                else:
                    raise Exception("Uploading input file failed!")


            if 'gff' in request.files:
                gff = request.files['gff']
                if gff is not None and gff.filename != '':
                    filename = secure_filename(gff.filename)
                    gff.save(path.join(dirname, filename))
                    if not path.exists(path.join(dirname, filename)):
                        raise Exception("Could not save file!")
                    job.gff3 = filename

            if 'coexpress_file' in request.files:
                coexpress_file = request.files['coexpress_file']
                if coexpress_file is not None and coexpress_file.filename != '':
                    filename = secure_filename(coexpress_file.filename)
                    coexpress_file.save(path.join(dirname, filename))
                    if not path.exists(path.join(dirname, filename)):
                        raise Exception("Could not save file!")

                    job.coexpress = True

                    _, ext = path.splitext(filename)
                    if ext.lower() == '.soft':
                        job.soft_file = filename
                    elif ext.lower() == '.csv':
                        job.csv_file = filename
                    else:
                        job.coexpress = False


            _submit_job(redis_store, job)
            return redirect(url_for('.display', task_id=job.uid))
    except Exception, e:
        error = unicode(e)
    return render_template('new.html', error=error,
                           old_email=old_email,
                           results_path=results_path)


@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/help')
@app.route('/help.html')
def help():
    return render_template('help.html')

@app.route('/download')
@app.route('/download.html')
def download():
    return render_template('download.html')



def handle_send_smtp(mail_from, mail_to, message, host="smtp.example.org", port=25):
    import smtplib
    s = smtplib.SMTP(host, port)
    s.ehlo_or_helo_if_needed()
    s.sendmail(mail_from, mail_to, message)


@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    error = None
    email = ''
    message = ''
    try:
        if request.method == 'POST':
            email = request.form.get('email', '')
            message = request.form.get('body', '')
            if email == '':
                raise Exception("Please specify an email address")
            if message == '':
                raise Exception("No message specified. Please specify a message")

            # contact_msg = Message(subject='plantiSMASH feedback',
            #                       recipients=app.config['DEFAULT_RECIPIENTS'],
            #                       body=message, sender=email)
            # mail.send(contact_msg)
            # confirmation_msg = Message(subject='plantiSMASH feedback received',
            #                            recipients=[email],
            #                            body=generate_confirmation_mail(message))
            # mail.send(confirmation_msg)

            # send feedback email
            feedback_message = "Subject: %s\n" % "plantiSMASH feedback"
            feedback_message += "From: %s\n" % email
            feedback_message += "To: %s\n" % app.config['DEFAULT_MAIL_SENDER']
            feedback_message += "\n"
            feedback_message += message

            print("sending feedback message")
            print("from: " + email)
            print("to: " + app.config['DEFAULT_MAIL_SENDER'])
            print(feedback_message)

            handle_send_smtp(email, app.config['DEFAULT_MAIL_SENDER'], feedback_message, host=app.config["MAIL_SERVER"])

            # Send confirmation email
            confirmation_message = "Subject: %s\n" % "plantiSMASH feedback received"
            confirmation_message += "From: %s\n" % app.config['DEFAULT_MAIL_SENDER']
            confirmation_message += "To: %s\n" % email
            confirmation_message += "\n"
            confirmation_message += generate_confirmation_mail(message)

            print("sending confirmation message")
            print("from: " + app.config['DEFAULT_MAIL_SENDER'])
            print("to: " + email)
            print(confirmation_message)

            handle_send_smtp(app.config['DEFAULT_MAIL_SENDER'], email, confirmation_message, host=app.config["MAIL_SERVER"])


            return render_template('message_sent.html', message=message)
    except Exception, e:
        error = unicode(e)
    return render_template('contact_form.html', error=error, email=email, message=message)

@app.route('/display/<task_id>')
def display(task_id):
    redis_store = get_db()
    results_path = app.config['RESULTS_URL']
    res = redis_store.hgetall(u'job:%s' % task_id)
    if res == {}:
        abort(404)
    else:
        job = Job(**res)
    return render_template('display.html', job=job, results_path=results_path)

@app.route('/display')
def display_tab():
    return render_template('new.html',
                           sec_met_types=sec_met_types,
                           switch_to='job',
                           results_path=app.config['RESULTS_URL'])

@app.route('/status/<task_id>')
def status(task_id):
    redis_store = get_db()
    res = redis_store.hgetall(u'job:%s' % task_id)
    if res == {}:
        abort(404)

    # Decode byte strings to Unicode for python 3 compatibility
    res = {k.decode('utf-8') if isinstance(k, bytes) else k:
           v.decode('utf-8') if isinstance(v, bytes) else v
           for k, v in res.items()}
    
    job = Job(**res)
    print("Status check: job %s has status '%s'" % (job.uid, job.status))

    if job.status == 'done':
        print("Job %s is completed" % job.uid)
        # check if the job is done and if so, move it to the completed queue
        result_url = "%s/%s" % (app.config['RESULTS_URL'], job.uid)
        redis_store.hset('job:%s' % job.uid, 'result_url', result_url)

        if job.jobtype == 'antismash':
            result_url += "/display.xhtml"
        else:
            result_url += "/index.html"
        res['result_url'] = result_url

    else:
        print("Job %s is not completed yet (status: %s)" % (job.uid, job.status))

    res['short_status'] = job.get_short_status()

    return jsonify(res)


@app.route('/server_status')
def server_status():
    redis_store = get_db()
    pending = redis_store.llen('jobs:queued')
    long_running = redis_store.llen("jobs:timeconsuming")
    running = redis_store.llen('jobs:running')

    # carry over jobs count from the old database from the config
    total_jobs = app.config['OLD_JOB_COUNT'] + redis_store.llen('jobs:completed') + \
                 redis_store.llen('jobs:failed')

    if pending + long_running + running > 0:
        status = 'working'
    else:
        status = 'idle'

    ts_queued, ts_queued_m = _get_job_timestamps(_get_oldest_job("jobs:queued"))
    ts_timeconsuming, ts_timeconsuming_m = _get_job_timestamps(_get_oldest_job("jobs:timeconsuming"))

    return jsonify(status=status, queue_length=pending, running=running,
                   long_running=long_running, total_jobs=total_jobs,
                   ts_queued=ts_queued, ts_queued_m=ts_queued_m,
                   ts_timeconsuming=ts_timeconsuming, ts_timeconsuming_m=ts_timeconsuming_m)

@app.route('/precalc', defaults={'req_path': ''})
@app.route('/precalc/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = app.config['PRECALCULATED_RESULTS']

    sys_path = os.path.join(BASE_DIR, req_path)

    abs_path = os.path.join('/precalc', req_path)
    

    # Return 404 if path doesn't exist
    if not os.path.exists(sys_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(sys_path):
        return send_file(sys_path)

    abs_path = abs_path + ('/' if abs_path[-1] != '/' else '')
    # Show directory contents
    files = os.listdir(sys_path)

    print(files)

    if "index.html" in files:
        return send_file(os.path.join(sys_path, "index.html"))

    for i, f in enumerate(files):
        f_sys_path = os.path.join(sys_path, f)
        if os.path.isdir(f_sys_path):
            files[i] = f + '/'

    # sort directories first, then files
    files.sort(key=lambda file: (not file.endswith('/'), file))


    files = [abs_path + f for f in files]


    return render_template('files.html', files=files, path=req_path)

@app.route('/clusterblast', defaults={'req_path': ''})
@app.route('/clusterblast/<path:req_path>')
def clusterblast_listing(req_path):
    BASE_DIR = app.config['CLUSTERBLAST_FILES']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
        

    # Show directory contents
    files = sorted(os.listdir(abs_path), key=lambda file: file)
    return render_template('files.html', files=files, path=req_path)




def _get_oldest_job(queue):
    """Get the oldest job in a queue"""
    redis_store = get_db()
    try:
        res = redis_store.hgetall("job:%s" % redis_store.lrange(queue, -1, -1)[0])
    except IndexError:
        return None

    return Job(**res)

def _get_job_timestamps(job):
    """Get both a readable and a machine-readble timestamp for a job"""
    if job is None:
        return None, None
    return job.added.strftime("%Y-%m-%d %H:%M"), job.added.strftime("%Y-%m-%dT%H:%M:%SZ")

@app.route('/current_notices')
def current_notices():
    "Display current notices"
    redis_store = get_db()
    rets = redis_store.keys('notice:*')
    notices = [ redis_store.hgetall(n) for n in rets]
    return jsonify(notices=notices)

@app.route('/show_notices')
def show_notices():
    "Show current notices"
    redis_store = get_db()
    rets = redis_store.keys('notice:*')
    notices = [Notice(**redis_store.hgetall(i)) for i in rets]
    return render_template('notices.html', notices=notices, skip_notices=True)
