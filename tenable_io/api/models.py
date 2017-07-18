from json import loads

from tenable_io.exceptions import TenableIOException
from tenable_io.util import payload_filter


class BaseModel(object):

    @classmethod
    def from_json(cls, json):
        return cls.from_dict(loads(json))

    @classmethod
    def from_dict(cls, dict_):
        instance = cls()
        for key in dict_:
            setattr(instance, key, dict_[key])
        return instance

    @classmethod
    def from_list(cls, list_):
        model_list = None
        if list_ is not None:
            model_list = []
            for item in list_:
                model_list.append(cls.from_dict(item))
        return model_list

    @classmethod
    def from_json_list(cls, json_list):
        return cls.from_list(loads(json_list))

    @staticmethod
    def _model_list(class_):
        """
        :param class_: The class that elements should be an instance of.
        :return: A decorator that ensures the assigning value is a list of `class_` instances.
        """
        assert issubclass(class_, BaseModel)

        def decorator(f):
            def wrapper(self, list_):
                if isinstance(list_, list):
                    model_list = []
                    for item in list_:
                        if isinstance(item, class_):
                            model_list.append(item)
                        elif isinstance(item, dict):
                            model_list.append(class_.from_dict(item))
                        else:
                            raise TenableIOException(u'Invalid element type.')
                    f(self, model_list)
                else:
                    f(self, [])
            return wrapper
        return decorator

    def as_payload(self, filter_=None):
        return payload_filter(self.__dict__, filter_)


class Agent(BaseModel):

    def __init__(
            self,
            distro=None,
            id=None,
            ip=None,
            last_scanned=None,
            name=None,
            platform=None,
            token=None,
            uuid=None
    ):
        self.distro = distro
        self.id = id
        self.ip = ip
        self.last_scanned = last_scanned
        self.name = name
        self.platform = platform
        self.token = token
        self.uuid = uuid


class AgentList(BaseModel):

    def __init__(
            self,
            agents=None
    ):
        self._agents = None
        self.agents = agents

    @property
    def agents(self):
        return self._agents

    @agents.setter
    @BaseModel._model_list(Agent)
    def agents(self, agents):
        self._agents = agents


class AgentGroup(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            owner_id=None,
            owner=None,
            shared=None,
            user_permissions=None,
            creation_date=None,
            last_modification_date=None
    ):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.owner = owner
        self.shared = shared
        self.user_permissions = user_permissions
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date


class AgentGroupList(BaseModel):

    def __init__(
            self,
            groups=None
    ):
        self._groups = None
        self.groups = groups

    @property
    def groups(self):
        return self._groups

    @groups.setter
    @BaseModel._model_list(AgentGroup)
    def groups(self, groups):
        self._groups = groups


class Exclusion(BaseModel):
    def __init__(
            self,
            id=None,
            name=None,
            description=None,
            schedule=None,
            creation_date=None,
            last_modification_date=None,
            members=None,
    ):
        self._schedule = None

        self.id = id
        self.name = name
        self.description = description
        self.schedule = schedule
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.members = members

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        if isinstance(schedule, ExclusionSchedule):
            self._schedule = schedule
        elif isinstance(schedule, dict):
            self._schedule = ExclusionSchedule.from_dict(schedule)
        else:
            self._schedule = None


class ExclusionList(BaseModel):
    def __init__(
            self,
            exclusions=None
    ):
        self._exclusions = None
        self.exclusions = exclusions

    @property
    def exclusions(self):
        return self._exclusions

    @exclusions.setter
    @BaseModel._model_list(Exclusion)
    def exclusions(self, exclusions):
        self._exclusions = exclusions


class ExclusionSchedule(BaseModel):

    def __init__(
            self,
            enabled=None,
            starttime=None,
            endtime=None,
            timezone=None,
            rrules=None
    ):
        self._rrules = None

        self.enabled = enabled
        self.starttime = starttime
        self.endtime = endtime
        self.timezone = timezone
        self.rrules = rrules

    @property
    def rrules(self):
        return self._rrules

    @rrules.setter
    def rrules(self, rrules):
        if isinstance(rrules, ExclusionRrules):
            self._rrules = rrules
        elif isinstance(rrules, dict):
            self._rrules = ExclusionRrules.from_dict(rrules)
        else:
            self._rrules = None

    def as_payload(self, filter_=None):
        payload = super(ExclusionSchedule, self).as_payload(True)
        if isinstance(self.rrules, ExclusionRrules):
            payload.__setitem__('rrules', self.rrules.as_payload(True))
        else:
            payload.pop('rrules', None)
        payload.pop('_rrules', None)
        return payload


class ExclusionRrules(BaseModel):

    def __init__(
            self,
            freq=None,
            interval=None,
            byweekday=None,
            bymonthday=None
    ):
        self.freq = freq
        self.interval = interval
        self.byweekday = byweekday
        self.bymonthday = bymonthday


