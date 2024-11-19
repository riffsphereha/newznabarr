import email.utils
import time
import xml.etree.ElementTree as ET

def searchresults_to_response(server, results):
    root = ET.Element("rss", version="2.0", attrib={
        "xmlns:atom": "http://www.w3.org/2005/Atom", 
        "xmlns:newznab": "http://www.newznab.com/DTD/2010/feeds/attributes/"
    })
    channel = ET.SubElement(root, "channel")
    
    ET.SubElement(channel, "title").text = "NewzNabArr"
    ET.SubElement(channel, "description").text = "Multiple newznab proxies for starr apps"
    ET.SubElement(channel, "link").text = server

    pub_date = email.utils.formatdate(time.time())
    ET.SubElement(channel, "pubDate").text = pub_date

    for result in results:
        prefix = result["prefix"]
        link2 = f"{server}api?download=nzb&prefix={prefix}&url={result['link']}&size={result['size']}&title={result['title']}"
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = result["title"]
        ET.SubElement(item, "description").text = result["description"]
        ET.SubElement(item, "guid").text = result["guid"]
        ET.SubElement(item, "comments").text = result["comments"]
        item_pub_date = email.utils.formatdate(time.time())
        ET.SubElement(item, "pubDate").text = item_pub_date
        ET.SubElement(item, "size").text = result["size"]
        ET.SubElement(item, "link").text = link2
        ET.SubElement(item, "category").text = result["category"]
        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", link2)
        enclosure.set("length", result["size"])  # Replace with actual file size if available
        enclosure.set("type", "application/x-nzb")  # or "application/epub" based on book format
    
        newznab_attrs = ET.SubElement(item, "newznab:attr")
        newznab_attrs.set("name", "category")
        newznab_attrs.set("value", result["category"])
        newznab_attrs = ET.SubElement(item, "newznab:attr")
        newznab_attrs.set("name", "files")
        newznab_attrs.set("value", "1")
        newznab_attrs = ET.SubElement(item, "newznab:attr")
        newznab_attrs.set("name", "grabs")
        newznab_attrs.set("value", "100")
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    return xml_str
