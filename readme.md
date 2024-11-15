Welcome to newznabarr, a newznab and sabnzbd proxy for the starr apps.

Like many, I'm a big fan of the starr apps (radarr, sonarr, lidarr, readarr, whisparr), since they do a great job managing my media.

However, over time, I feel like just having support for usenet and torrents isn't good enough anymore. There are more and more sources
that provide better support for specific media.

This is where newznabarr comes in! It's a tool that presents itself as a newznab indexer and sabnzbd download client to the starr apps,
while in the background it makes use of plugins for the actual searching and downloading.

At this point it is in early alpha, with just 1 plugin: bring support for a popular ebook site to readarr.

In the config file you can set:
    The download path
    The api key for the "sabnzbd" client
    The supported sabnzbd categories

Just configure this in readarr like a normal sabnzbd client and newznab index, but set the indexer to use this specific sabnzdb client.

For now rss is not supported, but it's on the to-do list!