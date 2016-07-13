#!/usr/bin/env/python

import errno
import os
import sys
import signal
import optparse

from threading import Timer

from ustream import ustreamDownloader
from livestream import livestreamDownloader
from youtube import youtubeDownloader

def sigint_handler(signum, frame):
    downloader.kill()

def sigalrm_handler(signum, frame):
    signal.alarm(0)
    downloader.kill()

def CreateDownloader(url, out_file):
    if url.startswith("http://www.ustream.tv"):
	return ustreamDownloader(url, out_file)
    elif url.startswith("http://livestream.com"):
	return livestreamDownloader(url, out_file)
    elif url.startswith("http://youtube.com"):
	return youtubeDownloader(url, out_file)
    else:
	return None

class DurationTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        exit("Usage: {0} [-s duration] url output_file".format(sys.argv[0]))

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGALRM, sigalrm_handler)

    # parses options
    parser = optparse.OptionParser(
            usage = 'Usage: %prog [options] url output_file',
            version = '2016.07.12',
            conflict_handler = 'resolve'
            )

    parser.add_option('-s', '--stop', action='store', dest='duration', help='time (in seconds) to run to dump streaming, defaults to 300.')
    (opts, args) = parser.parse_args()
    (init_url, out_file) = args

    downloader = CreateDownloader(init_url, out_file)
    downloader.start()
    if opts.duration:
        dur_secs = int(opts.duration)
    else:
        dur_secs = 300
    signal.alarm(dur_secs)

    downloader.wait_for_finished()




