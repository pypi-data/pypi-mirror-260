import copy
from dataclasses import dataclass
import os
from typing import Any, Dict, List, Optional, Tuple

import pytest

from anyscale.client.openapi_client.models import ComputeTemplate, ComputeTemplateConfig
from anyscale.sdk.anyscale_client.configuration import Configuration
from anyscale.sdk.anyscale_client.models import (
    ApplyServiceModel,
    ProductionServiceV2VersionModel,
    ServiceEventCurrentState,
    ServiceModel,
)
from anyscale.service._private.anyscale_client import (
    FakeAnyscaleClient,
    WORKSPACE_CLUSTER_NAME_PREFIX,
)
from anyscale.service._private.sdk import ServiceSDK
from anyscale.service.models import (
    ServiceConfig,
    ServiceState,
    ServiceStatus,
    ServiceVersionStatus,
)
from anyscale.utils.workspace_notification import (
    WorkspaceNotification,
    WorkspaceNotificationAction,
)


OPENAPI_NO_VALIDATION = Configuration()
OPENAPI_NO_VALIDATION.client_side_validation = False

TEST_COMPUTE_CONFIG_DICT = {
    "cloud_id": "fake-cloud-id",
    "region": "fake-region",
    "head_node_type": {
        "name": "fake-head-node-name",
        "instance_type": "fake-instance-type",
    },
    "worker_node_types": [],
    "auto_select_worker_config": False,
}


@pytest.fixture()
def sdk_with_fake_client() -> Tuple[ServiceSDK, FakeAnyscaleClient]:
    fake_client = FakeAnyscaleClient()
    return ServiceSDK(client=fake_client), fake_client


