import uuid
from datetime import datetime, timedelta
import re 

def parse_datetime_flexibly(s):
    s = s.replace('T', ' ').split('+')[0].split('Z')[0]  # remove 'T' and timezone
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError("Time data '{}' is not in a recognized format.".format(s))


class Job(object):
    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', unicode(uuid.uuid4()))
        self.jobtype = kwargs.get('jobtype', 'antismash')
        self.email = kwargs.get('email', '')
        self.filename = kwargs.get('filename', '')
        added = kwargs.get('added', datetime.utcnow())
        if isinstance(added, (str, unicode)):
            self.added = parse_datetime_flexibly(added)
        else:
            self.added = added
        last_changed = kwargs.get('last_changed', self.added)
        if isinstance(last_changed, (str, unicode)):
            self.last_changed = parse_datetime_flexibly(last_changed)
        else:
            self.last_changed = last_changed
        self.geneclustertypes = kwargs.get('geneclustertypes', '1')
        self.taxon = 'e' if kwargs.get('eukaryotic', False) else 'p'
        self.genefinder = kwargs.get('genefinder', 'prodigal')
        self.gtransl = kwargs.get('gtransl', 1)
        self.minglength = kwargs.get('minglength', 50)
        self.genomeconf = kwargs.get('genomeconf', 'l')
        self.all_orfs = kwargs.get('all_orfs', False)
        self.from_pos = int(kwargs.get('from', kwargs.get('from_pos', 0)))
        self.to_pos = int(kwargs.get('to', kwargs.get('to_pos', 0)))
        self.molecule = kwargs.get('molecule', 'nucl')
        self.inclusive = kwargs.get('inclusive', False)
        self.cf_cdsnr = int(kwargs.get('cf_cdsnr', 5))
        self.cf_npfams = int(kwargs.get('cf_npfams', 5))
        self.cf_threshold = float(kwargs.get('cf_threshold', 0.6))
        self.smcogs = kwargs.get('smcogs', False)
        self.clusterblast = kwargs.get('clusterblast', False)
        self.knownclusterblast = kwargs.get('knownclusterblast', False)
        self.subclusterblast = kwargs.get('subclusterblast', False)
        self.fullhmm = kwargs.get('fullhmm', False)
        self.asf = kwargs.get('asf', False)
        self.ecpred = kwargs.get('ecpred', False)
        self.modeling = kwargs.get('modeling', 'none')
        self.status = kwargs.get('status', 'pending')
        self.dispatcher = kwargs.get('dispatcher', 'unknown')
        self.download = kwargs.get('download', '')
        self.cdh_cutoff = kwargs.get('cdh_cutoff', 0.5)
        self.min_domain_number = kwargs.get('min_domain_number', 2)
        if 'min_mad' in kwargs:
            self.min_mad = kwargs['min_mad']

    def get_short_status(self):
        """Get a short status description useful for icon names"""
        return self.status.split(':')[0]

    def get_status(self):
        return self.status

    def get_dict(self):
        return self.__dict__

    def __repr__(self):
        return '<Job %r (%s)>' % (self.uid, self.status)

class Notice(object):
    def __init__(self,
                 teaser,
                 text,
                 added=None,
                 show_from=None,
                 show_until=None,
                 category=u'notice',
                 id=None
                ):
        self.id = id if id is not None else unicode(uuid.uuid4())
        self.added = added and added or datetime.utcnow()
        self.show_from = show_from and show_from or datetime.utcnow()
        self.show_until = show_until and show_until or \
                            datetime.utcnow() + timedelta(weeks=1)
        self.category = category
        self.teaser = teaser
        self.text = text

    def __repr__(self):
        return '<Notice (%s): %r>' % (self.category, self.teaser)

    @property
    def json(self):
        # first get rid of all internal attributes
        d = self.__dict__
        ret = dict((key, d[key]) for key in d.keys() if not key.startswith('_'))

        # replace datetime objects by a timestring
        for key in ret.keys():
            if hasattr(ret[key], 'strftime'):
                ret[key] = ret[key].strftime('%Y-%m-%d %H:%M:%S')

        return ret

class Stat(object):
    def __init__(self,
                 uid,
                 jobtype="antismash",
                 added=None,
                 finished=None,
                ):
        self.uid = uid
        self.added = added if added else datetime.utcnow()
        self.finished = finished if finished else datetime.utcnow()

    def __repr__(self):
        return '<Stat (%s): %s - %s>' % (self.uid, self.added, self.finished)
