import os
import importlib
import sys
from flask import Flask, request, Response, jsonify
import requests
import xml.etree.ElementTree as ET
import random
import string
import hashlib
import threading
import time

from plugin_search_interface import PluginSearchBase
from plugin_download_interface import PluginDownloadBase
from newznab import searchresults_to_response
from sabnzbd import *

# directory variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.environ.get('CONFIG')
PLUGIN_SEARCH_DIR = os.path.join(CONFIG_DIR, "plugins","search")
PLUGIN_DOWNLOAD_DIR = os.path.join(CONFIG_DIR, "plugins","download")
DOWNLOAD_DIR = "/data/downloads/downloadarr"
SAB_API = "abcde"
SAB_CATEGORIES = ["lidarr"]

# array holding plugins
search_plugins = []
download_plugins = []
sabqueue = []

# falsk app
app = Flask(__name__)

# load all the search plugins
def load_search_plugins(search_plugin_directory):
    search_plugins = []
    sys.path.insert(0, search_plugin_directory)
    print("Loading search plugins from:" + search_plugin_directory)

    for filename in os.listdir(search_plugin_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, PluginSearchBase) and obj is not PluginSearchBase:
                        search_plugins.append(obj())
            except Exception as e:
                print(f"Failed to load plugin {module_name}: {e}")
    sys.path.pop(0)
    print("Loaded search plugins: " + str(len(search_plugins)))
    return search_plugins

def load_download_plugins(download_plugin_directory):
    download_plugins = []    
    sys.path.insert(0, download_plugin_directory)
    print("Loading download plugins from:" + download_plugin_directory)

    for filename in os.listdir(download_plugin_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, PluginDownloadBase) and obj is not PluginDownloadBase:
                        download_plugins.append(obj())
            except Exception as e:
                print(f"Failed to load plugin {module_name}: {e}")
    sys.path.pop(0)
    print("Loaded download plugins: " + str(len(download_plugins)))
    return download_plugins

def run_download_queue():
    print("Download queue started")
    global sabqueue
    while True:
        print("Items in queue: " + len(sabqueue))
        for dl in sabqueue:
            if dl['status'] == "Queued":
                for dlplugin in download_plugins:
                    if dl["prefix"] in dlplugin.getprefix():
                        result = dlplugin.download(dl["url"],dl["title"],DOWNLOAD_DIR,dl["cat"])
                        if result == "404":
                            sabdeletefromqueue(CONFIG_DIR,sabqueue,dl["nzo"])
                        else:
                            dl["status"] = "Complete"
                            dl["storage"] = result
                            sabsavequeue(CONFIG_DIR,sabqueue)
        time.sleep(60)

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)  # Load the JSON data from the file
        return config
    except FileNotFoundError:
        print(f"Error: The file '{config_file}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{config_file}' contains invalid JSON.")
        return None

def start():
    config = read_config(os.path.join(CONFIG_DIR, "config.json"))
    global DOWNLOAD_DIR
    global SAB_API
    global SAB_CATEGORIES
    if config:
        DOWNLOAD_DIR = config.get("download_directory", DOWNLOAD_DIR)
        SAB_API = config.get("sab_api", SAB_API)
        SAB_CATEGORIES = config.get("sab_categories", SAB_CATEGORIES)
    #load search plugins
    global search_plugins
    global download_plugins
    global sabqueue
    search_plugins = load_search_plugins(PLUGIN_SEARCH_DIR)
    download_plugins = load_download_plugins(PLUGIN_DOWNLOAD_DIR)
    sabqueue = sabloadqueue(CONFIG_DIR)

# when api with t=caps, collect all supported cats from all search plugins
# and report them correctly
def newznab_caps_response():
    root = ET.Element("caps")

    server = ET.SubElement(root, "server")
    server.set("version", "0.1")

    for p in search_plugins:
        cat=p.getcat()
        for c in cat:
            categories = ET.SubElement(root, "categories")
            category = ET.SubElement(categories, "category")
            category.set("id", c)

    return ET.tostring(root, encoding="utf-8", method="xml")

# flask routes and code

