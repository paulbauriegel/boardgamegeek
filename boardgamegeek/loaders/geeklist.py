import datetime

from ..utils import xml_subelement_text
from ..objects.geeklist import GeekList

def parse_date(str_date):
    return datetime.datetime.strptime(str_date, '%a, %d %b %Y %H:%M:%S %z')
    # example: Sat, 02 Feb 2019 15:13:54 +0000


def create_geeklist_from_xml(xml_root, listid):
    data = {
        'id': listid,
        'name': xml_subelement_text(xml_root, 'title'),  # need a name for a thing!
        'postdate': xml_subelement_text(xml_root, 'postdate', parse_date, quiet=True),
        'editdate': xml_subelement_text(xml_root, 'editdate', parse_date, quiet=True),
        'thumbs': xml_subelement_text(xml_root, 'thumbs', int),
        'numitems': xml_subelement_text(xml_root, 'numitems', int),
        'username': xml_subelement_text(xml_root, 'username'),
        'description': xml_subelement_text(xml_root, 'description')
        # "comments": ...
    }
    return GeekList(data)

def add_geeklist_items_from_xml(geeklist, xml_root):
    added_items = False
    for item in xml_root.findall("item"):
        # initial data for this collection item
        data = {
            "id": item.attrib["id"],
            "username": item.attrib["username"],
            "postdate": parse_date(item.attrib["postdate"]) or None,
            "editdate": parse_date(item.attrib["editdate"]) or None,
            "thumbs": int(item.attrib["thumbs"]),
            "body": xml_subelement_text(item, "body")
            # "comments": ...
        }
        listitem = geeklist.add_item(data)
        object_data = {
            "id": item.attrib["objectid"],
            "name": item.attrib["objectname"],
            "imageid": item.attrib["imageid"],
            "type": item.attrib["objecttype"],
            "subtype": item.attrib["subtype"]
        }
        listitem.set_object(object_data)
        added_items = True
    return added_items
