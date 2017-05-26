import tempfile

from tenable_io.api.workbenches import WorkbenchesApi
from tenable_io.parser.workbenches import WorkbenchParser
from tenable_io.util import wait_until


class WorkbenchHelper(object):

    DEFAULT_PAGE_SIZE = 10

    def __init__(self, client):
        self._client = client

    def assets(self, date_range=1, plugin_id=None, page_size=DEFAULT_PAGE_SIZE):
        """Retrieve recorded assets.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param plugin_id: If specified, returns only assets with vulnerabilities found by the plugin identified by
            plugin_id, default to None.
        :param page_size: The page size of the pages returns by the iterator, default to DEFAULT_PAGE_SIZE.
        :raise TenableIOApiException:  When API error is encountered.
        :return: Iterator that yields pages of :class:`AssetVulnerabilities`.
        """
        return self.assets_parse(date_range, plugin_id, page_size)

    def assets_api(self, date_range=1, plugin_id=None):
        """Retrieve recorded assets.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param plugin_id: If specified, returns only assets with vulnerabilities found by the plugin identified by
            plugin_id, default to None.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`AssetVulnerabilities`.
        """
        asset_vulnerability_list = self._client.workbenches_api.assets_vulnerabilities(date_range)
        severities_by_id = {a.id: a.severities for a in asset_vulnerability_list.assets}
        asset_list = self._client.workbenches_api.assets(date_range=date_range)
        for asset in asset_list.assets:
            if asset.id in severities_by_id:
                asset.severities = severities_by_id[asset.id]

        if plugin_id is not None:
            vulnerability_assets_ids = self._vulnerability_asset_ids(plugin_id, date_range)
            return [asset for asset in asset_list.assets if asset.id in vulnerability_assets_ids]
        else:
            return asset_list.assets

    def _vulnerability_asset_ids(self, plugin_id, date_range=1):
        vulnerability_assets_ids = []
        vulnerability_output_list = self._client.workbenches_api.vulnerability_output(plugin_id, date_range=date_range)

        for vulnerability_plugin_output in vulnerability_output_list.outputs:
            for vulnerability_plugin_output_state in vulnerability_plugin_output.states:
                for vulnerability_output in vulnerability_plugin_output_state.results:
                    for asset in vulnerability_output.assets:
                        # Merge asset IDs for this vulnerability
                        vulnerability_assets_ids.append(asset['id'])

        # Remove duplicates
        vulnerability_assets_ids = list(set(vulnerability_assets_ids))

        return vulnerability_assets_ids

    def assets_parse(self, date_range=1, plugin_id=None, page_size=DEFAULT_PAGE_SIZE):
        """Retrieve recorded assets from the workbench nessus report.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param plugin_id: If specified, returns only assets with vulnerabilities found by the plugin identified by
            plugin_id, default to None.
        :param page_size: The page size of the pages returns by the iterator, default to DEFAULT_PAGE_SIZE.
        :raise TenableIOApiException:  When API error is encountered.
        :return: Iterator that yields pages of :class:`AssetVulnerabilities`.
        """
        file_id = self._client.workbenches_api.export_request(
            WorkbenchesApi.FORMAT_NESSUS,
            WorkbenchesApi.REPORT_VULNERABILITIES,
            WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
            date_range=date_range,
            plugin_id=plugin_id,
            filters=[{
                'quality': 'qt',
                'filter': 'severity',
                'value': 'All',
            }],
        )

        wait_until(lambda: self._client.workbenches_api.export_status(file_id) == WorkbenchesApi.STATUS_EXPORT_READY)

        iter_content = self._client.workbenches_api.export_download(file_id)

        with tempfile.NamedTemporaryFile() as temp:

            for chunk in iter_content:
                temp.write(chunk)
                temp.flush()

            assets = []
            try:
                gen = WorkbenchParser.parse(temp.name)
                while True:
                    report = next(gen)
                    assets.append(AssetVulnerabilities().from_report(report))
                    if page_size and len(assets) >= page_size:
                        yield assets
                        assets = []
                pass
            except StopIteration:
                pass

        if len(assets) > 0:
            yield assets

    def vulnerabilities(self, date_range=1, asset_id=None, page_size=DEFAULT_PAGE_SIZE):
        """Retrieve recorded vulnerabilities from the workbench nessus report.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param asset_id: If specified, returns only vulnerabilities for the asset identified by asset_id, default to
            None.
        :param page_size: The page size of the pages returns by the iterator, default to DEFAULT_PAGE_SIZE.
        :raise TenableIOApiException:  When API error is encountered.
        :return: Iterator that yields pages of :class:`Vulnerability`.
        """
        return self.vulnerabilities_parse(date_range, asset_id, page_size)

    def vulnerabilities_api(self, date_range=1, asset_id=None):
        """Retrieve recorded vulnerabilities.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param asset_id: If specified, returns only vulnerabilities for the asset identified by asset_id, default to
            None.
        :raise TenableIOApiException:  When API error is encountered.
        :return: A list of :class:`Vulnerability`.
        """
        if asset_id is not None:
            vulnerabilities = self._client.workbenches_api.asset_vulnerabilities(
                asset_id, date_range=date_range).vulnerabilities
        else:
            vulnerabilities = self._client.workbenches_api.vulnerabilities(date_range=date_range).vulnerabilities
        return vulnerabilities

    def vulnerabilities_parse(self, date_range=1, asset_id=None, page_size=DEFAULT_PAGE_SIZE):
        """Retrieve recorded vulnerabilities from the workbench nessus report.

        :param date_range: The number of days of data prior to today to return, default to 1.
        :param asset_id: If specified, returns only vulnerabilities for the asset identified by asset_id, default to
            None.
        :param page_size: The page size of the pages returns by the iterator, default to DEFAULT_PAGE_SIZE.
        :raise TenableIOApiException:  When API error is encountered.
        :return: Iterator that yields pages of :class:`Vulnerability`.
        """
        file_id = self._client.workbenches_api.export_request(
            WorkbenchesApi.FORMAT_NESSUS,
            WorkbenchesApi.REPORT_VULNERABILITIES,
            WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
            date_range=date_range,
            asset_id=asset_id,
            filters=[{
                'quality': 'qt',
                'filter': 'severity',
                'value': 'All',
            }]
        )

        wait_until(lambda: self._client.workbenches_api.export_status(file_id) == WorkbenchesApi.STATUS_EXPORT_READY)

        iter_content = self._client.workbenches_api.export_download(file_id)

        with tempfile.NamedTemporaryFile() as temp:

            for chunk in iter_content:
                temp.write(chunk)
                temp.flush()

            vulnerabilities = []
            try:
                gen = WorkbenchParser.parse(temp.name, tag=WorkbenchParser.REPORT_ITEM)
                while True:
                    report_item = next(gen)
                    vulnerabilities.append(Vulnerability().from_report_item(report_item))
                    if page_size and len(vulnerabilities) >= page_size:
                        yield vulnerabilities
                        vulnerabilities = []
                pass
            except StopIteration:
                pass

        if len(vulnerabilities) > 0:
            yield vulnerabilities

    def export(
            self,
            path,
            format=WorkbenchesApi.FORMAT_NESSUS,
            report=WorkbenchesApi.REPORT_VULNERABILITIES,
            chapter=WorkbenchesApi.CHAPTER_VULN_BY_ASSET,
            file_open_mode='wb',
            **kwargs
    ):
        """Download a workbench report.

        :param format: The file format. Default to WorkbenchesApi.FORMAT_NESSUS.
        :param report: The type of workbench report. Default to WorkbenchesApi.REPORT_VULNERABILITIES.
        :param chapter: Chapter to include. Default to WorkbenchesApi.CHAPTER_VULN_BY_ASSET.
        :param file_open_mode: Chapter to include, WorkbenchesApi.CHAPTER_VULN_BY_ASSET.
        :param **kwargs: Additional keyword arguments are the same as
            :class:`tenable_io.api.workbenches.WorkbenchesApi.export_request`
        :return: The same WorkbenchHelper instance.
        """
        file_id = self._client.workbenches_api.export_request(
            format,
            report,
            chapter,
            **kwargs
        )

        wait_until(lambda: self._client.workbenches_api.export_status(file_id) == WorkbenchesApi.STATUS_EXPORT_READY)

        iter_content = self._client.workbenches_api.export_download(file_id)
        with open(path, file_open_mode) as fd:
            for chunk in iter_content:
                fd.write(chunk)

        return self


