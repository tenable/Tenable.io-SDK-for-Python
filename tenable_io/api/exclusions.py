from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import Exclusion, ExclusionList, ExclusionSchedule


class ExclusionApi(BaseApi):

    def create(self, exclusion_create):
        """Create a new exclusion

        :param exclusion_create: An instance of :class:`ExclusionCreateRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Exclusion`.
        """
        response = self._client.post('exclusions', exclusion_create)
        return Exclusion.from_json(response.text)

    def delete(self, list_id):
        """Delete an exclusion

        :param list_id: The exclusion ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: True if successful.
        """
        self._client.delete('exclusions/%(list_id)s', path_params={'list_id': list_id})
        return True

    def details(self, list_id):
        """Return details of given exclusion

        :param list_id: The exclusion ID.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Exclusion`.
        """
        response = self._client.get('exclusions/%(list_id)s', path_params={'list_id': list_id})
        return Exclusion.from_json(response.text)

    def edit(self, list_id, exclusion_edit):
        """Edit the given exclusion

        :param list_id: The exclusion ID.
        :param exclusion_edit: An instance of :class:`ExclusionEditRequest`.
        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.Exclusion`.
        """
        response = self._client.put('exclusions/%(list_id)s', exclusion_edit, path_params={'list_id': list_id})
        return Exclusion.from_json(response.text)

    def list(self):
        """Return the current exclusions

        :raise TenableIOApiException:  When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.ExclusionList`.
        """
        response = self._client.get('exclusions')
        return ExclusionList.from_json(response.text)


class ExclusionSaveBaseRequest(BaseRequest):

    def __init__(
            self,
            name,
            members=None,
            description=None,
            schedule=None
    ):
        self.name = name
        self.members = members
        self.description = description
        self.schedule = schedule

    def as_payload(self, filter_=None):
        payload = super(ExclusionSaveBaseRequest, self).as_payload(True)
        if isinstance(self.schedule, ExclusionSchedule):
            payload.__setitem__('schedule', self.schedule.as_payload())
        else:
            payload.pop('schedule', None)
        return payload


class ExclusionCreateRequest(ExclusionSaveBaseRequest):

    def __init__(
            self,
            name,
            members,
            description=None,
            schedule=None
    ):
        super(ExclusionCreateRequest, self).__init__(name, members, description, schedule)


class ExclusionEditRequest(ExclusionSaveBaseRequest):

    def __init__(
            self,
            name=None,
            members=None,
            description=None,
            schedule=None
    ):
        super(ExclusionEditRequest, self).__init__(name, members, description, schedule)
