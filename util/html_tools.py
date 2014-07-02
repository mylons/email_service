__author__ = 'mylons'
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    """
    simple html parser implementation to join the parsed html
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    """
    removes html tags from a string
    :param html: string that may contain some html
    :return: string that doesn't contain html
    """
    h = HTMLStripper()
    h.feed(html)
    return h.get_data()