class Folder(BaseModel):

    TYPE_CUSTOM = 'custom'
    TYPE_MAIN = 'main'
    TYPE_TRASH = 'trash'

    def __init__(
            self,
            id=None,
            name=None,
            type=None,
            default_tag=None,
            custom=None,
            unread_count=None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.default_tag = default_tag
        self.custom = custom
        self.unread_count = unread_count


class FolderList(BaseModel):

    def __init__(
            self,
            folders=None,
    ):
        self._folders = None

        self.folders = folders

    @property
    def folders(self):
        return self._folders

    @folders.setter
    @BaseModel._model_list(Folder)
    def folders(self, folders):
        self._folders = folders


class Group(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            permissions=None,
            user_count=None,
    ):
        self.id = id
        self.name = name
        self.permissions = permissions
        self.user_count = user_count


class GroupList(BaseModel):

    def __init__(
            self,
            groups=None,
    ):
        self._groups = None

        self.groups = groups

    @property
    def groups(self):
        return self._groups

    @groups.setter
    @BaseModel._model_list(Group)
    def groups(self, groups):
        self._groups = groups


class Plugin(BaseModel):

    def __init__(
            self,
            id=None,
            name=None
    ):
        self.id = id
        self.name = name


class PluginAttribute(BaseModel):

    def __init__(
            self,
            attribute_name=None,
            attribute_value=None
    ):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value


class PluginDetails(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            family_name=None,
            attributes=None
    ):
        self._attributes = None
        self.id = id
        self.name = name
        self.family_name = family_name
        self.attributes = attributes

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    @BaseModel._model_list(PluginAttribute)
    def attributes(self, attributes):
        self._attributes = attributes


class PluginFamily(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            count=None
    ):
        self.id = id
        self.name = name
        self.count = count


class PluginFamilyDetails(BaseModel):

    def __init__(
            self,
            id=None,
            name=None,
            plugins=None
    ):
        self._plugins = None
        self.id = id
        self.name = name
        self.plugins = plugins

    @property
    def plugins(self):
        return self._plugins

    @plugins.setter
    @BaseModel._model_list(Plugin)
    def plugins(self, plugins):
        self._plugins = plugins


class PluginFamilyList(BaseModel):

    def __init__(
            self,
            families=None
    ):
        self._families = None
        self.families = families

    @property
    def families(self):
        return self._families

    @families.setter
    @BaseModel._model_list(PluginFamily)
    def families(self, families):
        self._families = families


class Policy(BaseModel):

    def __init__(
            self,
            id=None,
            template_uuid=None,
            name=None,
            description=None,
            owner_id=None,
            owner=None,
            shared=None,
            user_permissions=None,
            creation_date=None,
            last_modification_date=None,
            visibility=None,
            no_target=None,
    ):
        self.id = id
        self.template_uuid = template_uuid
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.owner = owner
        self.shared = shared
        self.user_permissions = user_permissions
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.visibility = visibility
        self.no_target = no_target


class PolicyList(BaseModel):

    def __init__(
            self,
            policies=None,
    ):
        self._policies = None

        self.policies = policies

    @property
    def policies(self):
        return self._policies

    @policies.setter
    @BaseModel._model_list(Policy)
    def policies(self, policies):
        self._policies = policies


class PolicyAudits(BaseModel):

    def __init__(
            self,
            custom=None,
            feed=None,
    ):
        assert custom is None or isinstance(custom, PolicyAuditsCustom)
        assert feed is None or isinstance(feed, PolicyAuditsFeed)

        self.custom = custom
        self.feed = feed


class PolicyAuditsCustom(BaseModel):

    def __init__(
            self,
            add=None,
            delete=None,
            edit=None
    ):
        assert add is None or len([a for a in add if isinstance(a, PolicyAuditsCustomItem)]) is len(add)

        self.add = add
        self.delete = delete
        self.edit = edit


class PolicyAuditsCustomItem(BaseModel):

    def __init__(
            self,
            category=None,
            file=None,
    ):
        self.category = category
        self.file = file


class PolicyAuditsFeed(BaseModel):

    def __init__(
            self,
            add=None,
            delete=None,
            edit=None
    ):
        assert add is None or len([a for a in add if isinstance(a, PolicyAuditsFeedItem)]) is len(add)

        self.add = add
        self.delete = delete
        self.edit = edit


class PolicyAuditsFeedItem(BaseModel):

    def __init__(
            self,
            id=None,
            variables=None,
    ):
        self.id = id
        self.variables = variables


class PolicyCredentials(BaseModel):

    def __init__(
            self,
            add=None,
            delete=None,
            edit=None,
    ):
        self.add = add
        self.delete = delete
        self.edit = edit


class PolicySCAP(BaseModel):

    def __init__(
            self,
            add=None,
            delete=None,
            edit=None,
    ):
        self.add = add
        self.delete = delete
        self.edit = edit


class PolicySettings(BaseModel):

    def __init__(
            self,
            acls=[],
            additional_snmp_port1=None,
            additional_snmp_port2=None,
            additional_snmp_port3=None,
            adtran_aos_offline_configs=None,
            allow_post_scan_editing=None,
            apm_force_updates=None,
            apm_update_timeout=None,
            arp_ping=None,
            av_grace_period=None,
            aws_ap_northeast_1=None,
            aws_ap_southeast_1=None,
            aws_ap_southeast_2=None,
            aws_eu_west_1=None,
            aws_sa_east_1=None,
            aws_ui_region_type=None,
            aws_us_east_1=None,
            aws_us_gov_west_1=None,
            aws_us_west_1=None,
            aws_us_west_2=None,
            aws_use_https=None,
            aws_verify_ssl=None,
            brocade_offline_configs=None,
            check_crl=None,
            cisco_config_to_audit=None,
            cisco_offline_configs=None,
            dell_f10_offline_configs=None,
            description=None,
            detect_ssl=None,
            display_unreachable_hosts=None,
            dont_use_ntlmv1=None,
            enable_admin_shares=None,
            enum_domain_users_end_uid=None,
            enum_domain_users_start_uid=None,
            enum_local_users_end_uid=None,
            enum_local_users_start_uid=None,
            enumerate_all_ciphers=None,
            extremeos_offline_configs=None,
            fast_network_discovery=None,
            fireeye_offline_configs=None,
            host_whitelist=None,
            http_login_auth_regex_nocase=None,
            http_login_auth_regex_on_headers=None,
            http_login_invert_auth_regex=None,
            http_login_max_redir=None,
            http_login_method=None,
            huawei_offline_configs=None,
            icmp_ping=None,
            icmp_ping_retries=None,
            icmp_unreach_means_host_down=None,
            junos_offline_configs=None,
            log_live_hosts=None,
            log_whole_attack=None,
            max_checks_per_host=None,
            max_hosts_per_scan=None,
            max_simult_tcp_sessions_per_host=None,
            max_simult_tcp_sessions_per_scan=None,
            modbus_end_reg=None,
            modbus_start_reg=None,
            name=None,
            netapp_offline_configs=None,
            network_receive_timeout=None,
            network_type=None,
            never_send_win_creds_in_the_clear=None,
            only_portscan_if_enum_failed=None,
            patch_audit_over_rexec=None,
            patch_audit_over_rsh=None,
            patch_audit_over_telnet=None,
            ping_the_remote_host=None,
            portscan_range=None,
            procurve_config_to_audit=None,
            procurve_offline_configs=None,
            provided_creds_only=None,
            reduce_connections_on_congestion=None,
            report_paranoia=None,
            report_superseded_patches=None,
            report_verbosity=None,
            request_windows_domain_info=None,
            reverse_lookup=None,
            safe_checks=None,
            scan_netware_hosts=None,
            scan_network_printers=None,
            scan_webapps=None,
            silent_dependencies=None,
            slice_network_addresses=None,
            smtp_domain=None,
            smtp_from=None,
            smtp_to=None,
            snmp_port=None,
            snmp_scanner=None,
            sonicos_offline_configs=None,
            ssh_client_banner=None,
            ssh_known_hosts=None,
            ssh_netstat_scanner=None,
            ssh_port=None,
            ssl_prob_ports=None,
            start_cotp_tsap=None,
            start_remote_registry=None,
            stop_cotp_tsap=None,
            stop_scan_on_disconnect=None,
            svc_detection_on_all_ports=None,
            syn_firewall_detection=None,
            syn_scanner=None,
            tcp_firewall_detection=None,
            tcp_ping=None,
            tcp_ping_dest_ports=None,
            tcp_scanner=None,
            test_default_oracle_accounts=None,
            test_local_nessus_host=None,
            thorough_tests=None,
            udp_ping=None,
            udp_scanner=None,
            unscanned_closed=None,
            verify_open_ports=None,
            win_known_bad_hashes=None,
            win_known_good_hashes=None,
            wmi_netstat_scanner=None,
            wol_mac_addresses=None,
            wol_wait_time=None,
    ):
        self.acls = acls
        self.additional_snmp_port1 = additional_snmp_port1
        self.additional_snmp_port2 = additional_snmp_port2
        self.additional_snmp_port3 = additional_snmp_port3
        self.adtran_aos_offline_configs = adtran_aos_offline_configs
        self.allow_post_scan_editing = allow_post_scan_editing
        self.apm_force_updates = apm_force_updates
        self.apm_update_timeout = apm_update_timeout
        self.arp_ping = arp_ping
        self.av_grace_period = av_grace_period
        self.aws_ap_northeast_1 = aws_ap_northeast_1
        self.aws_ap_southeast_1 = aws_ap_southeast_1
        self.aws_ap_southeast_2 = aws_ap_southeast_2
        self.aws_eu_west_1 = aws_eu_west_1
        self.aws_sa_east_1 = aws_sa_east_1
        self.aws_ui_region_type = aws_ui_region_type
        self.aws_us_east_1 = aws_us_east_1
        self.aws_us_gov_west_1 = aws_us_gov_west_1
        self.aws_us_west_1 = aws_us_west_1
        self.aws_us_west_2 = aws_us_west_2
        self.aws_use_https = aws_use_https
        self.aws_verify_ssl = aws_verify_ssl
        self.brocade_offline_configs = brocade_offline_configs
        self.check_crl = check_crl
        self.cisco_config_to_audit = cisco_config_to_audit
        self.cisco_offline_configs = cisco_offline_configs
        self.dell_f10_offline_configs = dell_f10_offline_configs
        self.description = description
        self.detect_ssl = detect_ssl
        self.display_unreachable_hosts = display_unreachable_hosts
        self.dont_use_ntlmv1 = dont_use_ntlmv1
        self.enable_admin_shares = enable_admin_shares
        self.enum_domain_users_end_uid = enum_domain_users_end_uid
        self.enum_domain_users_start_uid = enum_domain_users_start_uid
        self.enum_local_users_end_uid = enum_local_users_end_uid
        self.enum_local_users_start_uid = enum_local_users_start_uid
        self.enumerate_all_ciphers = enumerate_all_ciphers
        self.extremeos_offline_configs = extremeos_offline_configs
        self.fast_network_discovery = fast_network_discovery
        self.fireeye_offline_configs = fireeye_offline_configs
        self.host_whitelist = host_whitelist
        self.http_login_auth_regex_nocase = http_login_auth_regex_nocase
        self.http_login_auth_regex_on_headers = http_login_auth_regex_on_headers
        self.http_login_invert_auth_regex = http_login_invert_auth_regex
        self.http_login_max_redir = http_login_max_redir
        self.http_login_method = http_login_method
        self.huawei_offline_configs = huawei_offline_configs
        self.icmp_ping = icmp_ping
        self.icmp_ping_retries = icmp_ping_retries
        self.icmp_unreach_means_host_down = icmp_unreach_means_host_down
        self.junos_offline_configs = junos_offline_configs
        self.log_live_hosts = log_live_hosts
        self.log_whole_attack = log_whole_attack
        self.max_checks_per_host = max_checks_per_host
        self.max_hosts_per_scan = max_hosts_per_scan
        self.max_simult_tcp_sessions_per_host = max_simult_tcp_sessions_per_host
        self.max_simult_tcp_sessions_per_scan = max_simult_tcp_sessions_per_scan
        self.modbus_end_reg = modbus_end_reg
        self.modbus_start_reg = modbus_start_reg
        self.name = name
        self.netapp_offline_configs = netapp_offline_configs
        self.network_receive_timeout = network_receive_timeout
        self.network_type = network_type
        self.never_send_win_creds_in_the_clear = never_send_win_creds_in_the_clear
        self.only_portscan_if_enum_failed = only_portscan_if_enum_failed
        self.patch_audit_over_rexec = patch_audit_over_rexec
        self.patch_audit_over_rsh = patch_audit_over_rsh
        self.patch_audit_over_telnet = patch_audit_over_telnet
        self.ping_the_remote_host = ping_the_remote_host
        self.portscan_range = portscan_range
        self.procurve_config_to_audit = procurve_config_to_audit
        self.procurve_offline_configs = procurve_offline_configs
        self.provided_creds_only = provided_creds_only
        self.reduce_connections_on_congestion = reduce_connections_on_congestion
        self.report_paranoia = report_paranoia
        self.report_superseded_patches = report_superseded_patches
        self.report_verbosity = report_verbosity
        self.request_windows_domain_info = request_windows_domain_info
        self.reverse_lookup = reverse_lookup
        self.safe_checks = safe_checks
        self.scan_netware_hosts = scan_netware_hosts
        self.scan_network_printers = scan_network_printers
        self.scan_webapps = scan_webapps
        self.silent_dependencies = silent_dependencies
        self.slice_network_addresses = slice_network_addresses
        self.smtp_domain = smtp_domain
        self.smtp_from = smtp_from
        self.smtp_to = smtp_to
        self.snmp_port = snmp_port
        self.snmp_scanner = snmp_scanner
        self.sonicos_offline_configs = sonicos_offline_configs
        self.ssh_client_banner = ssh_client_banner
        self.ssh_known_hosts = ssh_known_hosts
        self.ssh_netstat_scanner = ssh_netstat_scanner
        self.ssh_port = ssh_port
        self.ssl_prob_ports = ssl_prob_ports
        self.start_cotp_tsap = start_cotp_tsap
        self.start_remote_registry = start_remote_registry
        self.stop_cotp_tsap = stop_cotp_tsap
        self.stop_scan_on_disconnect = stop_scan_on_disconnect
        self.svc_detection_on_all_ports = svc_detection_on_all_ports
        self.syn_firewall_detection = syn_firewall_detection
        self.syn_scanner = syn_scanner
        self.tcp_firewall_detection = tcp_firewall_detection
        self.tcp_ping = tcp_ping
        self.tcp_ping_dest_ports = tcp_ping_dest_ports
        self.tcp_scanner = tcp_scanner
        self.test_default_oracle_accounts = test_default_oracle_accounts
        self.test_local_nessus_host = test_local_nessus_host
        self.thorough_tests = thorough_tests
        self.udp_ping = udp_ping
        self.udp_scanner = udp_scanner
        self.unscanned_closed = unscanned_closed
        self.verify_open_ports = verify_open_ports
        self.win_known_bad_hashes = win_known_bad_hashes
        self.win_known_good_hashes = win_known_good_hashes
        self.wmi_netstat_scanner = wmi_netstat_scanner
        self.wol_mac_addresses = wol_mac_addresses
        self.wol_wait_time = wol_wait_time


class PolicyDetails(BaseModel):

    def __init__(
            self,
            uuid=None,
            audits=None,
            credentials=None,
            plugins=None,
            scap=None,
            settings=None,
    ):
        self._settings = None

        self.uuid = uuid
        self.audits = audits
        self.credentials = credentials
        self.plugins = plugins
        self.scap = scap
        self.settings = settings

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if isinstance(settings, PolicySettings):
            self._settings = settings
        elif isinstance(settings, dict):
            self._settings = PolicySettings.from_dict(settings)
        else:
            self._settings = None


class Scan(BaseModel):

    STATUS_ABORTED = u'aborted'
    STATUS_CANCELED = u'canceled'
    STATUS_COMPLETED = u'completed'
    STATUS_EMPTY = u'empty'
    STATUS_IMPORTED = u'imported'
    STATUS_PAUSED = u'paused'
    STATUS_PAUSING = u'pausing'
    STATUS_PENDING = u'pending'
    STATUS_RESUMING = u'resuming'
    STATUS_RUNNING = u'running'
    STATUS_STOPPING = u'stopping'

    def __init__(
            self,
            id=None,
            uuid=None,
            name=None,
            type=None,
            owner=None,
            enabled=None,
            folder_id=None,
            read=None,
            status=None,
            shared=None,
            user_permissions=None,
            creation_date=None,
            last_modification_date=None,
            control=None,
            starttime=None,
            timezone=None,
            rrules=None,
    ):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.type = type
        self.owner = owner
        self.enabled = enabled
        self.folder_id = folder_id
        self.read = read
        self.status = status
        self.shared = shared
        self.user_permissions = user_permissions
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date
        self.control = control
        self.starttime = starttime
        self.timezone = timezone
        self.rrules = rrules


class ScanDetailsHistory(BaseModel):
    def __init__(
            self,
            history_id=None,
            uuid=None,
            owner_id=None,
            status=None,
            creation_date=None,
            last_modification_date=None,
    ):
        self.history_id = history_id
        self.uuid = uuid
        self.owner_id = owner_id
        self.status = status
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date


class ScanDetails(BaseModel):

    def __init__(
            self,
            info=None,
            hosts=None,
            comphosts=None,
            notes=None,
            remediations=None,
            vulnerabilities=None,
            compliance=None,
            history=None,
            filters=None,
    ):
        self._info = None
        self._history = None

        self.info = info
        self.hosts = hosts
        self.comphosts = comphosts
        self.notes = notes
        self.remediations = remediations
        self.vulnerabilities = vulnerabilities
        self.compliance = compliance
        self.history = history
        self.filters = filters

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, info):
        if isinstance(info, ScanInfo):
            self._info = info
        elif isinstance(info, dict):
            self._info = ScanInfo.from_dict(info)
        else:
            self._info = None

    @property
    def history(self):
        return self._history

    @history.setter
    @BaseModel._model_list(ScanDetailsHistory)
    def history(self, history):
        self._history = history