class TestDeployBasic:
    def test_validation(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )

        with pytest.raises(TypeError):
            sdk.deploy(config, in_place="in_place")

        with pytest.raises(TypeError):
            sdk.deploy(config, canary_percent="10")

        with pytest.raises(ValueError):
            sdk.deploy(config, canary_percent=-1)

        with pytest.raises(ValueError):
            sdk.deploy(config, canary_percent=101)

        with pytest.raises(TypeError):
            sdk.deploy(config, max_surge_percent="10")

        with pytest.raises(ValueError):
            sdk.deploy(config, max_surge_percent=-1)

        with pytest.raises(ValueError):
            sdk.deploy(config, max_surge_percent=101)

    def test_basic(self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]):
        sdk, fake_client = sdk_with_fake_client

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(config)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id=fake_client.DEFAULT_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
        )

    def test_custom_image(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_cluster_env_mapping("my-custom-image", "img_id123")

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            image="my-custom-image",
        )
        sdk.deploy(config)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id="img_id123",
            compute_config_id=fake_client.DEFAULT_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
        )

        with pytest.raises(
            ValueError, match="The image 'does-not-exist' does not exist."
        ):
            sdk.deploy(config.options(image="does-not-exist"))

    def test_custom_compute_config_name(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        fake_client.add_compute_config(
            ComputeTemplate(
                id="compute_id123",
                name="my-custom-compute-config",
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )
        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            compute_config="my-custom-compute-config",
        )
        sdk.deploy(config)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id="compute_id123",
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
        )

        with pytest.raises(
            ValueError, match="The compute config 'does-not-exist' does not exist."
        ):
            sdk.deploy(config.options(compute_config="does-not-exist"))

    def test_custom_compute_config_dict(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        # Specify a compute config as a dictionary (anonymous).
        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            compute_config=TEST_COMPUTE_CONFIG_DICT,
        )
        sdk.deploy(config)
        anonymous_compute_config_id = fake_client.rolled_out_model.compute_config_id
        anonymous_compute_config = fake_client.get_compute_config(
            anonymous_compute_config_id
        )
        assert anonymous_compute_config.anonymous
        assert anonymous_compute_config.id == anonymous_compute_config_id
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id=anonymous_compute_config_id,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
        )

        # Test an invalid dict.
        with pytest.raises(RuntimeError, match="Invalid compute config"):
            config = ServiceConfig(
                applications=[{"import_path": "main:app"}],
                name="test-service-name",
                compute_config={"bad": "config"},
            )
            sdk.deploy(config)

    def test_in_place(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(config, in_place=True)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id=fake_client.DEFAULT_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="IN_PLACE",
        )

    def test_canary_percent(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(config, canary_percent=50)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id=fake_client.DEFAULT_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
            canary_percent=50,
        )

    def test_max_surge_percent(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(config, max_surge_percent=50)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.DEFAULT_PROJECT_ID,
            build_id=fake_client.DEFAULT_CLUSTER_ENV_BUILD_ID,
            compute_config_id=fake_client.DEFAULT_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
            max_surge_percent=50,
        )

    def test_workspace_notification_is_sent(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(True)

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(config)

        service_id = fake_client.get_service("test-service-name").id
        assert fake_client.sent_workspace_notifications == [
            WorkspaceNotification(
                body="Service 'test-service-name' deployed.",
                action=WorkspaceNotificationAction(
                    type="navigate-service", title="View Service", value=service_id,
                ),
            )
        ]


class TestDeployWorkspaceDefaults:
    def test_name_defaults_to_workspace_name(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        # Happy path: workspace cluster name has the expected prefix.
        fake_client.set_inside_workspace(
            True,
            cluster_name=WORKSPACE_CLUSTER_NAME_PREFIX + "super-special-workspace-name",
        )
        config = ServiceConfig(applications=[{"import_path": "main:app"}])
        sdk.deploy(config)
        assert fake_client.rolled_out_model.name == "super-special-workspace-name"

        # Defensive path: workspace cluster name doesn't have the expected prefix.
        fake_client.set_inside_workspace(
            True, cluster_name="not-sure-how-this-happened"
        )
        config = ServiceConfig(applications=[{"import_path": "main:app"}])
        sdk.deploy(config)
        assert fake_client.rolled_out_model.name == "not-sure-how-this-happened"

    def test_pick_up_cluster_configs(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(True)

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            working_dir="s3://remote.zip",
        )
        sdk.deploy(config)
        assert fake_client.rolled_out_model == ApplyServiceModel(
            name="test-service-name",
            project_id=fake_client.WORKSPACE_PROJECT_ID,
            build_id=fake_client.WORKSPACE_CLUSTER_ENV_BUILD_ID,
            compute_config_id=fake_client.WORKSPACE_CLUSTER_COMPUTE_ID,
            ray_serve_config={"applications": config.applications},
            rollout_strategy="ROLLOUT",
        )

    def test_override_working_dir(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(True)

        config = ServiceConfig(
            name="test-service-name",
            applications=[
                {"name": "no-runtime-env", "import_path": "main:app",},
                {
                    "name": "empty-runtime-env",
                    "import_path": "main:app",
                    "runtime_env": {},
                },
                {
                    "name": "other-working-dir",
                    "import_path": "main:app",
                    # Specified working_dir shouldn't be overwritten.
                    "runtime_env": {"working_dir": "other-path/"},
                },
                {
                    "name": "working-dir-none",
                    "import_path": "main:app",
                    # Setting working_dir to None should disable uploading.
                    "runtime_env": {"working_dir": None},
                },
            ],
        )

        sdk.deploy(config)
        applications = fake_client.rolled_out_model.ray_serve_config["applications"]
        assert len(applications) == 4

        # First app should have been autopopulated to local dir.
        assert applications[0]["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.WORKSPACE_CLOUD_ID
            )
        )
        autopopulated_uri = applications[0]["runtime_env"]["working_dir"]

        # Second app should have been autopopulated to local dir (and share the same URI).
        assert applications[1]["runtime_env"]["working_dir"] == autopopulated_uri

        # Third app should have not been altered and have a different URI.
        assert applications[2]["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.WORKSPACE_CLOUD_ID
            )
        )
        assert applications[2]["runtime_env"]["working_dir"] != autopopulated_uri

        # Fourth app should be untouched.
        assert applications[3]["runtime_env"]["working_dir"] is None

    @pytest.mark.parametrize("workspace_tracking_enabled", [False, True])
    def test_override_requirements(
        self,
        sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
        workspace_tracking_enabled: bool,
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(
            True,
            requirements_path=SINGLE_LINE_REQUIREMENTS.get_path()
            if workspace_tracking_enabled
            else None,
        )

        config = ServiceConfig(
            name="test-service-name",
            applications=[
                {"name": "no-runtime-env", "import_path": "main:app",},
                {
                    "name": "empty-runtime-env",
                    "import_path": "main:app",
                    "runtime_env": {},
                },
                {
                    "name": "other-requirements-file",
                    "import_path": "main:app",
                    # Specified requirements file shouldn't be overwritten.
                    "runtime_env": {"pip": MULTI_LINE_REQUIREMENTS.get_path()},
                },
                {
                    "name": "other-requirements-list",
                    "import_path": "main:app",
                    # Specified requirements list shouldn't be overwritten.
                    "runtime_env": {"pip": ["testabc", "test123"]},
                },
                {
                    "name": "requirements-none",
                    "import_path": "main:app",
                    # Setting requirements to None should disable uploading.
                    "runtime_env": {"pip": None},
                },
            ],
        )

        sdk.deploy(config)
        applications = fake_client.rolled_out_model.ray_serve_config["applications"]
        assert len(applications) == 5

        if workspace_tracking_enabled:
            expected_workspace_pip = SINGLE_LINE_REQUIREMENTS.expected_pip_list

            # First app should have been autopopulated to workspace requirements.
            assert applications[0]["runtime_env"]["pip"] == expected_workspace_pip

            # Second app should have been autopopulated to workspace requirements.
            assert applications[1]["runtime_env"]["pip"] == expected_workspace_pip

            # Third app should not have been overwritten and its file should have been reaad.
            assert (
                applications[2]["runtime_env"]["pip"]
                == MULTI_LINE_REQUIREMENTS.expected_pip_list
            )

            # Fourth app should be untouched.
            assert applications[3]["runtime_env"]["pip"] == ["testabc", "test123"]

            # Fifth app should be untouched.
            assert applications[4]["runtime_env"]["pip"] is None
        else:
            # None should be overridden if tracking is not enabled.
            assert "pip" not in applications[0]["runtime_env"]
            assert "pip" not in applications[1]["runtime_env"]
            assert (
                applications[2]["runtime_env"]["pip"]
                == MULTI_LINE_REQUIREMENTS.expected_pip_list
            )
            assert applications[3]["runtime_env"]["pip"] == ["testabc", "test123"]
            assert applications[4]["runtime_env"]["pip"] is None


class TestDeployUploadDirs:
    @pytest.mark.parametrize("inside_workspace", [False, True])
    def test_upload_basic_working_dir(
        self,
        sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
        inside_workspace: bool,
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(inside_workspace)

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            working_dir=".",
        )
        original_config = copy.deepcopy(config)

        sdk.deploy(config)
        # The original config should not be modified.
        assert config == original_config

        [application] = fake_client.rolled_out_model.ray_serve_config["applications"]

        # Check that the correct cloud_id was used for the upload.
        expected_cloud_id = (
            FakeAnyscaleClient.WORKSPACE_CLOUD_ID
            if inside_workspace
            else FakeAnyscaleClient.DEFAULT_CLOUD_ID
        )
        assert application["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(cloud_id=expected_cloud_id)
        )

    def test_upload_uses_cloud_from_compute_config(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.add_compute_config(
            ComputeTemplate(
                id="fake-compute-config-id",
                name="fake-compute-config",
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )
        fake_client.set_compute_config_id_to_cloud_id_mapping(
            "fake-compute-config-id", "compute-config-cloud-id"
        )

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            working_dir=".",
            compute_config="fake-compute-config",
        )
        sdk.deploy(config)

        [application] = fake_client.rolled_out_model.ray_serve_config["applications"]

        # Check that the correct cloud_id was used for the upload.
        expected_cloud_id = "compute-config-cloud-id"
        assert application["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(cloud_id=expected_cloud_id)
        )

    def test_upload_with_no_local_dirs(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        """Configs should be left unchanged if there are no local dirs."""
        sdk, fake_client = sdk_with_fake_client

        basic_config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="test-service-name"
        )
        sdk.deploy(basic_config)
        assert (
            fake_client.rolled_out_model.ray_serve_config["applications"]
            == basic_config.applications
        )

        config_with_requirements = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            requirements=["pip-install-test"],
        )
        sdk.deploy(config_with_requirements)
        assert (
            fake_client.rolled_out_model.ray_serve_config["applications"]
            == config_with_requirements.applications
        )

        complex_config = ServiceConfig(
            name="test-service-name",
            applications=[
                {"name": "app1", "import_path": "main:app",},
                {
                    "name": "app2",
                    "import_path": "main:app",
                    "runtime_env": {"env_vars": {"foo": "bar",},},
                },
            ],
        )
        sdk.deploy(complex_config)
        assert (
            fake_client.rolled_out_model.ray_serve_config["applications"]
            == complex_config.applications
        )

    def test_no_upload_remote_working_dir(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-service-name",
            working_dir="s3://some-remote-uri.zip",
        )

        sdk.deploy(config)
        applications = fake_client.rolled_out_model.ray_serve_config["applications"]
        assert len(applications) == 1
        assert (
            applications[0]["runtime_env"]["working_dir"] == "s3://some-remote-uri.zip"
        )

    def test_upload_local_py_modules(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        config = ServiceConfig(
            name="test-service-name",
            applications=[
                {
                    "import_path": "main:app",
                    "runtime_env": {
                        "py_modules": [
                            # Should be left alone.
                            "s3://some-remote-uri.zip",
                            # Should be uploaded.
                            "local-path",
                        ],
                    },
                },
            ],
        )
        sdk.deploy(config)
        applications = fake_client.rolled_out_model.ray_serve_config["applications"]
        assert len(applications) == 1
        assert (
            applications[0]["runtime_env"]["py_modules"][0]
            == "s3://some-remote-uri.zip"
        )
        assert applications[0]["runtime_env"]["py_modules"][1].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )

    def test_upload_caching(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        """The same directory should only by uploaded once."""
        sdk, fake_client = sdk_with_fake_client
        config = ServiceConfig(
            name="test-service-name",
            applications=[
                {
                    "name": "app1",
                    "import_path": "main:app",
                    "runtime_env": {"working_dir": ".",},
                },
                {
                    "name": "app2",
                    "import_path": "main:app",
                    "runtime_env": {
                        "working_dir": ".",
                        "py_modules": [".", "other-dir",],
                    },
                },
            ],
        )
        sdk.deploy(config)
        applications = fake_client.rolled_out_model.ray_serve_config["applications"]
        assert len(applications) == 2
        assert applications[0]["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )
        common_uri = applications[0]["runtime_env"]["working_dir"]

        assert applications[1]["runtime_env"]["working_dir"] == common_uri
        assert applications[1]["runtime_env"]["py_modules"][0] == common_uri
        assert applications[1]["runtime_env"]["py_modules"][1] != common_uri
        assert applications[1]["runtime_env"]["py_modules"][1].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )


@dataclass
class RequirementsFile:
    name: str
    expected_pip_list: Optional[List[str]]

    def get_path(self) -> str:
        return os.path.join(
            os.path.dirname(__file__), "test_requirements_files", self.name,
        )


SINGLE_LINE_REQUIREMENTS = RequirementsFile("single_line.txt", ["pip-install-test"])
MULTI_LINE_REQUIREMENTS = RequirementsFile(
    "multi_line.txt", ["pip-install-test", "torch==1.10.1"]
)

TEST_REQUIREMENTS_FILES = [
    SINGLE_LINE_REQUIREMENTS,
    MULTI_LINE_REQUIREMENTS,
    RequirementsFile("does_not_exist.txt", None),
    RequirementsFile("empty.txt", []),
    RequirementsFile(
        "multi_line_with_whitespace.txt",
        ["pip-install-test", "torch==1.10.1", "something-else"],
    ),
    RequirementsFile("comments.txt", ["pip-install-test", "torch==1.10.1"]),
]


class TestLoadRequirementsFiles:
    @pytest.mark.parametrize("requirements", [None, *TEST_REQUIREMENTS_FILES])
    @pytest.mark.parametrize("in_applications", [False, True])
    def test_override_requirements_file(
        self,
        sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
        requirements: Optional[RequirementsFile],
        in_applications: bool,
    ):
        sdk, fake_client = sdk_with_fake_client

        applications: List[Dict[str, Any]] = [
            {"name": "no_runtime_env", "import_path": "main:app"},
            {
                "name": "empty_runtime_env",
                "import_path": "main:app",
                "runtime_env": {},
            },
            {
                "name": "has_runtime_env",
                "import_path": "main:app",
                "runtime_env": {
                    "env_vars": {"abc": "123"},
                    "working_dir": "s3://somewhere.zip",
                },
            },
        ]
        if in_applications and requirements is not None:
            for application in applications:
                assert isinstance(application, dict)
                runtime_env = application.get("runtime_env", {})
                runtime_env["pip"] = requirements.get_path()
                application["runtime_env"] = runtime_env

            config = ServiceConfig(name="test-service-name", applications=applications)
        else:
            config = ServiceConfig(
                name="test-service-name",
                applications=applications,
                requirements=requirements.get_path() if requirements else None,
            )

        if requirements is not None and requirements.expected_pip_list is None:
            with pytest.raises(FileNotFoundError):
                sdk.deploy(config)

            return

        sdk.deploy(config)
        deployed_ray_serve_config = fake_client.rolled_out_model.ray_serve_config
        if requirements is None:
            assert deployed_ray_serve_config["applications"] == config.applications
        else:
            assert len(deployed_ray_serve_config["applications"]) == 3
            assert deployed_ray_serve_config["applications"][0] == {
                "name": "no_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"pip": requirements.expected_pip_list},
            }

            assert deployed_ray_serve_config["applications"][1] == {
                "name": "empty_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"pip": requirements.expected_pip_list},
            }
            assert deployed_ray_serve_config["applications"][2] == {
                "name": "has_runtime_env",
                "import_path": "main:app",
                "runtime_env": {
                    "env_vars": {"abc": "123"},
                    "working_dir": "s3://somewhere.zip",
                    "pip": requirements.expected_pip_list,
                },
            }


TEST_SERVICE_NAME = "fake-service-name"
TEST_SERVICE_ID = "fake-service-id"
TEST_QUERY_URL = "fake-query-url"

TEST_CLUSTER_ENV_NAME = "fake-build:3"
TEST_CLUSTER_ENV_BUILD_ID = "fake-build-id"

TEST_COMPUTE_CONFIG_NAME = "fake-compute-config"
TEST_COMPUTE_CONFIG_ID = "fake-compute-config-id"

TEST_APPLICATIONS = [{"import_path": "main:app"}]

DEFAULT_EXPECTED_STATUS = ServiceStatus(
    name=TEST_SERVICE_NAME,
    state=ServiceState.TERMINATED,
    query_url=TEST_QUERY_URL,
    query_auth_token=None,
    primary_version=None,
    canary_version=None,
)


def _expected_status(**kwargs) -> ServiceStatus:
    return ServiceStatus(**{**DEFAULT_EXPECTED_STATUS.to_dict(), **kwargs,})


def _service_version_model(
    name: str,
    weight: int,
    *,
    build_id: str = TEST_CLUSTER_ENV_BUILD_ID,
    compute_config_id: str = TEST_COMPUTE_CONFIG_ID,
    applications: Optional[List[Dict[str, Any]]] = None,
) -> ProductionServiceV2VersionModel:
    return ProductionServiceV2VersionModel(
        version=name,
        weight=weight,
        build_id=build_id,
        compute_config_id=compute_config_id,
        ray_serve_config={"applications": applications or TEST_APPLICATIONS},
        local_vars_configuration=OPENAPI_NO_VALIDATION,
    )


@dataclass
class ServiceStatusTestCase:
    id: str = TEST_SERVICE_ID
    name: str = TEST_SERVICE_NAME
    state: ServiceEventCurrentState = ServiceEventCurrentState.TERMINATED
    base_url: str = TEST_QUERY_URL
    auth_token: Optional[str] = None
    primary_version: Optional[ProductionServiceV2VersionModel] = None
    canary_version: Optional[ProductionServiceV2VersionModel] = None

    expected_status: ServiceStatus = DEFAULT_EXPECTED_STATUS

    def service_model(self) -> ServiceModel:
        return ServiceModel(
            id=self.id,
            name=self.name,
            current_state=self.state,
            base_url=self.base_url,
            auth_token=self.auth_token,
            primary_version=self.primary_version,
            canary_version=self.canary_version,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )


SERVICE_STATUS_TEST_CASES = [
    ServiceStatusTestCase(),
    ServiceStatusTestCase(expected_status=DEFAULT_EXPECTED_STATUS),
    # Test that states are mapped correctly.
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.STARTING,
        expected_status=_expected_status(state=ServiceState.STARTING),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.RUNNING,
        expected_status=_expected_status(state=ServiceState.RUNNING),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.ROLLING_OUT,
        expected_status=_expected_status(state=ServiceState.ROLLING_OUT),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.ROLLING_BACK,
        expected_status=_expected_status(state=ServiceState.ROLLING_BACK),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.UPDATING,
        expected_status=_expected_status(state=ServiceState.UPDATING),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.TERMINATING,
        expected_status=_expected_status(state=ServiceState.TERMINATING),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.TERMINATED,
        expected_status=_expected_status(state=ServiceState.TERMINATED),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.UNHEALTHY,
        expected_status=_expected_status(state=ServiceState.UNHEALTHY),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.SYSTEM_FAILURE,
        expected_status=_expected_status(state=ServiceState.SYSTEM_FAILURE),
    ),
    # Test that unrecognized states are mapped to ServiceState.UNKNOWN.
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.USER_ERROR_FAILURE,
        expected_status=_expected_status(state=ServiceState.UNKNOWN),
    ),
    ServiceStatusTestCase(
        auth_token="test-token-abc123",
        expected_status=_expected_status(query_auth_token="test-token-abc123"),
    ),
    # Test that primary and canary versions are mapped correctly.
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.RUNNING,
        primary_version=_service_version_model("primary", 100),
        expected_status=_expected_status(
            state=ServiceState.RUNNING,
            primary_version=ServiceVersionStatus(
                name="primary",
                weight=100,
                config=ServiceConfig(
                    name=TEST_SERVICE_NAME,
                    applications=TEST_APPLICATIONS,
                    image=TEST_CLUSTER_ENV_NAME,
                    compute_config=TEST_COMPUTE_CONFIG_NAME,
                ),
            ),
        ),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.RUNNING,
        primary_version=_service_version_model("primary", 50),
        canary_version=_service_version_model("canary", 50),
        expected_status=_expected_status(
            state=ServiceState.RUNNING,
            primary_version=ServiceVersionStatus(
                name="primary",
                weight=50,
                config=ServiceConfig(
                    name=TEST_SERVICE_NAME,
                    applications=TEST_APPLICATIONS,
                    image=TEST_CLUSTER_ENV_NAME,
                    compute_config=TEST_COMPUTE_CONFIG_NAME,
                ),
            ),
            canary_version=ServiceVersionStatus(
                name="canary",
                weight=50,
                config=ServiceConfig(
                    name=TEST_SERVICE_NAME,
                    applications=TEST_APPLICATIONS,
                    image=TEST_CLUSTER_ENV_NAME,
                    compute_config=TEST_COMPUTE_CONFIG_NAME,
                ),
            ),
        ),
    ),
    # Test that when the service is TERMINATED, primary/canary versions are ignored.
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.TERMINATED,
        primary_version=_service_version_model("primary", 100),
        expected_status=_expected_status(state=ServiceState.TERMINATED),
    ),
    ServiceStatusTestCase(
        state=ServiceEventCurrentState.TERMINATED,
        canary_version=_service_version_model("canary", 100),
        expected_status=_expected_status(state=ServiceState.TERMINATED),
    ),
]


