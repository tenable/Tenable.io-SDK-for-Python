=========
CHANGELOG
=========

Unreleased
==========

* Fixed: Added audits, credentials, plugins, and scap into PolicyCreateRequest.
* Changed: WorkbenchParser.parse to log parse error instead of raising an error. Error is usually due to server sending
malformed XML instead of an actual erroneous condition.
* Added: Support of Container Security Containers API.
* Added: Support of Container Security Test Jobs API.