class ScanHistory(BaseModel):

    def __init__(
            self,
            name=None,
            object_id=None,
            owner=None,
            owner_id=None,
            owner_uuid=None,
            scan_end=None,
            scan_start=None,
            scan_type=None,
            schedule_uuid=None,
            status=None,
            targets=None,
            uuid=None,
    ):
        self.name = name
        self.object_id = object_id
        self.owner = owner
        self.owner_id = owner_id
        self.owner_uuid = owner_uuid
        self.scan_end = scan_end
        self.scan_start = scan_start
        self.scan_type = scan_type
        self.schedule_uuid = schedule_uuid
        self.status = status
        self.targets = targets
        self.uuid = uuid


class ScanInfo(BaseModel):

    def __init__(
            self,
            acls=None,
            edit_allowed=None,
            status=None,
            policy=None,
            pci_can_upload=None,  # API uses "pci-can-upload" which is not a valid python attribute name.
            hasaudittrail=None,
            scan_start=None,
            folder_id=None,
            targets=None,
            timestamp=None,
            object_id=None,
            scanner_name=None,
            haskb=None,
            uuid=None,
            hostcount=None,
            scan_end=None,
            name=None,
            user_permissions=None,
            control=None,
    ):
        self.acls = acls
        self.edit_allowed = edit_allowed
        self.status = status
        self.policy = policy
        self.pci_can_upload = pci_can_upload
        self.hasaudittrail = hasaudittrail
        self.scan_start = scan_start
        self.folder_id = folder_id
        self.targets = targets
        self.timestamp = timestamp
        self.object_id = object_id
        self.scanner_name = scanner_name
        self.haskb = haskb
        self.uuid = uuid
        self.hostcount = hostcount
        self.scan_end = scan_end
        self.name = name
        self.user_permissions = user_permissions
        self.control = control

    @classmethod
    def from_dict(cls, dict_):
        # Because API uses "pci-can-upload" API uses "pci-can-upload" which is not a valid python attribute name.
        if 'pci-can-upload' in dict_:
            dict_['pci_can_upload'] = dict_.pop('pci-can-upload')
        return super(ScanInfo, cls).from_dict(dict_)

    def as_payload(self, filter_=None):
        # Because API uses "pci-can-upload" API uses "pci-can-upload" which is not a valid python attribute name.
        payload = self.as_payload(filter_)
        if 'pci_can_upload' in payload:
            payload['pci-can-upload'] = payload.pop('pci_can_upload')
        return payload


