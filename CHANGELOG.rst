=========
CHANGELOG
=========

Unreleased
==========

* Added: Support for Filters API.
* Added: Support for sort, f, ft, w, and wf parameters on agent list API.
* Changed: Model AgentList.pagination is now an instance of model FilterPagination.
* Removed: Model Agent.token.

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
