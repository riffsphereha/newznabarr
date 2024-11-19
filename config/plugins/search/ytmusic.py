from ytmusicapi import YTMusic

from plugin_search_interface import PluginSearchBase

class YTMusicSearch(PluginSearchBase):
    def getcat(self):
        return ["3010"]

    def gettestquery(self):
        return "joe sample - sample this"

    def getprefix(self):
        return "ytmusic"

    def search(self, query, cat):
        result = []
        ytmusic = YTMusic()
        try:
            # Search for the album
            search_results = ytmusic.search(query, filter='albums')
            for item in search_results:
                artists = ""
                for artist in item['artists']:
                    artists = artists + artist['name'] + " "
                albumtitle = item['title']
                year = item['year']
                link = item['browseId']
                title = artists + "- " + albumtitle + " (" + year +") (mp3) (128kbps)"
                GoodResult = True
                for word in query.split(" "):
                    if not (word.lower() in title.lower()):
                        GoodResult = False
                if GoodResult:
                    result.append({
                        "link": link,
                        "title": title,
                        "description": title,
                        "guid": link,
                        "comments": link,
                        "files": "1",
                        "size": "10000",
                        "category": cat,
                        "grabs": "100",
                        "prefix": self.getprefix()
                    })

        except Exception as e:
            print(f"An error occurred: {e}")
            result = []
        if len(result) == 0:
            result.append({
                "link": "",
                "title": "",
                "description": "",
                "guid": "",
                "comments": "",
                "files": "0",
                "size": "0",
                "category": cat,
                "grabs": "100"
            })
        return result