class ScanList(BaseModel):

    def __init__(
            self,
            folders=None,
            scans=None,
            timestamp=None,
    ):
        self._scans = None
        self.folders = folders
        self.scans = scans
        self.timestamp = timestamp

    @property
    def scans(self):
        return self._scans

    @scans.setter
    @BaseModel._model_list(Scan)
    def scans(self, scans):
        self._scans = scans


class ScanSettings(BaseModel):

    def __init__(
            self,
            name,
            text_targets,
            description=None,
            emails=None,
            enabled=False,
            launch=None,
            folder_id=None,
            policy_id=None,
            scanner_id=None,
    ):
        self.name = name
        self.description = description
        self.emails = emails
        self.enabled = enabled
        self.launch = launch
        self.folder_id = folder_id
        self.policy_id = policy_id
        self.scanner_id = scanner_id
        self.text_targets = text_targets


class Scanner(BaseModel):

    def __init__(
            self,
            id=None,
            uuid=None,
            name=None,
            type=None,
            status=None,
            scan_count=None,
            engine_version=None,
            platform=None,
            loaded_plugin_set=None,
            registration_code=None,
            owner=None,
            key=None,
            license=None
    ):
        self._license = None

        self.id = id
        self.uuid = uuid
        self.name = name
        self.type = type
        self.status = status
        self.scan_count = scan_count
        self.engine_version = engine_version
        self.platform = platform
        self.loaded_plugin_set = loaded_plugin_set
        self.registration_code = registration_code
        self.owner = owner
        self.key = key
        self.license = license

    @property
    def license(self):
        return self._license

    @license.setter
    def license(self, license):
        if isinstance(license, ScannerLicense):
            self._license = license
        elif isinstance(license, dict):
            self._license = ScannerLicense.from_dict(license)
        else:
            self._license = None


