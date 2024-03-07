import copy
import os
from typing import Any, Dict, Generator, Optional
from unittest.mock import patch

import click
from click.testing import CliRunner
import pytest

from anyscale.commands.service_commands import deploy
from anyscale.service.models import ServiceConfig, ServiceState, ServiceStatus


MINIMAL_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "test_config_files", "minimal.yaml",
)
FULL_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "test_config_files", "full.yaml",
)
MULTI_LINE_REQUIREMENTS_PATH = os.path.join(
    os.path.dirname(__file__), "test_requirements_files", "multi_line.txt",
)


class FakeServiceSDK:
    DEFAULT_SERVICE_NAME = "fake-service-name"

    def __init__(self):
        self._fetched_name: Optional[str] = None
        self._deployed_config: Optional[ServiceConfig] = None
        self._deployed_kwargs: Dict[str, Any] = {}

    @property
    def deployed_config(self) -> Optional[ServiceConfig]:
        return self._deployed_config

    @property
    def deployed_kwargs(self) -> Dict[str, Any]:
        return copy.deepcopy(self._deployed_kwargs)

    def deploy(self, config: ServiceConfig, **kwargs):
        assert isinstance(config, ServiceConfig)
        self._deployed_config = config
        self._deployed_kwargs = kwargs

    def status(self, name: Optional[str] = None) -> ServiceStatus:
        self._fetched_name = name
        return ServiceStatus(
            name=name or self.DEFAULT_SERVICE_NAME,
            state=ServiceState.TERMINATED,
            query_url="http://fake-service-url/",
            query_auth_token="asdf1234",
        )


@pytest.fixture()
def fake_service_sdk() -> Generator[FakeServiceSDK, None, None]:
    fake_service_sdk = FakeServiceSDK()
    with patch(
        "anyscale.service.commands._LAZY_GLOBAL_SDK", new=fake_service_sdk,
    ):
        yield fake_service_sdk


def _assert_error_message(result: click.testing.Result, *, message: str):
    assert result.exit_code != 0
    assert message in result.stdout


class TestDeploy:
    def test_deploy_no_arg(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy)
        _assert_error_message(
            result, message="Either config file or import path must be provided."
        )

    def test_deploy_from_import_path(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

    def test_deploy_from_import_path_with_args(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "arg1=val1", "arg2=val2"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[
                {
                    "import_path": "main:app",
                    "arguments": {"arg1": "val1", "arg2": "val2"},
                }
            ],
        )
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

    def test_deploy_from_import_path_with_bad_arg(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "bad_arg"])
        _assert_error_message(result, message="Invalid application argument 'bad_arg'")

    def test_deploy_from_file(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["-f", MINIMAL_CONFIG_PATH])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

    def test_deploy_from_file_with_import_path(self, fake_service_sdk):
        runner = CliRunner()
        os.path.join(
            os.path.dirname(__file__), "test_config_files", "minimal.yaml",
        )

        result = runner.invoke(
            deploy, ["-f", MINIMAL_CONFIG_PATH, "main:app", "arg1=val1"]
        )
        _assert_error_message(
            result,
            message="When config file is provided, import path and application arguments can't be.",
        )

        result = runner.invoke(deploy, ["-f", MINIMAL_CONFIG_PATH, "main:app"])
        _assert_error_message(
            result,
            message="When config file is provided, import path and application arguments can't be.",
        )

    @pytest.mark.parametrize("flag", ["--in-place", "-i"])
    def test_deploy_in_place(self, fake_service_sdk, flag: str):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", flag])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": None,
            "in_place": True,
            "max_surge_percent": None,
        }

    def test_deploy_canary_percent(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "--canary-percent", "50"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": 50,
            "in_place": False,
            "max_surge_percent": None,
        }

    def test_deploy_max_surge_percent(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "--max-surge-percent", "50"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": None,
            "in_place": False,
            "max_surge_percent": 50,
        }

    def test_deploy_excludes(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

        # Pass a single exclusion.
        result = runner.invoke(deploy, ["--exclude", "path1", "main:app"])
        assert result.exit_code == 0, result.stdout
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}], excludes=["path1"]
        )
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

        # Pass multiple exclusions.
        result = runner.invoke(
            deploy, ["--exclude", "path1", "-e", "path2", "main:app"]
        )
        assert result.exit_code == 0, result.stdout
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}], excludes=["path1", "path2"]
        )
        assert (
            fake_service_sdk.deployed_config.applications
            == expected_config.applications
        )

    def test_deploy_from_file_override_options(self, fake_service_sdk):
        runner = CliRunner()

        # No overrides, should match the config in the file.
        result = runner.invoke(deploy, ["-f", FULL_CONFIG_PATH])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="test-image",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override name.
        result = runner.invoke(
            deploy, ["-f", FULL_CONFIG_PATH, "--name", "override-name"]
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="override-name",
            image="test-image",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override image.
        result = runner.invoke(
            deploy, ["-f", FULL_CONFIG_PATH, "--image", "override-image"]
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="override-image",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override compute_config.
        result = runner.invoke(
            deploy,
            ["-f", FULL_CONFIG_PATH, "--compute-config", "override-compute-config"],
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="test-image",
            compute_config="override-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override working_dir.
        result = runner.invoke(
            deploy, ["-f", FULL_CONFIG_PATH, "--working-dir", "override-working-dir"]
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="test-image",
            compute_config="test-compute-config",
            working_dir="override-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override requirements.
        result = runner.invoke(
            deploy,
            ["-f", FULL_CONFIG_PATH, "--requirements", MULTI_LINE_REQUIREMENTS_PATH],
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="test-image",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=MULTI_LINE_REQUIREMENTS_PATH,
        )
        assert fake_service_sdk.deployed_config == expected_config
