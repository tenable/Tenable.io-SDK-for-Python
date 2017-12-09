from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AgentExclusion, AgentExclusionList, AgentExclusionSchedule


class AgentExclusionsApi(BaseApi):

    def create(self, agent_exclusion_create, scanner_id=1):
        """Create a new exclusion

        :param agent_exclusion_create: An instance of :class:`AgentExclusionCreateRequest`.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.post('scanners/%(scanner_id)s/agents/exclusions', agent_exclusion_create,
                                     path_params={
                                         'scanner_id': scanner_id
                                     })
        return AgentExclusion.from_json(response.text)

    def delete(self, exclusion_id, scanner_id=1):
        """Delete an exclusion

        :param exclusion_id: The exclusion ID.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/%(scanner_id)s/agents/exclusions/%(exclusion_id)s',
                            path_params={
                                'scanner_id': scanner_id,
                                'exclusion_id': exclusion_id
                            })
        return True

    def details(self, exclusion_id, scanner_id=1):
        """Return details of given exclusion

        :param exclusion_id: The exclusion ID.
        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.get('scanners/%(scanner_id)s/agents/exclusions/%(exclusion_id)s',
                                    path_params={
                                        'scanner_id': scanner_id,
                                        'exclusion_id': exclusion_id
                                    })
        return AgentExclusion.from_json(response.text)

    def edit(self, exclusion_id, agent_exclusion_edit, scanner_id=1):
        """Edit the given exclusion

        :param exclusion_id: The exclusion ID.
        :param scanner_id: The scanner ID.
        :param agent_exclusion_edit: An instance of :class:`AgentExclusionEditRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.put('scanners/%(scanner_id)s/agents/exclusions/%(exclusion_id)s',
                                    agent_exclusion_edit,
                                    path_params={
                                        'scanner_id': scanner_id,
                                        'exclusion_id': exclusion_id
                                    })
        return AgentExclusion.from_json(response.text)

    def list(self, scanner_id=1):
        """Return the current exclusions

        :param scanner_id: The scanner ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusionList`.
        """
        response = self._client.get('scanners/%(scanner_id)s/agents/exclusions',
                                    path_params={
                                        'scanner_id': scanner_id
                                    })
        return AgentExclusionList.from_json(response.text)


class AgentExclusionSaveBaseRequest(BaseRequest):

    def __init__(
            self,
            name,
            description=None,
            schedule=None
    ):
        """Base request for AgentExclusionCreateRequest and AgentExclusionEditRequest.

        :param name: The name of the exclusion.
        :type name: string
        :param description: The description of the exclusion.
        :type description: string
        :param schedule: A time window to limit the exclusion.
        :type schedule: :class:`tenable_io.api.models.AgentExclusionSchedule`
        """
        self.name = name
        self.description = description
        self.schedule = schedule

    def as_payload(self, filter_=None):
        payload = super(AgentExclusionSaveBaseRequest, self).as_payload(True)
        if isinstance(self.schedule, AgentExclusionSchedule):
            payload.__setitem__('schedule', self.schedule.as_payload())
        else:
            payload.pop('schedule', None)
        return payload


class AgentExclusionCreateRequest(AgentExclusionSaveBaseRequest):

    def __init__(
            self,
            name,
            description=None,
            schedule=None
    ):
        """Request for AgentExclusionsApi.create.

        :param name: The name of the exclusion.
        :type name: string
        :param description: The description of the exclusion.
        :type description: string
        :param schedule: A time window to limit the exclusion.
        :type schedule: :class:`tenable_io.api.models.AgentExclusionSchedule`
        """
        super(AgentExclusionCreateRequest, self).__init__(name, description, schedule)


class AgentExclusionEditRequest(AgentExclusionSaveBaseRequest):

    def __init__(
            self,
            name=None,
            description=None,
            schedule=None
    ):
        """Request for AgentExclusionsApi.edit.

        :param name: The name of the exclusion.
        :type name: string
        :param description: The description of the exclusion.
        :type description: string
        :param schedule: A time window to limit the exclusion.
        :type schedule: :class:`tenable_io.api.models.AgentExclusionSchedule`
        """
        super(AgentExclusionEditRequest, self).__init__(name, description, schedule)