class ScannerAwsTarget(BaseModel):

    def __init__(
            self,
            scanner_id=None,
            instance_id=None,
            private_ip=None,
            public_ip=None,
            state=None,
            zone=None,
            type=None,
            name=None
    ):
        self.scanner_id = scanner_id
        self.instance_id = instance_id
        self.private_ip = private_ip
        self.public_ip = public_ip
        self.state = state
        self.zone = zone
        self.type = type
        self.name = name


class ScannerAwsTargetList(BaseModel):

    def __init__(
            self,
            aws_targets=None
    ):
        self._aws_targets = None
        self._aws_targets = aws_targets

    @property
    def aws_targets(self):
        return self._aws_targets

    @aws_targets.setter
    @BaseModel._model_list(ScannerAwsTarget)
    def aws_targets(self, aws_targets):
        self.aws_targets = aws_targets


class ScannerLicense(BaseModel):

    def __init__(
            self,
            type=None,
            ips=None,
            agents=None,
            scanners=None
    ):
        self.type = type
        self.ips = ips
        self.agents = agents
        self.scanners = scanners


class ScannerList(BaseModel):

    def __init__(
            self,
            scanners=None
    ):
        self._scanners = None
        self.scanners = scanners

    @property
    def scanners(self):
        return self._scanners

    @scanners.setter
    @BaseModel._model_list(Scanner)
    def scanners(self, scanners):
        self._scanners = scanners


