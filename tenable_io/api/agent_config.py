from tenable_io.api.base import BaseApi, BaseRequest
from tenable_io.api.models import AgentConfig


class AgentConfigApi(BaseApi):

    def edit(self, agent_config):
        """Edit an agent config.

        :param agent_config: The agent config request.
        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentConfig`.
        """
        assert isinstance(agent_config, AgentConfigRequest)
        response = self._client.put('scanners/1/agents/config', agent_config)
        return AgentConfig.from_json(response.text)

    def details(self):
        """Get details of an agent config.

        :raise TenableIOApiException: When API error is encountered.
        :return: An instance of :class:`tenable_io.api.models.AgentConfig`.
        """
        response = self._client.get('scanners/1/agents/config')
        return AgentConfig.from_json(response.text)


class AgentConfigRequest(BaseRequest):

    def __init__(
            self,
            software_update=None,
            auto_unlink=None
    ):
        """Request for AgentConfigApi.edit.

        :param software_update: If True, software updates are enabled for agents pursuant to any agent exclusions that
            are in effect. If False, software updates are disabled for all agents, even if no agent exclusions are in
            effect.
        :type software_update: bool
        :param auto_unlink.enabled: If True, agent auto-unlink is enabled. Enabling auto-unlink causes it to take
            effect against all agents retroactively. This configuration value is only available if Agent Enhancements
            are enabled for your account.
        :type auto_unlink.enabled: bool
        :param auto_unlink.expiration: The expiration time for agents, in days. If an agent has not communicated in this
            number of days, it will be considered 'expired' and auto-unlinked if auto_unlink.enabled is True. Valid
            values are 1-365. This configuration value is only available if Agent Enhancements are enabled for your
            account.
        :type auto_unlink.expiration: int
        """
        self.software_update = software_update
        self.auto_unlink = auto_unlink
