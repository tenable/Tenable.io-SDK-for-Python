import pytest

from datetime import datetime, timedelta
from random import randint
from six import StringIO

from tenable_io.api.agent_groups import AgentGroupSaveRequest
from tenable_io.api.exclusions import ExclusionCreateRequest
from tenable_io.api.import_ import ImportAssetsRequest
from tenable_io.api.models import ExclusionSchedule, ExclusionRrules, ImportAsset, PolicySettings, ScanSettings
from tenable_io.api.policies import PolicyCreateRequest
from tenable_io.api.scans import ScanCreateRequest
from tenable_io.api.tags import TagCategoryRequest
from tenable_io.api.target_groups import TargetGroupCreateRequest
from tests.config import TenableIOTestConfig


@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
            ('Authorization', 'Auth fffffffffffffffffffffffffffffffffffffffffffffffffff')
        ]
    }


@pytest.fixture
def new_agent_group(client):
    return client.agent_groups_api.create(
        AgentGroupSaveRequest(
            'test_agent_group_name_{}'.format(randint(0, 10000))
        )
    )


def schedule_once():
    rrules = ExclusionRrules(
        "ONETIME",
        1
    )
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(hours=1)

    return ExclusionSchedule(
        True,
        start_time.strftime('%Y-%m-%d %H:%m:%S'),
        end_time.strftime('%Y-%m-%d %H:%m:%S'),
        'UTC',
        rrules
    )

@pytest.fixture
def new_exclusion(client):
    return client.exclusions_api.create(
        ExclusionCreateRequest(
            'test_exclusion_name{}'.format(randint(0, 10000)),
            u'fake.tenable.com,fake2.tenable.com',
            u'test description',
            schedule_once()
        )
    )

@pytest.fixture
def fetch_agent(client):
    agent_list = client.agents_api.list()
    return agent_list.agents[0].id if len(agent_list.agents) > 0 else None


@pytest.fixture
def fetch_file():
    file = StringIO('test content')
    setattr(file, 'name', 'test_file')
    return file


@pytest.fixture
def new_folder(client):
    return client.folders_api.create('test_folders_{}'.format(randint(0, 10000)))


@pytest.fixture
def new_group(client):
    return client.groups_api.create('test_groups_{}'.format(randint(0, 10000)))


@pytest.fixture
def import_asset(client):
    import_asset = ImportAsset(ipv4=['1.1.1.1'], fqdn=['my.test.asset'])
    import_request = ImportAssetsRequest(
        assets=[import_asset],
        source='TEST'
    )
    return client.import_api.assets(import_request)


@pytest.fixture
def new_policy(client):
    template_list = client.editor_api.list('policy')
    assert len(template_list.templates) > 0, u'Expected at least one policy template.'

    test_templates = [t for t in template_list.templates if t.name == 'basic']
    return client.policies_api.create(
        PolicyCreateRequest(
            test_templates[0].uuid,
            PolicySettings(
                name='test_policy_{}'.format(randint(0, 10000)),
                description='test_policies'
            )
        )
    )


@pytest.fixture
def fetch_container(client):
    containers = client.sc_containers_api.list()
    return containers[0]


@pytest.fixture
def fetch_scanner(client):
    scanner_list = client.scanners_api.list()
    assert len(scanner_list.scanners) > 0, u'At least one scanner.'

    test_scanner = scanner_list.scanners[0]

    for scanner in scanner_list.scanners:
        if scanner.name == 'US Cloud Scanner':
            test_scanner = scanner

    return test_scanner


@pytest.fixture
def new_scan(client):
    template_list = client.editor_api.list('scan')
    assert len(template_list.templates) > 0, u'Expected at least one scan template.'

    test_templates = [t for t in template_list.templates if t.name == 'basic']
    return client.scans_api.create(
        ScanCreateRequest(
            test_templates[0].uuid,
            ScanSettings(
                'test_scan_fixture',
                TenableIOTestConfig.get('scan_text_targets'),
            )
        ),
        return_uuid=True
    )

@pytest.fixture
def new_scan_id(client):
    template_list = client.editor_api.list('scan')
    assert len(template_list.templates) > 0, u'Expected at least one scan template.'

    test_templates = [t for t in template_list.templates if t.name == 'basic']
    return client.scans_api.create(
        ScanCreateRequest(
            test_templates[0].uuid,
            ScanSettings(
                'test_scan_fixture',
                TenableIOTestConfig.get('scan_text_targets'),
            )
        )
    )


@pytest.fixture
def new_tag_category(client):
    return client.tags_api.create_category(TagCategoryRequest(
        name='test_category_{}'.format(randint(0, 10000))
    ))


@pytest.fixture
def new_target_group(client):
    return client.target_groups_api.create(TargetGroupCreateRequest(
        name='test_target_group_{}'.format(randint(0, 10000)),
        members='tenable.com',
        type='system',
        acls=[{"permissions": 0, "type": "default"}]
    ))


@pytest.fixture
def fetch_asset(client):
    assets_list = client.workbenches_api.assets()
    return assets_list.assets[0]


@pytest.fixture
def fetch_vulnerability(client):
    vulnerabilities_list = client.workbenches_api.vulnerabilities(date_range=30)
    return vulnerabilities_list.vulnerabilities[0]