from tweets.src.build_locality_dataset import BuildLocalityDataset
from tweets.src.crawler_twitter import CrawlerTwitter
from tweets.src.stream_twitter import StreamTwitterGenerator
from tweets.src.transform_twitter import TransformTweets
import threading

class TweetsGrabber(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    return

  def run(self):
    CrawlerTwitter()
    BuildLocalityDataset()
    TransformTweets()
    StreamTwitterGenerator()