@app.route("/api", methods=["GET", "POST"])
def api():
    global sabqueue
    # return all cats supported by all our search plugins
    if request.args.get("t") == "caps":
        xml_response = newznab_caps_response()
        return Response(xml_response, mimetype="application/xml")

    # readarr uses t=book to check if the indexer works
    elif request.args.get("t") == "book" :
        request_cats=(request.args.get("cat").split(","))
        for plugin in search_plugins:
            for cat in plugin.getcat():
                if cat in request_cats:
                    query = plugin.gettestquery()
                    results = plugin.search(query)
                    xml_response = searchresults_to_response(request.host_url, plugin.getprefix, results)
                    return Response(xml_response, mimetype="application/xml")
        return "No search provider found"

    # t=search is the normal search function
    elif request.args.get("t") == "search" :
        request_cats=(request.args.get("cat").split(","))
        for plugin in search_plugins:
            for cat in plugin.getcat():
                if cat in request_cats:
                    query = request.args.get("q")
                    results = plugin.search(query)
                    xml_response = searchresults_to_response(request.host_url, plugin.getprefix(), results)
                    return Response(xml_response, mimetype="application/xml")
        return "No search provider found"


    # starr app downloads the nzb
    elif request.args.get("download") == "nzb":


        # Create the root element with the required namespace
        nzb = ET.Element('nzb', xmlns="http://www.newzbin.com/DTD/2003/nzb")

        # Add a <meta> section to store the hidden URL in plain text
        meta = ET.SubElement(nzb, 'meta')
        url_element = ET.SubElement(meta, 'prefix')
        url_element.text = request.args.get("prefix")
        url_element = ET.SubElement(meta, 'url')
        url_element.text = request.args.get("url")
        url_element = ET.SubElement(meta, 'size')
        url_element.text = request.args.get("size")
        url_element = ET.SubElement(meta, 'title')
        url_element.text = request.args.get("title")

        # Create a <file> element with required attributes
        file_elem = ET.SubElement(nzb, 'file', poster="none", subject="none")
        
        # Add a <groups> section within the <file> element
        groups = ET.SubElement(file_elem, 'groups')
        group = ET.SubElement(groups, 'group')

        # Add a <segments> section with provided segments information
        segments = ET.SubElement(file_elem, 'segments')
        segment = ET.SubElement(segments, 'segment', bytes=request.args.get("size"), number="1")

        # Convert the XML tree to a string
        return ET.tostring(nzb, encoding='utf-8', xml_declaration=True).decode()    

    # sabnzbd functions
    elif request.args.get("mode") == "version":
        return sabversion()

    elif request.args.get("mode") == 'get_config':
        if SAB_API == request.args.get("apikey"):
            sabconfig = sabgetconfig(SAB_CATEGORIES)
            sabconfig["config"]["misc"]["complete_dir"] = DOWNLOAD_DIR
            sabconfig["config"]["misc"]["api_key"] = SAB_API
            return sabconfig
        return jsonify({"error": "Access Denied"}), 403

    elif request.args.get("mode") == "addfile":
        if SAB_API == request.args.get("apikey"):
            uploaded_file=request.files["name"]
            file_text = uploaded_file.read()
            root = ET.fromstring(file_text)
            namespace = {'nzb': 'http://www.newzbin.com/DTD/2003/nzb'}
            url_element = root.find('.//nzb:meta/nzb:url', namespace)
            url = url_element.text if url_element is not None else None
            prefix_element = root.find('.//nzb:meta/nzb:prefix', namespace)
            prefix = prefix_element.text if prefix_element is not None else None
            size_element = root.find('.//nzb:meta/nzb:size', namespace)
            size = size_element.text if size_element is not None else None
            title_element = root.find('.//nzb:meta/nzb:title', namespace)
            title = title_element.text if title_element is not None else None

            nzo=hashlib.md5(url.encode()).hexdigest()
            print(nzo)
            sabqueue.append({
                "prefix": prefix,
                "size": size,
                "url": url,
                "nzo": nzo,
                "title": title,
                "status": "Queued",
                "cat": request.args.get("cat")
                })
            result=json.loads("""{"status":true,"nzo_ids":["SABnzbd_nzo_cqz8nwn8"]}""")
            result["nzo_ids"]=[f"SABnzbd_nzo_{nzo}"]
            sabsavequeue(CONFIG_DIR,sabqueue)
            return(result), 200
        return jsonify({"error": "Access Denied"}), 403

    elif request.args.get("mode") == 'queue':
        if SAB_API == request.args.get("apikey"):
            if "name" in request.args:
                if request.args.get("name") == "delete":
                    sabqueue = sabdeletefromqueue(CONFIG_DIR,sabqueue,request.args.get("value"))
                    return "ok"
            else:
                return sabgetqueue(sabqueue)
        return jsonify({"error": "Access Denied"}), 403

    elif request.args.get("mode") == 'history':
        if SAB_API == request.args.get("apikey"):
            return sabgethistory(sabqueue)
        return jsonify({"error": "Access Denied"}), 403
    
download_thread = threading.Thread(target=run_download_queue)
download_thread.daemon = True  # Ensures the thread stops when the program ends
download_thread.start()

if __name__ == "__main__":
    # load configs and plugins
    start()
    # start flask
    app.run(host="0.0.0.0", port=10000)