class ScannerScan(BaseModel):

    def __init__(
            self,
            scanner_uuid=None,
            name=None,
            status=None,
            id=None,
            scan_id=None,
            user=None,
            last_modification_date=None,
            start_time=None,
            remote=None
    ):
        self.scanner_uuid = scanner_uuid
        self.name = name
        self.status = status
        self.id = id
        self.scan_id = scan_id
        self.user = user
        self.last_modification_date = last_modification_date
        self.start_time = start_time
        self.remote = remote


class ScannerScanList(BaseModel):

    def __init__(
            self,
            scans=None
    ):
        self._scans = None
        self.scans = scans

    @property
    def scans(self):
        return self._scans

    @scans.setter
    @BaseModel._model_list(ScannerScan)
    def scans(self, scans):
        self._scans = scans


class ScContainer(BaseModel):
    def __init__(
            self,
            number_of_vulnerabilities=None,
            name=None,
            digest=None,
            score=None,
            id=None,
            status=None,
            created_at=None,
            platform=None,
            updated_at=None,
    ):
        self.number_of_vulnerabilities = number_of_vulnerabilities
        self.name = name
        self.digest = digest
        self.score = score
        self.id = id
        self.status = status
        self.created_at = created_at
        self.platform = platform
        self.updated_at = updated_at


class ScReport(BaseModel):
    def __init__(
            self,
            id=None,
            image_name=None,
            docker_image_id=None,
            tag=None,
            os=None,
            os_version=None,
            os_architecture=None,
            sha256=None,
            sha1=None,
            md5=None,
            platform=None,
            created_at=None,
            updated_at=None,
            malware=None,
            findings=None,
            installed_packages=None,
            risk_score=None,
            digest=None,
    ):
        self.id = id
        self.image_name = image_name
        self.docker_image_id = docker_image_id
        self.tag = tag
        self.os = os
        self.os_version = os_version
        self.os_architecture = os_architecture
        self.sha256 = sha256
        self.sha1 = sha1
        self.md5 = md5
        self.platform = platform
        self.created_at = created_at
        self.updated_at = updated_at
        self.malware = malware
        self.findings = findings
        self.installed_packages = installed_packages
        self.risk_score = risk_score
        self.digest = digest


