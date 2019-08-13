import pytest

import os

from tenable_io.api.exclusions import ExclusionEditRequest
from tenable_io.api.models import Exclusion, ExclusionList


@pytest.mark.vcr()
def test_exclusions_create(new_exclusion):
    assert isinstance(new_exclusion, Exclusion), u'The `create` method did not return type `Exclusion`.'


@pytest.mark.vcr()
def test_exclusions_details(client, new_exclusion):
    exclusion = client.exclusions_api.details(new_exclusion.id)
    assert isinstance(exclusion, Exclusion), u'The `create` method did not return type `Exclusion`.'


@pytest.mark.vcr()
def test_exclusions_list(client):
    exclusion_list = client.exclusions_api.list()
    assert isinstance(exclusion_list, ExclusionList), u'The `list` method did not return type `ExclusionList`.'

@pytest.mark.vcr()
def test_exclusions_edit(client, new_exclusion):
    exclusion = new_exclusion
    edited_exclusion_name = 'test_exclusion_name_edited'
    edit_request = ExclusionEditRequest(
        edited_exclusion_name,
        exclusion.members
    )
    edited_exclusion = client.exclusions_api.edit(exclusion.id, edit_request)
    assert isinstance(edited_exclusion, Exclusion), u'The `edit` method did not return type `Exclusion`.'
    assert edited_exclusion.name == edited_exclusion_name, u'Expected name to be updated.'

@pytest.mark.vcr()
def test_exclusions_delete(client, new_exclusion):
    assert client.exclusions_api.delete(new_exclusion.id), u'Exclusion was not deleted.'

@pytest.mark.vcr()
def test_exclusions_import(client):
    import_exclusion_name = 'test_exclusion_name_imported'
    path = u'test_exclusions_import'
    with open(path, 'w') as f:
        f.write('id,name,description,members,creation_date,last_modification_date\n3,"{}","11","test.host.com",1562002566,1562002566'.format(import_exclusion_name))
    assert os.path.getsize(path) > 0, u'The exclusion file is not empty.'

    with open(path, 'rb') as fu:
        upload_file_name = client.file_api.upload(fu)
    assert upload_file_name, u'File `upload` method returns valid file name.'

    client.exclusions_api.import_exclusion(upload_file_name)
    exclusion_list = client.exclusions_api.list()
    assert len(exclusion_list.exclusions) > 0, u'Expected exclusions to be returned.'
    exlcusion_names = [ex.name for ex in exclusion_list.exclusions]
    assert import_exclusion_name in exlcusion_names, u'Expected imported exclusion to be returned.'
    os.remove(path)


