from dataclasses import dataclass
import os
from typing import Any, Dict, Generator, List, Optional, Tuple
from unittest.mock import patch
import uuid

import pytest
from requests.exceptions import RequestException

from anyscale.client.openapi_client.models import (
    ArchiveStatus,
    CloudDataBucketFileType,
    CloudDataBucketPresignedUploadInfo,
    CloudDataBucketPresignedUploadRequest,
    ComputeTemplateConfig,
    ComputeTemplateQuery,
    CreateComputeTemplate,
    DecoratedComputeTemplate,
    DecoratedcomputetemplateListResponse,
)
from anyscale.sdk.anyscale_client.configuration import Configuration
from anyscale.sdk.anyscale_client.models import (
    Cloud,
    Cluster,
    ClusterCompute,
    ClusterComputeConfig,
    ClusterEnvironment,
    ClusterEnvironmentBuild,
    ComputeTemplate,
    ListResponseMetadata,
    Project,
    ServiceModel,
    ServicemodelListResponse,
)
from anyscale.sdk.anyscale_client.rest import ApiException
from anyscale.service._private.anyscale_client import (
    DEFAULT_PYTHON_VERSION,
    DEFAULT_RAY_VERSION,
    RealAnyscaleClient,
)
from anyscale.utils.workspace_notification import (
    WORKSPACE_NOTIFICATION_ADDRESS,
    WorkspaceNotification,
    WorkspaceNotificationAction,
)


def _get_test_file_path(subpath: str) -> str:
    return os.path.join(os.path.dirname(__file__), subpath)


BASIC_WORKING_DIR = _get_test_file_path("test_working_dirs/basic")
NESTED_WORKING_DIR = _get_test_file_path("test_working_dirs/nested")
SYMLINK_WORKING_DIR = _get_test_file_path("test_working_dirs/symlink_to_basic")
TEST_WORKING_DIRS = [BASIC_WORKING_DIR, NESTED_WORKING_DIR, SYMLINK_WORKING_DIR]

TEST_WORKSPACE_REQUIREMENTS_FILE_PATH = _get_test_file_path(
    "test_requirements_files/test_workspace_requirements.txt"
)

FAKE_WORKSPACE_NOTIFICATION = WorkspaceNotification(
    body="Hello world!",
    action=WorkspaceNotificationAction(
        type="navigate-service", title="fake-title", value="fake-value",
    ),
)

OPENAPI_NO_VALIDATION = Configuration()
OPENAPI_NO_VALIDATION.client_side_validation = False


class FakeServiceController:
    pass


@dataclass
class FakeClientResult:
    result: Any


