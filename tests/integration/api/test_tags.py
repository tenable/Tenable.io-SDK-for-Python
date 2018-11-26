import pytest

from tenable_io.api.models import AssetTagAssignment, AssetTagAssignmentList, TagCategory, TagCategoryList, TagValue, \
    TagValueList
from tenable_io.api.tags import AssetAssignmentsRequest, TagCategoryRequest, TagValueRequest
from tests.base import BaseTest


class TestTagsApi(BaseTest):

    @pytest.fixture(scope='class')
    def tag_category(self, app, client):
        category = client.tags_api.create_category(TagCategoryRequest(
            name=app.session_name('test_category')
        ))
        yield category
        assert client.tags_api.delete_category(category.uuid), u'Unabled to delete category.'

    @pytest.fixture()
    def tag_value(self, app, client):
        value = client.tags_api.create_value(TagValueRequest(
            category_name=app.session_name('test_category_name'),
            value=app.session_name('test_value')
        ))
        yield value
        assert client.tags_api.delete_category(value.category_uuid), u'Unabled to delete category.'

    def test_create_delete_category(self, app, client):
        category = client.tags_api.create_category(TagCategoryRequest(
            name=app.session_name('test_create_delete'),
            description='A sample tag category description.'
        ))
        assert hasattr(category, 'uuid'), u'Tag category has no uuID.'
        assert hasattr(category, 'name') and category.name, u'Tag category has empty name field.'
        assert hasattr(category, 'description') and category.description, u'Tag category has empty description field.'
        assert client.tags_api.delete_category(category.uuid), u'Tag category was not deleted.'

    def test_category_get(self, tag_category, client):
        got_category = client.tags_api.category(tag_category.uuid)
        assert got_category.uuid == tag_category.uuid, \
            u'The `category` method returns tag category with different uuid.'

    def test_category_edit(self, app, client, tag_category):
        previous_name = tag_category.name
        new_name = app.session_name('test_category_edit')

        edited_category = client.tags_api.edit_category(tag_category.uuid, TagCategoryRequest(
            name=new_name
        ))
        assert edited_category.name == new_name, \
            u'The `edit_category` method returns category with different name field.'

        reverted_category = client.tags_api.edit_category(tag_category.uuid, TagCategoryRequest(
            name=previous_name
        ))
        assert reverted_category.name == previous_name, u'The reverted category has different name.'

    def test_category_list(self, client, tag_category):
        category_list = client.tags_api.categories()
        assert isinstance(category_list, TagCategoryList), u'The `categories` method return type.'

        for cat in category_list.categories:
            assert isinstance(cat, TagCategory), u'Tag category list item type.'
        assert len([cat for cat in category_list.categories if cat.uuid == tag_category.uuid]) == 1, \
            u'Tag category list contains created category.'

    def test_create_delete_value(self, app, client):
        value = client.tags_api.create_value(TagValueRequest(
            category_name=app.session_name('test_category_name'),
            value=app.session_name('test_create_delete'),
            description='Sample value description',
        ))
        assert isinstance(value, TagValue), u'The `create_value` method return type.'
        assert hasattr(value, 'uuid'), u'Tag value has no uuID.'
        assert hasattr(value, 'category_name') and value.category_name, u'Tag value has empty category_name field.'
        assert hasattr(value, 'value') and value.value, u'Tag value has empty value field.'
        assert hasattr(value, 'description') and value.description, u'Tag value has empty description field.'
        assert client.tags_api.delete_value(value.uuid), u'Tag value was not deleted.'

    def test_value_get(self, tag_value, client):
        got_value = client.tags_api.value(tag_value.uuid)
        assert got_value.uuid == tag_value.uuid, u'The `value` method returns tag value with different uuid.'

    def test_value_edit(self, app, client, tag_value):
        previous_value = tag_value.value
        new_value = app.session_name('test_value_edit')

        edited_value = client.tags_api.edit_value(tag_value.uuid, TagValueRequest(
            value=new_value
        ))
        assert edited_value.value == new_value, u'The `edit_value` method returns value with different value field.'

        reverted_value = client.tags_api.edit_value(tag_value.uuid, TagValueRequest(
            value=previous_value
        ))
        assert reverted_value.value == previous_value, u'The reverted value has different value field.'

    def test_value_list(self, client, tag_value):
        value_list = client.tags_api.values()
        assert isinstance(value_list, TagValueList), u'The `values` method return type.'

        for val in value_list.values:
            assert isinstance(val, TagValue), u'Tag value list item type.'
        assert len([val for val in value_list.values if val.uuid == tag_value.uuid]) == 1, \
            u'Tag value list contains created value.'

    def test_value_bulk_delete(self, app, client, tag_value):
        value_list = client.tags_api.category_values(tag_value.category_uuid).values
        assert len(value_list) == 1 and value_list[0].value is not None, \
            u'Category contains more than 1 value or no values.'
        value_2 = client.tags_api.create_value(TagValueRequest(
            category_uuid=tag_value.category_uuid,
            value=app.session_name('test_bulk_delete2')
        ))
        assert isinstance(value_2, TagValue), u'Tag value_2 type.'
        value_list = client.tags_api.category_values(tag_value.category_uuid).values
        assert len(value_list) == 2, u'The second value was not created.'
        assert len([v for v in value_list if v.value is None]) == 0, \
            u'The category contains an empty value entry'
        assert client.tags_api.value_delete_requests([v.uuid for v in value_list]), \
            u'The `value_delete_requests` did not succeed.'
        value_list = client.tags_api.category_values(tag_value.category_uuid).values
        assert len(value_list) == 1 and value_list[0].value is None, \
            u'Values were not removed.'

    def test_category_values(self, client, tag_value):
        category_values = client.tags_api.category_values(tag_value.category_uuid)
        assert isinstance(category_values, TagValueList), u'The `category_values` method return type.'
        assert len([val for val in category_values.values if val.uuid == tag_value.uuid]) == 1, \
            u'Tag category values contains created value.'

        category_value = client.tags_api.category_value(tag_value.category_uuid, tag_value.uuid)
        assert isinstance(category_value, TagValue), u'The `category_value` method return type.'
        assert category_value.uuid == tag_value.uuid, u'The retreive category value does not match created value uuid.'

    def test_asset_tag_assignments_count(self, app, client, tag_value):
        asset = client.assets_api.list().assets[0]
        asset_assignments = client.tags_api.asset_tag_assignments(asset.id)
        assert isinstance(asset_assignments, AssetTagAssignmentList), u'The `asset_tag_assignments` method return type.'
        assert len([val for val in asset_assignments.tags if val.value_uuid == tag_value.uuid]) == 0, \
            u'Asset assignment list already contains value.'
        assert client.tags_api.edit_asset_tag_assignments(AssetAssignmentsRequest(
            action='add',
            assets=[asset.id],
            tags=[tag_value.uuid]
        ))
        asset_assignments = client.tags_api.asset_tag_assignments(asset.id)
        for a in asset_assignments.tags:
            assert isinstance(a, AssetTagAssignment), u'The asset assignments element type.'
        assert len([val for val in asset_assignments.tags if val.value_uuid == tag_value.uuid]) == 1, \
            u'Asset assignments does not contain added value.'
        assert client.tags_api.category_counts(tag_value.category_uuid) == 1, \
            u'The `category_counts` method return count.'
        assert client.tags_api.value_counts(tag_value.uuid) == 1, \
            u'The `value_counts` method return count.'
