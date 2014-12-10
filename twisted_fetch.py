from twisted.internet import defer, reactor
from twisted.web.client import getPage
import time
from sm.db import connection
col = connection['outdoor']['event']

query = {'pic':None, 'status':-10}
def get_crawled_items(offset, count):
    items = list(col.find(
        query,
        ['_id', 'orig_pic', 'orig_previews']
        ).skip(offset).limit(count)
    )
    return items

def fetch_pic(item):
    deferer = []
    orig_pic = item.get('orig_pic')
    print 'orig_pic', orig_pic
    orig_previews = item.get('orig_previews')
    if not (orig_pic or orig_previews):
        print 'no pic'
        return
    d = getPage(str(orig_pic))
    d.addCallback(process_page,str(orig_pic))
    deferer.append(d)
    for d in orig_previews:
        de = getPage(str(d))
        de.addCallback(process_page, str(d))
        deferer.append(de)
    return deferer


def process_page(page, url):
    print url, len(page)
    return url, len(page)


def printResults(result):
    for success, value in result:
        if success:
            print 'Success:', value
        else:
            print 'Failure:', value.getErrorMessage()

def printDelta(_, start):
    delta = time.time() - start
    print 'ran in %0.3fs' % (delta,)
    return delta

def fetch_all_pic(items):
    callbacks = []
    for item in items:
        d = fetch_pic(item)
        if type(d)==list:
            callbacks.extend(d)
        elif d:
            callbacks.append(d)
    callbacks = defer.DeferredList(callbacks)
    callbacks.addCallback(printResults)
    return callbacks

@defer.inlineCallbacks
def main():
    times = []
    page_count = 10
    total = col.find(query).count()
    for x in xrange(total/page_count):
        offset = x*page_count
        items = get_crawled_items(offset, page_count)
        d_list = fetch_all_pic(items)
        d_list.addCallback(printDelta, time.time())
        times.append((yield d_list))
    print 'avg time: %0.3fs' % (sum(times) / len(times),)
    print len(times)
    print sum(times)
    print total

reactor.callWhenRunning(main)
reactor.run()
