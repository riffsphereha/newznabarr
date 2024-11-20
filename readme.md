After using the *arr apps for years, I realized that while Usenet and torrents are great, they aren't always the best or only sources for content. Unfortunately, the *arr apps currently only support these two options. That’s why I created Newznabarr — a Usenet plugin framework for the *arr ecosystem designed to fill that gap.

What is Newznabarr?

Newznabarr presents itself as a Newznab indexer and SABnzbd client, making it compatible with the *arr apps you’re already using. However, the magic lies under the hood: all searches are handled by plugins, allowing for maximum flexibility and expandability. This means you can use Newznabarr to tap into other content sources beyond traditional Usenet and torrents.

Current Features:

Plugin-based search functionality for easy expandability.

A Readarr plugin to integrate with a popular book site, providing better book search options than traditional methods.

YouTube Music for Lidarr (coming soon!) 🎶

Designed to fit seamlessly into your existing *arr workflow.

Roadmap:

RSS feed integration for the book site in Readarr (on the way!)

Music Streaming Sites Integration 🎧

Video Streaming Sites Integration 📺

Contribute and Extend:

Make Your Own Plugins: One of the core ideas behind Newznabarr is expandability. You can create and add your own plugins to enhance functionality or integrate with other content sources. If you have an idea for a plugin, feel free to fork the repo and start building!

Name Suggestion: If you think there’s a better name for this project, feel free to suggest one! We’re open to ideas.

Icon Design: If you're a designer or just have a creative idea, help us out with a unique icon for Newznabarr!

How to Get Started:

Docker Hub: riffsphereha/newznabarr

GitHub: riffsphereha/newznabarr

⚠️ Note: Newznabarr is in a very early alpha stage, so expect some bugs and rough edges. Feedback, suggestions, and contributions are welcome!

Let me know what you think, and if you have any ideas for additional plugins, a new name, or an icon, I’d love to hear them! 🌟

Install:
    Install using docker.
    Default port is 10000. Use FLASK_RUN_PORT environmental variable to change container port.
    /config points to your appdata. Here will be the config.json files, the sab queue, and the plugins.
    Use PUID and PGID to set user and group. For unraid, set them to 99 and 100
    Make sure to add a downloadfolder, and make it match your folder setup. Edit the config.json to reflect this folder.
        Since this is early alpha and I'm lazy, the default still uses the old name: "/data/downloads/downloadarr".
