from io import StringIO

from django.utils.encoding import force_str
from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework_xml.renderers import XMLRenderer


class CustomXMLRender(XMLRenderer):
    root_tag_name = ""
    item_tag_name = ""
    attribute = {}
    nearest_postcode = {}

    def render(
        self, data, accepted_media_type=None, renderer_context=None
    ):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ""
        stream = StringIO()
        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, self.attribute)
        if self.root_tag_name == "outcode":
            xml.characters(force_str(data["outcode"]))
        else:
            self._to_xml(xml, data)
        xml.endElement(self.root_tag_name)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data, i=0):
        if isinstance(data, (list, tuple)):
            tag = self.item_tag_name
            for item in data:
                if i == 0 and self.root_tag_name == "outcodes":
                    xml.startElement(
                        tag, self.nearest_postcode[item["zipcode"]]
                    )
                else:
                    xml.startElement(tag, {})
                self._to_xml(xml, item, i + 1)
                xml.endElement(tag)
        elif isinstance(data, dict):
            xml.characters(force_str(data["zipcode"]))

        elif data is None:
            # Don't output any value
            pass
        else:
            xml.characters(force_str(data))


class XMLGenerator(CustomXMLRender):
    @classmethod
    def startup(
        cls, root_tag, item_tag, attribute, nearest_postcode={}
    ):
        cls.root_tag_name = root_tag
        cls.item_tag_name = item_tag
        cls.attribute = attribute
        cls.nearest_postcode = nearest_postcode
