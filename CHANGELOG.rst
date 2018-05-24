=========
CHANGELOG
=========

1.2.1
==========

* Changed: Scan helper methods now use /latest-status when checking scan status.

1.2.0
==========

* Added: Route to get a scan's latest status (/latest-status).
* Added: X-Tio-Retry-Count header sent with each retry.
* Changed: Replace urllib3.Retry with custom retry logic in TenableIOClient.
* Fixed: Recursion error in ScanInfo model.

1.1.1
==========

* Fixed: Retries were broken for python 2.7 users.

1.1.0
==========

* Added: 500 added to retryable error codes.
* Added: Permissions Helper added for more detailed permissions support.
* Changed: ScanSettings model updated with acl.
* Added: Model TargetGroup.acls
* Added: Model ScanSetting properties: starttime, rrules, timezone, file_targets, and launch_now

1.0.0
==========

* Added: Support for agent-exclusions API.
* Added: Support for agent-config API.
* Added: Support for bulk-operations API.
* Added: Model AgentGroup properties: agents, agents_count, pagination, and timestamp.
* Added: Support for sort, f, ft, w, and wf parameters on agent-group details and agent-group agents API.
* Added: Support for Filters API.
* Added: Support for sort, f, ft, w, and wf parameters on agent list API.
* Changed: Model AgentList.pagination is now an instance of model FilterPagination.
* Removed: Model Agent.token.
* Added: Support for assets API.
* Added: Support for import API.
* Changed: Support for scanner_id parameter for agents, agent-config, agent-exclusions, agent-groups, and bulk-operations API.
* Fixed: Scan Helpers last_history function.

0.4.0
=====

* Added: Support for offset and limit on endpoints returning an agent list.

0.3.0
=====

* Added: Support for include_aggregate parameter for ScansApi.import_scan.
* Added: Support for scans host-details API.
* Changed: Model ScanDetails.hosts is now a list of ScanHost's instead of dict's.

0.2.0
=====

* Fixed: Added audits, credentials, plugins, and scap into PolicyCreateRequest.
* Changed: WorkbenchParser.parse to log parse error instead of raising an error. Error is usually due to server sending
malformed XML instead of an actual erroneous condition.
* Added: Support of Container Security Containers API.
* Added: Support of Container Security Test Jobs API.
* Added: Support of Container Security Reports API.
* Added: Support of Container Security Policy API.
