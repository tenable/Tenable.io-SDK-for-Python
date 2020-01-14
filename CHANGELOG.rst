=========
CHANGELOG
=========

1.13.0
==========
* Added: Support for Bulk ACR updates and added Lumin related attributes to Asset objects.

1.12.0
==========
* Added: Support for Networks API
* Added: Support for missing Asset management endpoints.

1.11.0
==========
* Added: Support for Managed Credentials API
* Added: Support for missing Editor API endpoints.

1.10.1
==========
* Fixed: missing ScanRef id attribute when initializing a ScanRef via the id method.

1.10.0
==========
* Changed: Scans API and Scan Helper methods will now accept schedule_uuid as a param to improve lookup performance.
* Fixed: Missing support for agent_group_id in Agent Scan configuration.
* Added: Support for tag_targets in Scan configuration.

1.9.1
==========
* Fixed: Scan exports for WAS scans caused 404s due to missing param

1.9.0
==========
* Added: Support for user authorizations endpoints

1.8.0
==========
* Added: Support for creating dynamic tags
* Changed: Overhaul of all tests for reliability & speed improvements. pytest-vcr and pytest-xdist are now test dependencies.

1.7.0
==========
* Added: Support for all scan export chapters
* Added: Last Modification Date parameter to scan list method
* Added: Import endpoint to exclusions API

1.6.0
==========

* Added: Support for new export API filters
* Added: Support for assets lists in scan settings

1.5.0
==========

* Added: Support for reading vulns and asset exports into memory
* Added: Support for graceful back-off
* Added: Support for tagging API
* Added: Support for access groups API

1.4.1
==========

* Added: SDK version details to User-Agent header.
* Fixed: TenableIOClient config issue in python 3.7.

1.4.0
==========

* Added: Support for retrieving additional plugin families.

1.3.0
==========

* Added: Support for explicit proxy configuration.
* Added: Support for vulns exports API.
* Added: Export helper to download vulnerabilities.
* Added: Support for assets exports API.
* Added: Export helper to download assets.

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
