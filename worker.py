import os
from time import sleep

from cf_cname_flattener import compareDNS

# How much seconds to wait before running script again
INTERVAL = float(os.environ.get('CF_INTERVAL', 60))

print 'Running CloudFlare CNAME flattener every %s seconds' % INTERVAL
while 1:
    compareDNS()
    sleep(INTERVAL)
