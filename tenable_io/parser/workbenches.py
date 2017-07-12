import xml.etree.cElementTree as ET

from tenable_io.exceptions import TenableIOException
from tenable_io.log import logging


class WorkbenchParser(object):

    HOST_PROPERTIES = 'HostProperties'
    REPORT_HOST = 'ReportHost'
    REPORT_ITEM = 'ReportItem'

    @staticmethod
    def parse(path, tag=REPORT_HOST):
        """Parse Nessus XML export from Workbench API into dicts.

        :param path: The file path.
        :param tag: The XML tag to iterate on. It should be WorkbenchParser.REPORT_HOST or WorkbenchParser.REPORT_ITEM.
        """
        assert tag in [WorkbenchParser.REPORT_HOST, WorkbenchParser.REPORT_ITEM], u'Valid tag for parsing.'

        report_host = None
        host_properties = None
        report_items = [] if tag == WorkbenchParser.REPORT_HOST else None

        try:
            for event, elem in ET.iterparse(path, events=('start', 'end')):

                if event == 'start':
                    if elem.tag == 'ReportHost':
                        report_host = WorkbenchParser._from_report_host(elem)

                if event == 'end':

                    if elem.tag == WorkbenchParser.REPORT_HOST:
                        elem.clear()
                        if tag == elem.tag:
                            yield {
                                'report_host': report_host,
                                'host_properties': host_properties,
                                'report_items': report_items,
                            }
                            report_items = []

                    if elem.tag == WorkbenchParser.HOST_PROPERTIES:
                        host_properties = WorkbenchParser._from_host_properties(elem)
                        elem.clear()

                    if elem.tag == WorkbenchParser.REPORT_ITEM:
                        report_item = WorkbenchParser._from_report_item(elem)
                        elem.clear()
                        if tag == elem.tag:
                            yield report_item
                        elif tag == WorkbenchParser.REPORT_HOST:
                            report_items.append(report_item)
        except ET.ParseError as e:
            logging.warn(u'Failed to parse Nessus XML: ' + e.msg)
            # TODO The service return malformed XML for empty set, for now we won't raise an exception for what should
            # TODO be a normal state. However, this might masked out real error from bubble up (unlikely).
            # raise TenableIOException(u'Failed to parse Nessus XML: ' + e.message)

    @staticmethod
    def _from_report_host(elem):
        return dict(elem.attrib)

    @staticmethod
    def _from_host_properties(elem):
        host_properties = {}
        for tag in elem.findall('tag'):
            name = tag.get('name')
            if name in ['mac-address']:
                host_properties[name] = tag.text.split() if isinstance(tag.text, str) else tag.text
            else:
                host_properties[name] = tag.text
        return host_properties

    @staticmethod
    def _from_report_item(elem):
        d = dict()
        for a in elem.attrib:
            d[a] = elem.attrib[a]
        for child in list(elem):
            if child.tag in ['bid', 'cve', 'xref', 'see_also']:
                if child.tag not in d:
                    d[child.tag] = []
                d[child.tag].append(child.text)
            else:
                d[child.tag] = child.text
        return d
