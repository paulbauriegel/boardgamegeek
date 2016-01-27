import logging


from ..guild import Guild
from ..utils import xml_subelement_text


log = logging.getLogger("boardgamegeek.loaders.guild")


def create_guild_from_xml(xml_root, html_parser):

    if "name" not in xml_root.attrib:
        log.warn("unable to get guild information (name not found)")
        return None

    data = {"name": xml_root.attrib["name"],
            "created": xml_root.attrib.get("created"),
            "id": int(xml_root.attrib["id"]),
            "members": [],
            "category": xml_subelement_text(xml_root, "category"),
            "website": xml_subelement_text(xml_root, "website"),
            "manager": xml_subelement_text(xml_root, "manager"),
            "description": xml_subelement_text(xml_root, "description", convert=html_parser.unescape, quiet=True)}

    # Grab location info
    location = xml_root.find("location")
    if location is not None:
        data.update({"city": xml_subelement_text(location, "city"),
                     "country": xml_subelement_text(location, "country"),
                     "postalcode": xml_subelement_text(location, "postalcode"),
                     "addr1": xml_subelement_text(location, "addr1"),
                     "addr2": xml_subelement_text(location, "addr2"),
                     "stateorprovince": xml_subelement_text(location, "stateorprovince")})

    members = xml_root.find("members")
    data["member_count"] = int(members.attrib["count"])

    return Guild(data)


def add_guild_members_from_xml(guild, xml_root):
    """
    Processes the XML and adds members to ``guild``
    :param guild: the :py:class:`boardgamegeek.Guild` object to add members to
    :param xml_root: XML node
    :return: True if at least a member was added, False otherwise
    """

    added_member = False
    for member in xml_root.findall(".//member"):
        guild.add_member(member.attrib["name"])
        added_member = True

    return added_member
