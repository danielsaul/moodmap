from .utils import *
from twython import TwythonStreamer
import logging

logger = logging.getLogger('moodmap.twitter')

# UK Location Boundary
#locations = [
#    -7.93, 55.40, -0.53, 60.92,
#    -5.65, 51.60, 2.33, 56.13,
#    -5.52, 50.60, 1.67, 51.84,
#    -6.64, 49.82, 1.54, 51.29, 
#    -8.28, 54.07, -5.27, 55.35
#]

callback = None

class Streamer(TwythonStreamer):
    def set_callback(self, callback):
        self.callback = callback

    def on_success(self, data):
        #logger.debug(data)
        if self.callback:
            self.callback(data)

    def on_error(self, status_code, data):
        logger.warning("Twitter Error: [{0}] {1}".format(status_code, data['text']))
    
    def on_timeout(self):
        logger.warning("Twitter Snoozing")

def start(filter_location, locations=locations, callback=callback):
    stream = Streamer(env("TWITTER_CONSUMER_KEY"), env("TWITTER_CONSUMER_SECRET"), env("TWITTER_ACCESS_TOKEN"), env("TWITTER_ACCESS_TOKEN_SECRET"))
    stream.set_callback(callback)

    logger.info("Twitter stream starting.")

    if filter_location:
        stream.statuses.filter(locations=locations)
    else:
        stream.statuses.sample(language="en")

