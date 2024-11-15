from abc import ABC, abstractmethod

class PluginSearchBase(ABC):
    @abstractmethod
    def getcat(self):
        """Return all cats supported by plugin."""
        pass

    @abstractmethod
    def gettestquery(self):
        """Return a test query supported by the plugin to do a test search"""
        pass

    @abstractmethod
    def getprefix(self):
        """The prefix for the search link, to identify a compatible downloader"""
        pass

    @abstractmethod
    def search(self, query):
        """Perform a search"""
        # Must include:
        # link: some info on where to download from
        # title: used by starr apps to compare the result
        # description: can be anything
        # guid: unique identifier, not really used but there in case
        # comments: anything
        # size: file size
        # files: number of files
        # category: the exact category
        # grabs: how many downloads there are
        pass