class TestStatus:
    def test_service_not_found(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_inside_workspace(True)

        with pytest.raises(
            RuntimeError, match="Service with name 'test-service-name' was not found."
        ):
            sdk.status("test-service-name")

    @pytest.mark.parametrize("test_case", SERVICE_STATUS_TEST_CASES)
    def test_build_status_from_model(
        self,
        sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
        test_case: ServiceStatusTestCase,
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_cluster_env_mapping(
            TEST_CLUSTER_ENV_NAME, TEST_CLUSTER_ENV_BUILD_ID
        )
        fake_client.add_compute_config(
            ComputeTemplate(
                id=TEST_COMPUTE_CONFIG_ID,
                name=TEST_COMPUTE_CONFIG_NAME,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )
        service_model = test_case.service_model()
        fake_client.update_service(service_model)

        status: ServiceStatus = sdk.status(name=service_model.name)
        assert (
            status == test_case.expected_status
        ), f"Expected: {test_case.expected_status}\nActual: {status}"

    def test_default_name_in_workspace(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        test_case = ServiceStatusTestCase(
            name="default-name-from-workspace",
            expected_status=_expected_status(name="default-name-from-workspace"),
        )
        service_model = test_case.service_model()
        fake_client.update_service(service_model)
        fake_client.set_cluster_env_mapping(
            TEST_CLUSTER_ENV_NAME, TEST_CLUSTER_ENV_BUILD_ID
        )
        fake_client.add_compute_config(
            ComputeTemplate(
                id=TEST_COMPUTE_CONFIG_ID,
                name=TEST_COMPUTE_CONFIG_NAME,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )
        fake_client.set_inside_workspace(
            True,
            cluster_name=WORKSPACE_CLUSTER_NAME_PREFIX + "default-name-from-workspace",
        )

        status: ServiceStatus = sdk.status()
        assert (
            status == test_case.expected_status
        ), f"Expected: {test_case.expected_status}\nActual: {status}"

    def test_failed_to_get_cluster_env_name(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        test_case = ServiceStatusTestCase(
            state=ServiceEventCurrentState.RUNNING,
            primary_version=_service_version_model("primary", 100),
        )
        service_model = test_case.service_model()
        fake_client.update_service(service_model)
        fake_client.add_compute_config(
            ComputeTemplate(
                id=TEST_COMPUTE_CONFIG_ID,
                name=TEST_COMPUTE_CONFIG_NAME,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )

        with pytest.raises(RuntimeError, match="Failed to get cluster env name"):
            sdk.status(name=service_model.name)

    def test_failed_to_get_compute_config_name(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, fake_client = sdk_with_fake_client

        test_case = ServiceStatusTestCase(
            state=ServiceEventCurrentState.RUNNING,
            primary_version=_service_version_model("primary", 100),
        )
        service_model = test_case.service_model()
        fake_client.update_service(service_model)
        fake_client.set_cluster_env_mapping(
            TEST_CLUSTER_ENV_NAME, TEST_CLUSTER_ENV_BUILD_ID
        )

        with pytest.raises(RuntimeError, match="Failed to get compute config"):
            sdk.status(name=service_model.name)

    def test_anonymous_compute_config_inlined(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient],
    ):
        sdk, fake_client = sdk_with_fake_client
        fake_client.set_cluster_env_mapping(
            TEST_CLUSTER_ENV_NAME, TEST_CLUSTER_ENV_BUILD_ID
        )
        fake_client.add_compute_config(
            ComputeTemplate(
                anonymous=True,
                id="anonymous-compute-config-id",
                name="anonymous-compute-config-name",
                config=ComputeTemplateConfig(**TEST_COMPUTE_CONFIG_DICT,),
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        )

        test_case = ServiceStatusTestCase(
            state=ServiceEventCurrentState.RUNNING,
            primary_version=_service_version_model(
                "primary", 100, compute_config_id="anonymous-compute-config-id"
            ),
            expected_status=_expected_status(
                state=ServiceState.RUNNING,
                primary_version=ServiceVersionStatus(
                    name="primary",
                    weight=100,
                    config=ServiceConfig(
                        name=TEST_SERVICE_NAME,
                        applications=TEST_APPLICATIONS,
                        image=TEST_CLUSTER_ENV_NAME,
                        compute_config=TEST_COMPUTE_CONFIG_DICT,
                    ),
                ),
            ),
        )
        service_model = test_case.service_model()
        fake_client.update_service(service_model)

        status: ServiceStatus = sdk.status(name=service_model.name)
        assert (
            status == test_case.expected_status
        ), f"Expected: {test_case.expected_status}\nActual: {status}"