class ScTestJob(BaseModel):
    def __init__(
            self,
            container_id=None,
            job_id=None,
            error=None,
            job_status=None,
            created_at=None,
            updated_at=None,
    ):
        self.container_id = container_id
        self.job_id = job_id
        self.error = error
        self.job_status = job_status
        self.created_at = created_at
        self.updated_at = updated_at


class ServerProperties(BaseModel):

    def __init__(
            self,
            capabilities=None,
            enterprise=None,
            expiration=None,
            expiration_time=None,
            idle_timeout=None,
            license=None,
            loaded_plugin_set=None,
            login_banner=None,
            nessus_type=None,
            nessus_ui_version=None,
            notifications=None,
            plugin_set=None,
            scanner_boottime=None,
            server_version=None,
            server_uuid=None,
            update=None,
    ):
        self.capabilities = capabilities
        self.enterprise = enterprise
        self.expiration = expiration
        self.expiration_time = expiration_time
        self.idle_timeout = idle_timeout
        self.license = license
        self.loaded_plugin_set = loaded_plugin_set
        self.login_banner = login_banner
        self.nessus_type = nessus_type
        self.nessus_ui_version = nessus_ui_version
        self.notifications = notifications
        self.plugin_set = plugin_set
        self.scanner_boottime = scanner_boottime
        self.server_version = server_version
        self.server_uuid = server_uuid
        self.update = update


class ServerStatus(BaseModel):

    def __init__(
            self,
            status=None,
            progress=None,
    ):
        self.status = status
        self.progress = progress


