import pytest

from random import randint
from tenable_io.api.access_groups import AccessGroupRequest
from tenable_io.api.models import AccessGroup, AccessGroupList, AssetRule, AssetRuleFilter, Filters

@pytest.mark.vcr()
def test_access_groups_filters_get(client):
    filters = client.access_groups_api.filters()
    print(filters)
    assert isinstance(filters, Filters), u'The `filters` method did not return type `Filters`.'

@pytest.mark.vcr()
def test_access_groups_rule_filters_get(client):
    rule_filters = client.access_groups_api.rule_filters()
    print(rule_filters)
    for rf in rule_filters:
        assert isinstance(rf, AssetRuleFilter), u'The `rule_filters` method did not return type `AssetRuleFilter`.'

@pytest.mark.vcr()
def test_access_groups_list(client):
    access_group_list = client.access_groups_api.list()
    assert isinstance(access_group_list, AccessGroupList), u'The `list` method did not return type `AccessGroupList`.'
    for ag in access_group_list.access_groups:
        assert isinstance(ag, AccessGroup), u'Invalid access group list\'s element type.'

@pytest.mark.vcr()
def test_access_groups_get_details(client):
        new_group = create_access_group(client)
        got_access_group = client.access_groups_api.details(new_group.id)
        assert got_access_group.id == new_group.id, u'The `details` method returns access group with different ID.'

@pytest.mark.vcr()
def test_access_groups_delete(client):
    access_group = client.access_groups_api.create(AccessGroupRequest(
        name='test_create_delete',
        rules=[AssetRule(
            type='ipv4',
            operator='eq',
            terms=['10.0.0.14']
        )]
    ))
    assert isinstance(access_group, AccessGroup), u'The `create` method did not return type `AccessGroup`.'
    assert client.access_groups_api.delete(access_group.id), u'Access group was not deleted.'

@pytest.mark.vcr()
def test_access_groups_edit(client):
    existing_group = create_access_group(client)
    new_name = 'test_edit'

    edited_access_group = client.access_groups_api.edit(existing_group.id, AccessGroupRequest(
        name=new_name,
        rules=[AssetRule(
            type='ipv4',
            operator='eq',
            terms=['10.0.0.20']
        )]
    ))
    assert isinstance(edited_access_group, AccessGroup), u'The `edit` method did not return type `AccessGroup`.'
    assert edited_access_group.name != existing_group.name, u'The `edit` method did not change the group name.'

    got_access_group = client.access_groups_api.details(edited_access_group.id)
    assert got_access_group.name == new_name, u'The `details` method returns access group with different name.'

def create_access_group(client):
    asset_rule = AssetRule(
        type='ipv4',
        operator='eq',
        terms=['172.11.13.14']
    )
    return client.access_groups_api.create(AccessGroupRequest(
        name='test_access_group_name{}'.format(randint(0, 100)),
        rules=[asset_rule]
    ))
