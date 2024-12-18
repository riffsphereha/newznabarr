# Newznabarr - Usenet Plugin Framework for *Arr Apps

After using the *arr apps for years, I realized that while Usenet and torrents are great, they aren't always the best or only sources for content. Unfortunately, the *arr apps currently only support these two options. That’s why I created **Newznabarr** — a Usenet plugin framework for the *arr ecosystem designed to fill that gap.

## What is Newznabarr?

**Newznabarr** presents itself as a Newznab indexer and SABnzbd client, making it compatible with the *arr apps you’re already using. However, the magic lies under the hood: all searches are handled by plugins, allowing for maximum flexibility and expandability. This means you can use Newznabarr to tap into other content sources beyond traditional Usenet and torrents.

### Current Features:
- Plugin-based search and download functionality for easy expandability.
- A plugin to integrate **Readarr** with a popular book site.
- A plugin to integrate **Lidarr** with **YouTube Music** (128kbps mp3) 🎶
- Designed to fit seamlessly into your existing *arr workflow.

### Roadmap:
- RSS feed integration for the book site in **Readarr**
- **Music Streaming Sites Integration** 🎧
- **Video Streaming Sites Integration** 📺

### Contribute and Extend:
- **Make Your Own Plugins**: One of the core ideas behind Newznabarr is expandability. You can create and add your own plugins to enhance functionality or integrate with other content sources. If you have an idea for a plugin, feel free to fork the repo and start building!
- **Name Suggestion**: If you think there’s a better name for this project, feel free to suggest one! We’re open to ideas. **Expandarr** is a good option for now! (thanks u/waterloonies)
- **Icon Design**: If you're a designer or just have a creative idea, help us out with a unique icon for Newznabarr!
- I'm a bad programmer. I got this working, but if you think you can make it better in any way, please do!

### How to Get Started:
- **Docker Hub**: `riffsphereha/newznabarr`
- **GitHub**: `riffsphereha/newznabarr`

⚠️ **Note**: Newznabarr is in a very early alpha stage, so expect some bugs and rough edges. Feedback, suggestions, and contributions are welcome!

Let me know what you think, and if you have any ideas for additional plugins, a new name, or an icon, I’d love to hear them! 🌟

---

## Installation

### Install using Docker

- **Default Port**: `10000`. You can change this using the `FLASK_RUN_PORT` environment variable.
- **Configuration Directory**: Mount `/config` to your appdata folder. This will contain:
  - `config.json` files
  - SAB queue
  - Plugins
- **User and Group IDs**:
  - Use `PUID` and `PGID` to set the user and group IDs for permissions.
  - For Unraid, set `PUID` to `99` and `PGID` to `100`.
- **Download Folder**:
  - Add a download folder that matches your setup and update the `config.json` file to reflect this folder.
  - **Note**: The default path is still using the old name `/data/downloads/downloadarr` (this will be updated in future versions).

---

## How to Use

### 1. Add a SABnzbd Client to Your *Arr App

- Configure as you normally would with the following settings:
  - **Name**
  - **Enable**
  - **Host**
  - **Port**
  - **API Key**

- **Notes**:
  - Currently, plugins are available only for **Readarr** and **Lidarr**, so other *Arr apps are untested.
  - The API key can be set in the `config.json` file.
  - Enable advanced settings and set the **Client Priority** to `50`. Since this doesn't support real NZBs, it should only be used for supported plugins.
  - **Important**: Lower the SABnzbd client priority (set to a lower value than other clients) to ensure it doesn't interfere with real NZB downloads.

### 2. Add a Newznab Indexer

- Configure as you normally would with the following settings:
  - **Name**
  - **Enable Search** (RSS support is not yet available)
  - **URL** (use the `http://<ip>:<port>` format).

- **Notes**:
  - No API key is required.
  - Enable advanced settings and set the **Download Client** to the SABnzbd client you just added.

---

## Additional Information

- For more advanced configurations, or if you need to modify the default behavior, check the `config.json` file.
- Stay tuned for upcoming features, including more plugin support and enhancements!