class FakeExternalAPIClient:
    """Fake implementation of the "external" Anyscale REST API.

    Should mimic the behavior and return values of the client defined at:
    `anyscale.sdk.anyscale_client`.
    """

    DEFAULT_CLOUD_ID = "fake-default-cloud-id"
    DEFAULT_PROJECT_ID = "fake-default-project-id"
    DEFAULT_CLUSTER_COMPUTE_ID = "fake-default-cluster-compute-id"
    DEFAULT_CLUSTER_ENV_BUILD_ID = "fake-default-cluster-env-build-id"

    WORKSPACE_CLOUD_ID = "fake-workspace-cloud-id"
    WORKSPACE_CLUSTER_ID = "fake-workspace-cluster-id"
    WORKSPACE_PROJECT_ID = "fake-workspace-project-id"
    WORKSPACE_CLUSTER_COMPUTE_ID = "fake-workspace-cluster-compute-id"
    WORKSPACE_CLUSTER_ENV_BUILD_ID = "fake-workspace-cluster-env-build-id"

    def __init__(self):
        self._num_get_cloud_calls: int = 0
        self._num_get_project_calls: int = 0
        self._num_get_cluster_calls: int = 0
        self._num_get_cluster_compute_calls: int = 0

        # Cluster environment ID to name.
        self._cluster_env_names: Dict[str, str] = {}
        # Cluster environment build ID to (cluster environment ID, revision).
        self._cluster_env_builds: Dict[str, Tuple[str, int]] = {}

        # Cluster compute ID to name. Populate workspace mapping by default.
        self._cluster_computes: Dict[str, ClusterCompute] = {
            self.WORKSPACE_CLUSTER_COMPUTE_ID: ClusterCompute(
                id=self.WORKSPACE_CLUSTER_COMPUTE_ID,
                config=ClusterComputeConfig(
                    cloud_id=self.WORKSPACE_CLOUD_ID,
                    local_vars_configuration=OPENAPI_NO_VALIDATION,
                ),
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        }

        # Used to emulate multi-page list endpoint behavior.
        self._services_list: List[ServiceModel] = []
        self._next_services_list_paging_token: Optional[str] = None

    @property
    def num_get_cloud_calls(self) -> int:
        return self._num_get_cloud_calls

    def get_default_cloud(self) -> FakeClientResult:
        self._num_get_cloud_calls += 1
        return FakeClientResult(
            result=Cloud(
                id=self.DEFAULT_CLOUD_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    @property
    def num_get_project_calls(self) -> int:
        return self._num_get_project_calls

    def get_default_project(self) -> FakeClientResult:
        self._num_get_project_calls += 1
        return FakeClientResult(
            result=Project(
                id=self.DEFAULT_PROJECT_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    def get_default_cluster_compute(self) -> FakeClientResult:
        return FakeClientResult(
            result=ComputeTemplate(
                id=self.DEFAULT_CLUSTER_COMPUTE_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    def get_default_cluster_environment_build(
        self, python_version: str, ray_version: str
    ) -> FakeClientResult:
        assert ray_version == DEFAULT_RAY_VERSION
        assert python_version == DEFAULT_PYTHON_VERSION

        return FakeClientResult(
            result=ClusterEnvironmentBuild(
                id=self.DEFAULT_CLUSTER_ENV_BUILD_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    @property
    def num_get_cluster_calls(self) -> int:
        return self._num_get_cluster_calls

    def get_cluster(self, cluster_id: str) -> FakeClientResult:
        self._num_get_cluster_calls += 1
        assert (
            cluster_id == self.WORKSPACE_CLUSTER_ID
        ), "`get_cluster` should only be used to get the workspace cluster."
        return FakeClientResult(
            result=Cluster(
                id=self.WORKSPACE_CLUSTER_ID,
                project_id=self.WORKSPACE_PROJECT_ID,
                cluster_compute_id=self.WORKSPACE_CLUSTER_COMPUTE_ID,
                cluster_environment_build_id=self.WORKSPACE_CLUSTER_ENV_BUILD_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )

    @property
    def num_get_cluster_compute_calls(self) -> int:
        return self._num_get_cluster_compute_calls

    def set_cluster_compute_mapping(
        self, cluster_compute_id: str, cluster_compute: ClusterCompute
    ):
        self._cluster_computes[cluster_compute_id] = cluster_compute

    def get_cluster_compute(self, cluster_compute_id: str) -> FakeClientResult:
        self._num_get_cluster_compute_calls += 1
        if cluster_compute_id not in self._cluster_computes:
            raise ApiException(status=404)

        return FakeClientResult(result=self._cluster_computes[cluster_compute_id],)

    def set_cluster_env_name_mapping(
        self, cluster_environment_id: str, cluster_env_name: str
    ):
        self._cluster_env_names[cluster_environment_id] = cluster_env_name

    def get_cluster_environment(self, cluster_environment_id: str,) -> FakeClientResult:
        if cluster_environment_id not in self._cluster_env_names:
            raise ApiException(status=404)

        return FakeClientResult(
            result=ClusterEnvironment(
                name=self._cluster_env_names[cluster_environment_id],
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    def set_cluster_env_build_mapping(
        self,
        cluster_environment_build_id: str,
        *,
        cluster_environment_id: str,
        revision: int,
    ):
        self._cluster_env_builds[cluster_environment_build_id] = (
            cluster_environment_id,
            revision,
        )

    def get_cluster_environment_build(
        self, cluster_environment_build_id: str
    ) -> FakeClientResult:
        if cluster_environment_build_id not in self._cluster_env_builds:
            raise ApiException(status=404)

        cluster_environment_id, revision = self._cluster_env_builds[
            cluster_environment_build_id
        ]
        return FakeClientResult(
            result=ClusterEnvironmentBuild(
                revision=revision,
                cluster_environment_id=cluster_environment_id,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    def set_services_list(self, services: List[ServiceModel]):
        self._services_list = services

    def list_services(
        self, *, project_id: str, name: str, count: int, paging_token: Optional[str]
    ) -> ServicemodelListResponse:
        assert paging_token == self._next_services_list_paging_token
        int_paging_token = 0 if paging_token is None else int(paging_token)

        slice_begin = int_paging_token * count
        slice_end = min((int_paging_token + 1) * count, len(self._services_list))
        if slice_end == len(self._services_list):
            self._next_services_list_paging_token = None
        else:
            self._next_services_list_paging_token = str(int_paging_token + 1)

        return ServicemodelListResponse(
            results=self._services_list[slice_begin:slice_end],
            metadata=ListResponseMetadata(
                next_paging_token=self._next_services_list_paging_token,
                total=len(self._services_list),
            ),
        )


class FakeInternalAPIClient:
    """Fake implementation of the "internal" Anyscale REST API.

    Should mimic the behavior and return values of the client defined at:
    `anyscale.client.openai_client`.
    """

    FAKE_FILE_URI = "s3://some-bucket/{file_name}"
    FAKE_UPLOAD_URL_PREFIX = "http://some-domain.com/upload-magic-file/"

    def __init__(self):
        # Compute template ID to compute template.
        self._compute_templates: Dict[str, DecoratedComputeTemplate] = {}

    def generate_cloud_data_bucket_presigned_upload_url_api_v2_clouds_cloud_id_generate_cloud_data_bucket_presigned_upload_url_post(
        self, cloud_id: str, request: CloudDataBucketPresignedUploadRequest
    ) -> FakeClientResult:
        assert request.file_type == CloudDataBucketFileType.RUNTIME_ENV_PACKAGES
        assert isinstance(request.file_name, str)
        return FakeClientResult(
            result=CloudDataBucketPresignedUploadInfo(
                upload_url=self.FAKE_UPLOAD_URL_PREFIX + request.file_name,
                file_uri=self.FAKE_FILE_URI.format(file_name=request.file_name),
            ),
        )

    def add_compute_template(self, compute_template: DecoratedComputeTemplate):
        self._compute_templates[compute_template.id] = compute_template

    def create_compute_template_api_v2_compute_templates_post(
        self, create_compute_template: CreateComputeTemplate,
    ) -> FakeClientResult:
        compute_config_id = f"anonymous-compute-template-{str(uuid.uuid4())}"
        if create_compute_template.anonymous:
            assert not create_compute_template.name
            name = f"{compute_config_id}-name"
        else:
            assert create_compute_template.name
            name = create_compute_template.name

        compute_template = DecoratedComputeTemplate(
            id=compute_config_id,
            name=name,
            config=create_compute_template.config,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        self.add_compute_template(compute_template)
        return FakeClientResult(result=compute_template)

    def get_compute_template_api_v2_compute_templates_template_id_get(
        self, compute_config_id: str
    ) -> FakeClientResult:
        if compute_config_id not in self._compute_templates:
            raise ApiException(status=404)

        return FakeClientResult(result=self._compute_templates[compute_config_id])

    def search_compute_templates_api_v2_compute_templates_search_post(
        self, query: ComputeTemplateQuery
    ) -> DecoratedcomputetemplateListResponse:
        assert query.orgwide
        assert query.include_anonymous
        assert query.archive_status == ArchiveStatus.ALL

        assert len(query.name) == 1
        assert list(query.name.keys())[0] == "equals"
        name = list(query.name.values())[0]

        results = []
        for compute_template in self._compute_templates.values():
            if name == compute_template.name:
                results.append(compute_template)

        return DecoratedcomputetemplateListResponse(results=results)


@pytest.fixture()
def setup_anyscale_client(
    request,
) -> Generator[
    Tuple[RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient], None, None
]:
    if not hasattr(request, "param"):
        request.param = {}

    # Mimic running in a workspace by setting expected environment variables.
    mock_os_environ: Dict[str, str] = {}
    if request.param.get("inside_workspace", False):
        mock_os_environ.update(
            ANYSCALE_SESSION_ID=FakeExternalAPIClient.WORKSPACE_CLUSTER_ID,
            ANYSCALE_EXPERIMENTAL_WORKSPACE_ID="fake-workspace-id",
        )

        mock_os_environ.update(ANYSCALE_WORKSPACE_DYNAMIC_DEPENDENCY_TRACKING="1",)
        if request.param.get("workspace_dependency_tracking_disabled", False):
            mock_os_environ.update(ANYSCALE_SKIP_PYTHON_DEPENDENCY_TRACKING="1")

    fake_external_client = FakeExternalAPIClient()
    fake_internal_client = FakeInternalAPIClient()
    anyscale_client = RealAnyscaleClient(
        api_clients=(fake_external_client, fake_internal_client),
        workspace_requirements_file_path=TEST_WORKSPACE_REQUIREMENTS_FILE_PATH,
    )

    with patch.dict(os.environ, mock_os_environ):
        yield anyscale_client, fake_external_client, fake_internal_client


class FakeRequestsResponse:
    def __init__(self, *, should_raise: bool):
        self._should_raise = should_raise

    def raise_for_status(self):
        if self._should_raise:
            raise RequestException("Fake request error!")


class FakeRequests:
    def __init__(self):
        self._should_raise = False

        self.sent_json: Optional[Dict] = None
        self.sent_data: Optional[bytes] = None
        self.called_url: Optional[str] = None
        self.called_method: Optional[str] = None

    def set_should_raise(self, should_raise: bool):
        self._should_raise = should_raise

    def _do_request(
        self,
        method: str,
        url: str,
        *,
        data: Optional[bytes] = None,
        json: Optional[Dict] = None,
    ) -> FakeRequestsResponse:
        self.called_method = method
        self.called_url = url
        self.sent_data = data
        self.sent_json = json

        return FakeRequestsResponse(should_raise=self._should_raise)

    def put(self, url: str, *, data: Optional[bytes] = None) -> FakeRequestsResponse:
        return self._do_request("PUT", url, data=data)

    def post(self, url: str, *, json: Optional[Dict] = None) -> FakeRequestsResponse:
        return self._do_request("POST", url, json=json)


@pytest.fixture()
def fake_requests() -> Generator[FakeRequests, None, None]:
    fake_requests = FakeRequests()
    with patch("requests.post", new=fake_requests.post), patch(
        "requests.put", new=fake_requests.put
    ):
        yield fake_requests


class TestWorkspaceMethods:
    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": False}], indirect=True
    )
    def test_call_inside_workspace_outside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert not anyscale_client.inside_workspace()

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_call_inside_workspace_inside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert anyscale_client.inside_workspace()

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": False}], indirect=True
    )
    def test_call_get_current_workspace_cluster_outside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        assert anyscale_client.get_current_workspace_cluster() is None
        assert fake_external_client.num_get_cluster_calls == 0

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_call_get_current_workspace_cluster_inside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client

        # The cluster model should be cached so we only make one API call.
        for _ in range(100):
            cluster = anyscale_client.get_current_workspace_cluster()
            assert cluster is not None
            assert cluster.id == FakeExternalAPIClient.WORKSPACE_CLUSTER_ID
            assert cluster.project_id == FakeExternalAPIClient.WORKSPACE_PROJECT_ID
            assert (
                cluster.cluster_compute_id
                == FakeExternalAPIClient.WORKSPACE_CLUSTER_COMPUTE_ID
            )
            assert (
                cluster.cluster_environment_build_id
                == FakeExternalAPIClient.WORKSPACE_CLUSTER_ENV_BUILD_ID
            )

            assert fake_external_client.num_get_cluster_calls == 1

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": False,}], indirect=True
    )
    def test_call_get_workspace_requirements_path_outside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client

        # Should return None even if the file path exists.
        assert anyscale_client.get_workspace_requirements_path() is None

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_call_get_workspace_requirements_path_inside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert (
            anyscale_client.get_workspace_requirements_path()
            == TEST_WORKSPACE_REQUIREMENTS_FILE_PATH
        )

    @pytest.mark.parametrize(
        "setup_anyscale_client",
        [{"inside_workspace": True, "workspace_dependency_tracking_disabled": True}],
        indirect=True,
    )
    def test_call_get_workspace_requirements_path_inside_workspace_disabled(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert anyscale_client.get_workspace_requirements_path() is None

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": False}], indirect=True,
    )
    def test_send_notification_outside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
    ):
        anyscale_client, _, _ = setup_anyscale_client
        anyscale_client.send_workspace_notification(FAKE_WORKSPACE_NOTIFICATION)

        # Nothing should be sent because we're not in a workspace.
        assert fake_requests.called_url is None

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True,
    )
    def test_send_notification_inside_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
    ):
        anyscale_client, _, _ = setup_anyscale_client
        anyscale_client.send_workspace_notification(FAKE_WORKSPACE_NOTIFICATION)

        assert fake_requests.called_method == "POST"
        assert fake_requests.called_url == WORKSPACE_NOTIFICATION_ADDRESS
        assert fake_requests.sent_json == FAKE_WORKSPACE_NOTIFICATION.dict()

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True,
    )
    def test_send_notification_fails(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
    ):
        """Failing to send a notification should *not* raise an exception."""
        anyscale_client, _, _ = setup_anyscale_client
        fake_requests.set_should_raise(True)
        anyscale_client.send_workspace_notification(FAKE_WORKSPACE_NOTIFICATION)

        assert fake_requests.called_method == "POST"
        assert fake_requests.called_url == WORKSPACE_NOTIFICATION_ADDRESS
        assert fake_requests.sent_json == FAKE_WORKSPACE_NOTIFICATION.dict()


class TestGetCloudID:
    def test_get_default(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client

        # The cloud ID should be cached so we only make one API call.
        for _ in range(100):
            assert (
                anyscale_client.get_cloud_id() == FakeExternalAPIClient.DEFAULT_CLOUD_ID
            )
            assert fake_external_client.num_get_cloud_calls == 1
            assert fake_external_client.num_get_cluster_calls == 0
            assert fake_external_client.num_get_cluster_compute_calls == 0

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_get_from_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        # The cloud ID should be cached so we only make one API call.
        for _ in range(100):
            assert (
                anyscale_client.get_cloud_id()
                == FakeExternalAPIClient.WORKSPACE_CLOUD_ID
            )
            # get_cloud isn't called because it's from the workspace instead.
            assert fake_external_client.num_get_cloud_calls == 0
            assert fake_external_client.num_get_cluster_calls == 1
            assert fake_external_client.num_get_cluster_compute_calls == 1

    def test_get_compute_config_id(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        fake_external_client.set_cluster_compute_mapping(
            "fake-compute-config-id",
            ClusterCompute(
                name="fake-compute-config",
                id="fake-compute-config-id",
                config=ClusterComputeConfig(
                    cloud_id="compute-config-cloud-id",
                    local_vars_configuration=OPENAPI_NO_VALIDATION,
                ),
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

        assert (
            anyscale_client.get_cloud_id(compute_config_id="fake-compute-config-id")
            == "compute-config-cloud-id"
        )


class TestGetProjectID:
    def test_get_default(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client

        # The project ID should be cached so we only make one API call.
        for _ in range(100):
            assert (
                anyscale_client.get_project_id()
                == FakeExternalAPIClient.DEFAULT_PROJECT_ID
            )
            assert fake_external_client.num_get_project_calls == 1

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_get_from_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        assert (
            anyscale_client.get_project_id()
            == FakeExternalAPIClient.WORKSPACE_PROJECT_ID
        )


class TestComputeConfig:
    def test_get_default_compute_config_id(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert (
            anyscale_client.get_compute_config_id()
            == FakeExternalAPIClient.DEFAULT_CLUSTER_COMPUTE_ID
        )

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_get_compute_config_id_from_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        assert (
            anyscale_client.get_compute_config_id()
            == FakeExternalAPIClient.WORKSPACE_CLUSTER_COMPUTE_ID
        )

    def test_get_compute_config_id_by_name_not_found(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, fake_internal_client = setup_anyscale_client
        assert (
            anyscale_client.get_compute_config_id(compute_config_name="fake-news")
            is None
        )

    def test_get_compute_config_id_by_name(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, fake_internal_client = setup_anyscale_client
        fake_internal_client.add_compute_template(
            DecoratedComputeTemplate(
                id="fake-compute-config-id",
                name="fake-compute-config-name",
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )
        assert (
            anyscale_client.get_compute_config_id("fake-compute-config-name")
            == "fake-compute-config-id"
        )

        assert anyscale_client.get_compute_config_id("does-not-exist") is None

    def test_get_compute_config(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, fake_internal_client = setup_anyscale_client
        fake_internal_client.add_compute_template(
            DecoratedComputeTemplate(
                id="fake-compute-config-id",
                name="fake-compute-config-name",
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )
        assert anyscale_client.get_compute_config("does-not-exist") is None
        assert (
            anyscale_client.get_compute_config("fake-compute-config-id").name
            == "fake-compute-config-name"
        )

    def test_create_anonymous_compute_config(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client

        config = ComputeTemplateConfig(
            cloud_id="fake-cloud-id", local_vars_configuration=OPENAPI_NO_VALIDATION,
        )

        compute_config_id = anyscale_client.create_anonymous_compute_config(config,)

        compute_config = anyscale_client.get_compute_config(compute_config_id)
        assert compute_config is not None
        assert compute_config.id == compute_config_id
        assert compute_config.config == config


class TestClusterEnv:
    def test_get_default_cluster_env_build_id(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert (
            anyscale_client.get_cluster_env_build_id()
            == FakeExternalAPIClient.DEFAULT_CLUSTER_ENV_BUILD_ID
        )

    @pytest.mark.parametrize(
        "setup_anyscale_client", [{"inside_workspace": True}], indirect=True
    )
    def test_get_cluster_env_build_id_from_workspace(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        assert (
            anyscale_client.get_cluster_env_build_id()
            == FakeExternalAPIClient.WORKSPACE_CLUSTER_ENV_BUILD_ID
        )

    def test_get_cluster_env_name(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        fake_external_client.set_cluster_env_name_mapping(
            "fake-cluster-env-id", "fake-cluster-env-name"
        )
        fake_external_client.set_cluster_env_build_mapping(
            "fake-cluster-env-build-id",
            cluster_environment_id="fake-cluster-env-id",
            revision=5,
        )
        assert anyscale_client.get_cluster_env_name("does-not-exist") is None
        assert (
            anyscale_client.get_cluster_env_name("fake-cluster-env-build-id")
            == "fake-cluster-env-name:5"
        )


class TestUploadLocalDirToCloudStorage:
    @pytest.mark.parametrize("working_dir", TEST_WORKING_DIRS)
    def test_basic(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
        working_dir: str,
    ):
        anyscale_client, _, fake_internal_client = setup_anyscale_client
        uri = anyscale_client.upload_local_dir_to_cloud_storage(
            working_dir, cloud_id="test-cloud-id",
        )
        assert isinstance(uri, str) and len(uri) > 0
        assert fake_requests.called_method == "PUT"
        assert (
            fake_requests.called_url is not None
            and fake_requests.called_url.startswith(
                fake_internal_client.FAKE_UPLOAD_URL_PREFIX
            )
        )
        assert fake_requests.sent_data is not None and len(fake_requests.sent_data) > 0

    def test_missing_dir(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        with pytest.raises(
            RuntimeError, match="Path 'does_not_exist' is not a valid directory."
        ):
            anyscale_client.upload_local_dir_to_cloud_storage(
                "does_not_exist", cloud_id="test-cloud-id",
            )

    def test_uri_content_addressed(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
    ):
        anyscale_client, _, _ = setup_anyscale_client

        # Uploading the same directory contents should result in the same content-addressed URI.
        uri1 = anyscale_client.upload_local_dir_to_cloud_storage(
            BASIC_WORKING_DIR, cloud_id="test-cloud-id",
        )
        uri2 = anyscale_client.upload_local_dir_to_cloud_storage(
            BASIC_WORKING_DIR, cloud_id="test-cloud-id",
        )
        assert uri1 == uri2

        # Uploading a different directory should not result in the same content-addressed URI.
        uri3 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id",
        )
        assert uri1 != uri3 and uri2 != uri3

    def test_excludes(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
        fake_requests: FakeRequests,
    ):
        anyscale_client, _, _ = setup_anyscale_client

        # No exclusions.
        uri1 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id",
        )

        # Exclusions that don't match anything.
        uri2 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id", excludes=["does-not-exist"],
        )

        assert uri1 == uri2

        # Exclude a subdirectory.
        uri3 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id", excludes=["subdir"],
        )

        assert uri3 != uri1

        # Exclude requirements.txt by name.
        uri4 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id", excludes=["requirements.txt"],
        )

        assert uri4 != uri3 and uri4 != uri1

        # Exclude requirements.txt by wildcard.
        uri5 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id", excludes=["*.txt"],
        )

        assert uri5 == uri4


class TestGetService:
    def _make_service_model(self, name: str,) -> ServiceModel:
        # Use UUID for ID to make models unique.
        return ServiceModel(
            id=str(uuid.uuid4()),
            name=name,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )

    def test_get_service_none_returned(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, _, _ = setup_anyscale_client
        assert anyscale_client.get_service("test-service-name") is None

    def test_get_service_one_returned_matches(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        model = self._make_service_model("test-service-name")
        fake_external_client.set_services_list([model])

        returned_model = anyscale_client.get_service("test-service-name")
        assert returned_model is not None
        assert returned_model == model

    def test_get_service_multiple_returned_one_matches(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        model = self._make_service_model("test-service-name")
        all_models = [
            self._make_service_model(f"other-service-name-{i}") for i in range(5)
        ]
        all_models.insert(0, model)
        fake_external_client.set_services_list(all_models)

        returned_model = anyscale_client.get_service("test-service-name")
        assert returned_model is not None
        assert returned_model == model

    def test_get_service_many_pages(
        self,
        setup_anyscale_client: Tuple[
            RealAnyscaleClient, FakeExternalAPIClient, FakeInternalAPIClient
        ],
    ):
        anyscale_client, fake_external_client, _ = setup_anyscale_client
        model = self._make_service_model("test-service-name")
        all_models = [
            self._make_service_model(f"other-service-name-{i}")
            for i in range((10 * anyscale_client.LIST_ENDPOINT_COUNT) + 5)
        ]
        all_models.insert(0, model)
        fake_external_client.set_services_list(all_models)

        returned_model = anyscale_client.get_service("test-service-name")
        assert returned_model is not None
        assert returned_model == model
