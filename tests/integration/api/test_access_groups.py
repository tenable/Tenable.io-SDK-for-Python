import pytest

from tenable_io.api.access_groups import AccessGroupRequest
from tenable_io.api.models import AccessGroup, AccessGroupList, AssetRule, AssetRuleFilter, Filters
from tests.base import BaseTest


class TestAccessGroupsApi(BaseTest):

    @pytest.fixture(scope='class')
    def access_group(self, app, client):
        asset_rule = AssetRule(
            type='ipv4',
            operator='eq',
            terms=['172.11.13.14']
        )
        access_group = client.access_groups_api.create(AccessGroupRequest(
            name=app.session_name('test_access_group'),
            rules=[asset_rule]
        ))
        yield access_group
        assert client.access_groups_api.delete(access_group.id), u'Access group was not deleted.'

    def test_filters_get(self, client):
        filters = client.access_groups_api.filters()
        assert isinstance(filters, Filters), u'The `filters` method returned invalid filter type.'
        rule_filters = client.access_groups_api.rule_filters()
        for rf in rule_filters:
            assert isinstance(rf, AssetRuleFilter), u'The `rule_filters` method returned invalid rule filter type.'

    def test_list(self, client, access_group):
        access_group_list = client.access_groups_api.list()
        assert isinstance(access_group_list, AccessGroupList), u'Invalid `AccessGroupList` class type.'
        for ag in access_group_list.access_groups:
            assert isinstance(ag, AccessGroup), u'Invalid access group list\'s element type.'
        assert len([ag for ag in access_group_list.access_groups if ag.id == access_group.id]) == 1, \
            u'Access group list does not contain created access group.'

    def test_create_delete(self, app, client):
        access_group = client.access_groups_api.create(AccessGroupRequest(
            name=app.session_name('test_create_delete'),
            rules=[AssetRule(
                type='ipv4',
                operator='eq',
                terms=['10.0.0.14']
            )]
        ))
        assert isinstance(access_group, AccessGroup), u'The `create` method return invalid type.'
        assert hasattr(access_group, 'id'), u'Access group has no ID.'
        assert hasattr(access_group, 'status'), u'Access group has no status.'
        assert client.access_groups_api.delete(access_group.id), u'Access group was not deleted.'

    def test_get_details(self, access_group, client):
        got_access_group = client.access_groups_api.details(access_group.id)
        assert got_access_group.id == access_group.id, u'The `details` method returns access group with different ID.'

    def test_edit(self, app, client, access_group):
        previous_name = access_group.name
        new_name = app.session_name('test_edit')

        edited_access_group = client.access_groups_api.edit(access_group.id, AccessGroupRequest(
            name=new_name,
            rules=[AssetRule(
                type='ipv4',
                operator='eq',
                terms=['10.0.0.20']
            )]
        ))
        assert edited_access_group.name == new_name, u'The `edit` method returns access group with different name.'

        got_access_group = client.access_groups_api.details(edited_access_group.id)
        assert got_access_group.name == new_name, u'The `details` method returns access group with different name.'