class AssetVulnerabilities(object):

    def __init__(
            self,
            name=None,
            asset=None,
            vulnerabilities=None,
    ):
        self.name = name
        self.asset = asset
        self.vulnerabilities = vulnerabilities

    def from_report(self, report):
        self.name = report['report_host'].get('name')
        self.asset = Asset().host_properties(report['host_properties'])
        self.vulnerabilities = [Vulnerability().from_report_item(item) for item in report['report_items']]
        return self


class Vulnerability(object):

    def __init__(
            self,
            plugin_family=None,
            severity=None,
            protocol=None,
            plugin_name=None,
            plugin_id=None,
            svc_name=None,
            port=None,

            bid=None,
            canvas_package=None,
            cve=None,
            cvss_base_score=None,
            cvss_temporal_score=None,
            cvss_temporal_vector=None,
            cvss_vector=None,
            cvss3_base_score=None,
            cvss3_temporal_score=None,
            cvss3_temporal_vector=None,
            cvss3_vector=None,
            d2_elliot_name=None,
            description=None,
            exploit_available=None,
            exploited_by_nessus=None,
            exploit_framework_canvas=None,
            exploit_framework_core=None,
            exploit_framework_exploithub=None,
            exploit_framework_metasploit=None,
            exploit_framework_d2_elliot=None,
            exploited_by_malware=None,
            first_found=None,
            has_patch=None,
            in_the_news=None,
            last_found=None,
            last_fixed=None,
            malware=None,
            metasploit_name=None,
            patch_publication_date=None,
            plugin_modification_date=None,
            plugin_publication_date=None,
            plugin_output=None,
            plugin_type=None,
            plugin_version=None,
            risk_factor=None,
            solution=None,
            synopsis=None,
            unsupported_by_vendor=None,
            vulnerability_state=None,
            vuln_publication_date=None,
            xref=None,
            see_also=None,
    ):
        self.plugin_family = plugin_family
        self.severity = severity
        self.protocol = protocol
        self.plugin_name = plugin_name
        self.plugin_id = plugin_id
        self.svc_name = svc_name
        self.port = port

        self.bid = bid
        self.canvas_package = canvas_package
        self.cve = cve
        self.cvss_base_score = cvss_base_score
        self.cvss_temporal_score = cvss_temporal_score
        self.cvss_temporal_vector = cvss_temporal_vector
        self.cvss_vector = cvss_vector
        self.cvss3_base_score = cvss3_base_score
        self.cvss3_temporal_score = cvss3_temporal_score
        self.cvss3_temporal_vector = cvss3_temporal_vector
        self.cvss3_vector = cvss3_vector
        self.d2_elliot_name = d2_elliot_name
        self.description = description
        self.exploit_available = exploit_available
        self.exploited_by_nessus = exploited_by_nessus
        self.exploit_framework_canvas = exploit_framework_canvas
        self.exploit_framework_core = exploit_framework_core
        self.exploit_framework_exploithub = exploit_framework_exploithub
        self.exploit_framework_metasploit = exploit_framework_metasploit
        self.exploit_framework_d2_elliot = exploit_framework_d2_elliot
        self.exploited_by_malware = exploited_by_malware
        self.first_found = first_found
        self.has_patch = has_patch
        self.in_the_news = in_the_news
        self.last_found = last_found
        self.last_fixed = last_fixed
        self.malware = malware
        self.metasploit_name = metasploit_name
        self.patch_publication_date = patch_publication_date
        self.plugin_modification_date = plugin_modification_date
        self.plugin_publication_date = plugin_publication_date
        self.plugin_output = plugin_output
        self.plugin_type = plugin_type
        self.plugin_version = plugin_version
        self.risk_factor = risk_factor
        self.solution = solution
        self.synopsis = synopsis
        self.unsupported_by_vendor = unsupported_by_vendor
        self.vulnerability_state = vulnerability_state
        self.vuln_publication_date = vuln_publication_date
        self.xref = xref
        self.see_also = see_also

    def from_report_item(self, report_item):
        self.plugin_family = report_item.get('pluginFamily')
        self.severity = report_item.get('severity')
        self.protocol = report_item.get('protocol')
        self.plugin_name = report_item.get('pluginName')
        self.plugin_id = report_item.get('pluginID')
        self.svc_name = report_item.get('svc_name')
        self.port = report_item.get('port')

        self.bid = report_item.get('bid')
        self.canvas_package = report_item.get('canvas_package')
        self.cve = report_item.get('cve')
        self.cvss_base_score = report_item.get('cvss_base_score')
        self.cvss_temporal_score = report_item.get('cvss_temporal_score')
        self.cvss_temporal_vector = report_item.get('cvss_temporal_vector')
        self.cvss_vector = report_item.get('cvss_vector')
        self.cvss3_base_score = report_item.get('cvss3_base_score')
        self.cvss3_temporal_score = report_item.get('cvss3_temporal_score')
        self.cvss3_temporal_vector = report_item.get('cvss3_temporal_vector')
        self.cvss3_vector = report_item.get('cvss3_vector')
        self.d2_elliot_name = report_item.get('d2_elliot_name')
        self.description = report_item.get('description')
        self.exploit_available = report_item.get('exploit_available')
        self.exploited_by_nessus = report_item.get('exploited_by_nessus')
        self.exploit_framework_canvas = report_item.get('exploit_framework_canvas')
        self.exploit_framework_core = report_item.get('exploit_framework_core')
        self.exploit_framework_exploithub = report_item.get('exploit_framework_exploithub')
        self.exploit_framework_metasploit = report_item.get('exploit_framework_metasploit')
        self.exploit_framework_d2_elliot = report_item.get('exploit_framework_d2_elliot')
        self.exploited_by_malware = report_item.get('exploited_by_malware')
        self.first_found = report_item.get('first_found')
        self.has_patch = report_item.get('has_patch')
        self.in_the_news = report_item.get('in_the_news')
        self.last_found = report_item.get('last_found')
        self.last_fixed = report_item.get('last_fixed')
        self.malware = report_item.get('malware')
        self.metasploit_name = report_item.get('metasploit_name')
        self.patch_publication_date = report_item.get('patch_publication_date')
        self.plugin_modification_date = report_item.get('plugin_modification_date')
        self.plugin_publication_date = report_item.get('plugin_publication_date')
        self.plugin_output = report_item.get('plugin_output')
        self.plugin_type = report_item.get('plugin_type')
        self.plugin_version = report_item.get('plugin_version')
        self.risk_factor = report_item.get('risk_factor')
        self.solution = report_item.get('solution')
        self.synopsis = report_item.get('synopsis')
        self.unsupported_by_vendor = report_item.get('unsupported_by_vendor')
        self.vulnerability_state = report_item.get('vulnerability_state')
        self.vuln_publication_date = report_item.get('vuln_publication_date')
        self.xref = report_item.get('xref')
        self.see_also = report_item.get('see_also')
        return self


