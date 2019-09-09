import pytest

from random import randint

from tenable_io.api.models import AssetTagAssignment, AssetTagAssignmentList, TagCategory, TagCategoryList, TagValue, \
    TagValueList
from tenable_io.api.tags import AssetAssignmentsRequest, TagCategoryRequest, TagValueRequest


# def create_category(client):
#     return client.tags_api.create_category(TagCategoryRequest(
#         name='test_category_{}'.format(randint(0, 1000))
#     ))


def create_value(client, category_name):
    return client.tags_api.create_value(TagValueRequest(
        category_name=category_name,
        value='test_value_{}'.format(randint(0, 1000))
    ))


@pytest.mark.vcr()
def test_tags_category_create(new_tag_category):
    assert isinstance(new_tag_category, TagCategory), u'The `create_category` method did not return type `TagCategory`.'


@pytest.mark.vcr()
def test_tags_categories(client):
    category_list = client.tags_api.categories()
    assert isinstance(category_list, TagCategoryList), u'The `categories` method did not return type `TagCategoryList`.'

    for category in category_list.categories:
        assert isinstance(category, TagCategory), u'The list should be of type `TagCategory`.'


@pytest.mark.vcr()
def test_tags_category(client, new_tag_category):
    category = new_tag_category
    fetched_category = client.tags_api.category(category.uuid)
    assert fetched_category.uuid == category.uuid, \
        u'The `category` method returns tag category with different uuid.'
    assert isinstance(fetched_category, TagCategory), u'The `category` method did not return type `TagCategory`.'


@pytest.mark.vcr()
def test_tags_category_delete(client, new_tag_category):
    assert client.tags_api.delete_category(new_tag_category.uuid), u'The tag category was not deleted.'


@pytest.mark.vcr()
def test_tags_category_edit(client, new_tag_category):
    edit_name = 'test_category_edit'
    edit_category = client.tags_api.edit_category(new_tag_category.uuid, TagCategoryRequest(
        name=edit_name
    ))
    assert isinstance(edit_category, TagCategory), u'The `edit_category` method did not return type `TagCategory`.'
    assert edit_category.name == edit_name, u'The tag category edit was not successful.'


@pytest.mark.vcr()
def test_tags_category_values(client, new_tag_category):
    category = new_tag_category
    value = create_value(client, category.name)
    category_values = client.tags_api.category_values(category.uuid)
    assert isinstance(category_values, TagValueList), \
        u'The `category_values` method did not return type `TagValueList`.'
    assert len(category_values.values), u'Expected a single value for the category.'
    assert category_values.values[0].value == value.value, u'Expected created value to be returned.'


@pytest.mark.vcr()
def test_tags_category_value(client, new_tag_category):
    category = new_tag_category
    value = create_value(client, category.name)
    category_value = client.tags_api.category_value(category.uuid, value.uuid)
    assert isinstance(category_value, TagValue), \
        u'The `category_value` method did not return type `TagValue`.'
    assert category_value.value == value.value, u'Expected created value to be returned.'


@pytest.mark.vcr()
def test_tags_category_counts(client, new_tag_category):
    counts = client.tags_api.category_counts(new_tag_category.uuid)
    assert counts is None, u'Expected no assignments for the new category.'


@pytest.mark.vcr()
def test_tags_value_create(client, new_tag_category):
    value = create_value(client, new_tag_category.uuid)
    assert isinstance(value, TagValue), u'The `create_value` method did not return type `TagValue`.'


@pytest.mark.vcr()
def test_tags_values(client):
    value_list = client.tags_api.values()
    assert isinstance(value_list, TagValueList), u'The `values` method did not return type `TagValueList`.'

    for value in value_list.values:
        assert isinstance(value, TagValue), u'The list should be of type `TagValue`.'


@pytest.mark.vcr()
def test_tags_value_delete(client, new_tag_category):
    value = create_value(client, new_tag_category.uuid)
    assert client.tags_api.delete_value(value.uuid), u'The tag value was not deleted.'


@pytest.mark.vcr()
def test_tags_value_edit(client, new_tag_category):
    value = create_value(client, new_tag_category.uuid)
    edit_name = 'test_value_edit'
    edit_value = client.tags_api.edit_value(value.uuid, TagValueRequest(
        value=edit_name
    ))
    assert isinstance(edit_value, TagValue), u'The `edit_value` method did not return type `TagValue`.'
    assert edit_value.value == edit_name, u'The tag value edit was not successful.'


@pytest.mark.vcr()
def test_tags_value_counts(client, new_tag_category):
    value = create_value(client, new_tag_category.uuid)
    counts = client.tags_api.value_counts(value.uuid)
    assert counts is None, u'Expected no assignments for the new value.'


@pytest.mark.vcr()
def test_tags_value_bulk_delete(client, new_tag_category):
    category = new_tag_category
    value1 = create_value(client, category.uuid)
    value2 = create_value(client, category.uuid)
    assert client.tags_api.value_delete_requests([value1.uuid, value2.uuid]), u'The tag values were not deleted.'


@pytest.mark.vcr()
def test_tags_asset_tag_assignments(client, new_tag_category):
    value = create_value(client, new_tag_category.uuid)
    asset = client.assets_api.list().assets[0]
    # check assignments
    asset_assignments = client.tags_api.asset_tag_assignments(asset.id)
    assert isinstance(asset_assignments, AssetTagAssignmentList), \
        u'The `asset_tag_assignments` method did not return type `AssetTagAssignmentList`.'
    assert len(asset_assignments.tags) == 0, u'Expected 0 assignments for asset.'
    # assign value to asset
    assignment_request = AssetAssignmentsRequest(
        action='add',
        assets=[asset.id],
        tags=[value.uuid]
    )
    assert client.tags_api.edit_asset_tag_assignments(assignment_request), \
        u'The tag assignment request was not successful.'
    # check assignments again
    asset_assignments = client.tags_api.asset_tag_assignments(asset.id)
    assert isinstance(asset_assignments, AssetTagAssignmentList), \
        u'The `asset_tag_assignments` method did not return type `AssetTagAssignmentList`.'
    assert len(asset_assignments.tags) == 1, u'Expected 1 assignment for asset.'
    for assignment in asset_assignments.tags:
        assert isinstance(assignment, AssetTagAssignment), u'Expected list of type `AssetTagAssignment`.'