class Session(BaseModel):

    def __init__(
            self,
            id=None,
            username=None,
            email=None,
            name=None,
            type=None,
            permissions=None,
            lastlogin=None,
            container_id=None,
            groups=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.type = type
        self.permissions = permissions
        self.lastlogin = lastlogin
        self.container_id = container_id
        self.groups = groups


class TargetGroup(BaseModel):

    def __init__(
        self,
        id=None,
        default_group=None,
        name=None,
        members=None,
        type=None,
        owner=None,
        owner_id=None,
        last_modification_date=None,
        shared=None,
        user_permissions=None,
    ):
        self.id = id
        self.default_group = default_group
        self.name = name
        self.members = members
        self.type = type
        self.owner = owner
        self.owner_id = owner_id
        self.last_modification_date = last_modification_date
        self.shared = shared
        self.user_permissions = user_permissions


class TargetGroupList(BaseModel):

    def __init__(
            self,
            target_groups=None,
    ):
        self._target_groups = None
        self.target_groups = target_groups

    @property
    def target_groups(self):
        return self._target_groups

    @target_groups.setter
    @BaseModel._model_list(TargetGroup)
    def target_groups(self, target_groups):
        self._target_groups = target_groups


class Template(BaseModel):

    def __init__(
            self,
            uuid=None,
            name=None,
            title=None,
            description=None,
            cloud_only=None,
            subscription_only=None,
            is_agent=None,
            more_info=None,
    ):
        self.uuid = uuid
        self.name = name
        self.title = title
        self.description = description
        self.cloud_only = cloud_only
        self.subscription_only = subscription_only
        self.is_agent = is_agent
        self.more_info = more_info


class TemplateList(BaseModel):

    def __init__(
            self,
            templates=None,
    ):
        self._templates = templates

        self.templates = templates

    @property
    def templates(self):
        return self._templates

    @templates.setter
    @BaseModel._model_list(Template)
    def templates(self, templates):
        self._templates = templates


class User(BaseModel):

    def __init__(
            self,
            id=None,
            username=None,
            name=None,
            email=None,
            permissions=None,
            lastlogin=None,
            type=None,
            login_fail_count=None,
            last_login_attempt=None,
    ):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.permissions = permissions
        self.lastlogin = lastlogin
        self.type = type
        self.login_fail_count = login_fail_count
        self.last_login_attempt = last_login_attempt


class UserKeys(BaseModel):

    def __init__(
            self,
            access_key=None,
            secret_key=None,
    ):
        self.access_key = access_key
        self.secret_key = secret_key

    @classmethod
    def from_dict(cls, dict_):
        # Because API uses camelCase for some reason; normalize to underscore here.
        if 'accessKey' in dict_:
            dict_['access_key'] = dict_.pop('accessKey')
        if 'secretKey' in dict_:
            dict_['secret_key'] = dict_.pop('secretKey')
        return super(UserKeys, cls).from_dict(dict_)

    def as_payload(self, filter_=None):
        # Because API uses camelCase for some reason; normalize to underscore here.
        payload = self.as_payload(filter_)
        if 'access_key' in payload:
            payload['accessKey'] = payload.pop('access_key')
        if 'secret_key' in payload:
            payload['secretKey'] = payload.pop('secret_key')
        return payload


class UserList(BaseModel):

    def __init__(
            self,
            users=None,
    ):
        self._users = None
        self.users = users

    @property
    def users(self):
        return self._users

    @users.setter
    @BaseModel._model_list(User)
    def users(self, users):
        self._users = users


class AssetSeverity(BaseModel):

    def __init__(
            self,
            count=None,
            level=None,
            name=None,
    ):
        self.count = count
        self.level = level
        self.name = name


class Asset(BaseModel):

    def __init__(
            self,
            id=None,
            fqdn=None,
            ipv4=None,
            ipv6=None,
            last_seen=None,
            operating_system=None,
            severities=None,
    ):
        self._severities = None

        self.id = id
        self.fqdn = fqdn
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.last_seen = last_seen
        self.operating_system = operating_system
        self.severities = severities

    @property
    def severities(self):
        return self._severities

    @severities.setter
    @BaseModel._model_list(AssetSeverity)
    def severities(self, severities):
        self._severities = severities


class AssetActivity(BaseModel):

    def __init__(
            self,
            type=None,
            timestamp=None,
            scan_id=None,
            schedule_id=None,
            source=None,
            matches=None
    ):
        self.type = type,
        self.timestamp = timestamp,
        self.scan_id = scan_id,
        self.schedule_id = schedule_id,
        self.source = source,
        self.matches = matches


class AssetActivityList(BaseModel):

    def __init__(
            self,
            activity=None,
    ):
        self._activity = None
        self.activity = activity

    @property
    def activity(self):
        return self._activity

    @activity.setter
    @BaseModel._model_list(AssetActivity)
    def activity(self, activity):
        self._activity = activity


class AssetInfo(BaseModel):

    def __init__(
            self,
            counts=None,
            first_seen=None,
            fqdn=None,
            ipv4=None,
            ipv6=None,
            last_authenticated_scan_date=None,
            last_seen=None,
            mac_address=None,
            netbios_name=None,
            operating_system=None,
            system_type=None,
    ):
        self._counts = None

        self.counts = counts
        self.first_seen = first_seen
        self.fqdn = fqdn
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.last_authenticated_scan_date = last_authenticated_scan_date
        self.last_seen = last_seen
        self.mac_address = mac_address
        self.netbios_name = netbios_name
        self.operating_system = operating_system
        self.system_type = system_type

    @property
    def counts(self):
        return self._counts

    @counts.setter
    def counts(self, counts):
        self._counts = counts
        if isinstance(self._counts, dict) \
                and 'vulnerabilities' in self._counts \
                and 'severities' in self._counts['vulnerabilities'] \
                and isinstance(self._counts['vulnerabilities']['severities'], list):
            self._counts['vulnerabilities']['severities'] = \
                AssetSeverity.from_list(self._counts['vulnerabilities']['severities'])


class AssetList(BaseModel):

    def __init__(
            self,
            assets=None,
    ):
        self._assets = None

        self.assets = assets

    @property
    def assets(self):
        return self._assets

    @assets.setter
    @BaseModel._model_list(Asset)
    def assets(self, assets):
        self._assets = assets


class Vulnerability(BaseModel):

    def __init_(
            self,
            count=None,
            plugin_family=None,
            plugin_id=None,
            plugin_name=None,
            vulnerability_state=None,
            severity=None,
    ):
        self.count = count
        self.plugin_family = plugin_family
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.vulnerability_state = vulnerability_state
        self.severity = severity


class VulnerabilityList(BaseModel):

    def __init__(
            self,
            vulnerabilities=None,
    ):
        self._vulnerabilities = None,
        self.vulnerabilities = vulnerabilities

    @property
    def vulnerabilities(self):
        return self._vulnerabilities

    @vulnerabilities.setter
    @BaseModel._model_list(Vulnerability)
    def vulnerabilities(self, vulnerabilities):
        self._vulnerabilities = vulnerabilities


class VulnerabilityOutput(BaseModel):

    def __init__(
            self,
            application_protocol=None,
            assets=None,
            port=None,
            transport_protocol=None,
    ):
        self.application_protocol = application_protocol
        self.assets = assets
        self.port = port
        self.transport_protocol = transport_protocol


class VulnerabilityPluginOutputState(BaseModel):

    def __init__(
            self,
            name=None,
            results=None,
    ):
        self._results = None

        self.name = name
        self.results = results

    @property
    def results(self):
        return self._results

    @results.setter
    @BaseModel._model_list(VulnerabilityOutput)
    def results(self, results):
        self._results = results


class VulnerabilityPluginOutput(BaseModel):

    def __init__(
            self,
            plugin_output=None,
            states=None,
    ):
        self._states = states

        self.plugin_output = plugin_output
        self.states = states

    @property
    def states(self):
        return self._states

    @states.setter
    @BaseModel._model_list(VulnerabilityPluginOutputState)
    def states(self, states):
        self._states = states


class VulnerabilityOutputList(BaseModel):

    def __init__(
            self,
            outputs=None
    ):
        self._outputs = None,

        self.outputs = outputs

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    @BaseModel._model_list(VulnerabilityPluginOutput)
    def outputs(self, outputs):
        self._outputs = outputs