class Asset(object):

    def __init__(
            self,
            bios_uuid=None,
            host_fqdn=None,
            hostname=None,
            host_ip=None,
            host_uuid=None,
            host_start=None,
            host_end=None,
            local_checks_proto=None,
            mac_address=None,
            mcafee_epo_guid=None,
            netbios_name=None,
            operating_system=None,
            system_type=None,
    ):
        self.bios_uuid = bios_uuid
        self.host_fqdn = host_fqdn
        self.hostname = hostname
        self.host_ip = host_ip
        self.host_uuid = host_uuid
        self.host_start = host_start
        self.host_end = host_end
        self.local_checks_proto = local_checks_proto
        self.mac_address = mac_address
        self.mcafee_epo_guid = mcafee_epo_guid
        self.netbios_name = netbios_name
        self.operating_system = operating_system
        self.system_type = system_type

    def host_properties(self, host_properties):
        self.bios_uuid = host_properties.get('bios-uuid')
        self.host_fqdn = host_properties.get('host-fqdn')
        self.hostname = host_properties.get('hostname')
        self.host_ip = host_properties.get('host-ip')
        self.host_uuid = host_properties.get('host-uuid')
        self.host_start = host_properties.get('HOST_START')
        self.host_end = host_properties.get('HOST_END')
        self.local_checks_proto = host_properties.get('local-checks-proto')
        self.mac_address = host_properties.get('mac-address')
        self.mcafee_epo_guid = host_properties.get('mcafee-epo-guid')
        self.netbios_name = host_properties.get('netbios-name')
        self.operating_system = host_properties.get('operating-system')
        self.system_type = host_properties.get('system-type')
        return self
