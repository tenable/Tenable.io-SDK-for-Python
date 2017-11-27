from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AgentExclusion, AgentExclusionList, AgentExclusionSchedule


class AgentExclusionsApi(BaseApi):

    def create(self, agent_exclusion_create):
        """Create a new exclusion

        :param agent_exclusion_create: An instance of :class:`AgentExclusionCreateRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.post('scanners/1/agents/exclusions', agent_exclusion_create)
        return AgentExclusion.from_json(response.text)

    def delete(self, exclusion_id):
        """Delete an exclusion

        :param exclusion_id: The exclusion ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('scanners/1/agents/exclusions/%(exclusion_id)s',
                            path_params={'exclusion_id': exclusion_id})
        return True

    def details(self, exclusion_id):
        """Return details of given exclusion

        :param exclusion_id: The exclusion ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.get('scanners/1/agents/exclusions/%(exclusion_id)s',
                                    path_params={'exclusion_id': exclusion_id})
        return AgentExclusion.from_json(response.text)

    def edit(self, exclusion_id, agent_exclusion_edit):
        """Edit the given exclusion

        :param exclusion_id: The exclusion ID.
        :param agent_exclusion_edit: An instance of :class:`AgentExclusionEditRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusion`.
        """
        response = self._client.put('scanners/1/agents/exclusions/%(exclusion_id)s',
                                    agent_exclusion_edit,
                                    path_params={'exclusion_id': exclusion_id})
        return AgentExclusion.from_json(response.text)

    def list(self):
        """Return the current exclusions

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentExclusionList`.
        """
        response = self._client.get('scanners/1/agents/exclusions')
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
