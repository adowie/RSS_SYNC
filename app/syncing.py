from feedparser import parse

class RSSFeedProcessor:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.entries = []
        self.feed = None
    def fetch_feed(self):
        try:
            feed = parse(self.feed_url)
            print(f"Fetching feed from URI {self.feed_url}")
            self.entries = feed.entries
            self.feed = feed
        except FeedParserDictKeyError as e:
            print(f"KeyError: {e}")
        except FeedParserHTTPError as e:
            print(f"HTTPError: {e}")
        except ParseError as e:
            print(f"ParseError: {e}")
        except Exception as e:
            raise Exception("Error fetching RSS feed")
        

