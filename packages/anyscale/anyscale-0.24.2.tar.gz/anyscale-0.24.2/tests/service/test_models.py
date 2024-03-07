from dataclasses import dataclass
import os
import re
from typing import Any, Dict, List, Optional

import pytest

from anyscale.service.models import (
    ServiceConfig,
    ServiceState,
    ServiceStatus,
    ServiceVersionStatus,
)


@dataclass
class ConfigFile:
    name: str
    expected_config: Optional[ServiceConfig] = None
    expected_error: Optional[str] = None

    def get_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "test_config_files", self.name)


TEST_CONFIG_FILES = [
    ConfigFile(
        "minimal.yaml",
        expected_config=ServiceConfig(applications=[{"import_path": "main:app"}]),
    ),
    ConfigFile(
        "full.yaml",
        expected_config=ServiceConfig(
            applications=[{"import_path": "main:app"}],
            name="test-name",
            image="test-image",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            excludes=["test"],
            requirements=["pip-install-test"],
        ),
    ),
    ConfigFile(
        "points_to_requirements_file.yaml",
        expected_config=ServiceConfig(
            applications=[{"import_path": "main:app"}],
            requirements="some_requirements_file.txt",
        ),
    ),
    ConfigFile(
        "unrecognized_option.yaml",
        expected_error=re.escape("Unrecognized options: ['bad_option']."),
    ),
    ConfigFile(
        "multiple_applications.yaml",
        expected_config=ServiceConfig(
            applications=[
                {
                    "name": "app1",
                    "import_path": "main:app1",
                    "runtime_env": {"env_vars": {"abc": "def"}},
                },
                {
                    "name": "app2",
                    "import_path": "main:app",
                    "arguments": {"abc": "def", "nested": {"key": "val"}},
                },
            ],
        ),
    ),
]


class TestServiceConfig:
    def test_empty_applications(self):
        with pytest.raises(ValueError, match="'applications' cannot be empty."):
            ServiceConfig(applications=[])

    def test_bad_applications_type(self):
        with pytest.raises(TypeError, match="'applications' must be a list."):
            ServiceConfig(applications={})

    def test_invalid_import_paths(self):
        with pytest.raises(TypeError, match="'import_path' must be a string"):
            ServiceConfig(applications=[{"import_path": 1}])

        with pytest.raises(ValueError, match="Got invalid import path 'hello'"):
            ServiceConfig(applications=[{"import_path": "hello"}])

        with pytest.raises(ValueError, match="Got invalid import path 'hello.'"):
            ServiceConfig(applications=[{"import_path": "hello."}])

        with pytest.raises(ValueError, match="Got invalid import path 'hello:'"):
            ServiceConfig(applications=[{"import_path": "hello:"}])

        with pytest.raises(ValueError, match="Got invalid import path ':hello'"):
            ServiceConfig(applications=[{"import_path": ":hello"}])

        with pytest.raises(ValueError, match="Got invalid import path '.hello'"):
            ServiceConfig(applications=[{"import_path": ".hello"}])

    def test_applications(self):
        applications = [
            {"import_path": "main:app"},
            {"import_path": "main:app", "name": "app2"},
        ]
        config = ServiceConfig(applications=applications)
        assert config.applications == applications

    def test_name(self):
        config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert config.name is None

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], name="my-custom-name"
        )
        assert config.name == "my-custom-name"

        with pytest.raises(TypeError, match="'name' must be a string"):
            ServiceConfig(applications=[{"import_path": "main:app"}], name=123)

    def test_image(self):
        config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert config.image is None

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}], image="my-custom-image:1"
        )
        assert config.image == "my-custom-image:1"

        with pytest.raises(TypeError, match="'image' must be a string"):
            ServiceConfig(applications=[{"import_path": "main:app"}], image=123)

    def test_compute_config(self):
        config = ServiceConfig(applications=[{"import_path": "main:app"}])
        assert config.compute_config is None

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            compute_config="my-custom-compute_config",
        )
        assert config.compute_config == "my-custom-compute_config"

        config = ServiceConfig(
            applications=[{"import_path": "main:app"}],
            compute_config={"test": "inlined"},
        )
        assert config.compute_config == {"test": "inlined"}

        with pytest.raises(
            TypeError, match="'compute_config' must be a string or dictionary."
        ):
            ServiceConfig(
                applications=[{"import_path": "main:app"}], compute_config=123
            )

    def test_options(self):
        config = ServiceConfig(applications=[{"import_path": "main:app"}])

        options = {
            "name": "test-name",
            "image": "test-image",
            "compute_config": "test-compute-config",
            "requirements": ["pip-install-test"],
            "working_dir": ".",
            "excludes": ["some-path"],
        }

        # Test setting fields one at a time.
        for option, val in options.items():
            assert config.options(**{option: val}) == ServiceConfig(
                applications=[{"import_path": "main:app"}], **{option: val}
            )

            assert config.options(**{option: val}) == ServiceConfig(
                applications=[{"import_path": "main:app"}], **{option: val}
            )

        # Test setting fields all at once.
        assert config.options(**options) == ServiceConfig(
            applications=[{"import_path": "main:app"}], **options
        )

    def test_working_dir_excludes_bad_types(self):
        with pytest.raises(TypeError, match="'working_dir' must be a string."):
            ServiceConfig(
                applications=[{"import_path": "main:app"}], working_dir=1,
            )

        with pytest.raises(TypeError, match="'excludes' must be a list of strings."):
            ServiceConfig(
                applications=[{"import_path": "main:app"}], excludes="hi",
            )

        with pytest.raises(TypeError, match="'excludes' must be a list of strings."):
            ServiceConfig(
                applications=[{"import_path": "main:app"}], excludes=["hi", 1],
            )

    @pytest.mark.parametrize(
        ("working_dir", "excludes"),
        [
            (None, None),
            (".", ["path1/", "path2"]),
            ("s3://path.zip", ["path1/", "path2"]),
        ],
    )
    def test_override_working_dir_excludes(
        self, working_dir: Optional[str], excludes: Optional[List[str]]
    ):
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
                    "excludes": ["something-else"],
                    "working_dir": "s3://somewhere.zip",
                    "env_vars": {"abc": "123"},
                },
            },
        ]

        config = ServiceConfig(
            applications=applications, working_dir=working_dir, excludes=excludes
        )

        if working_dir is None:
            assert excludes is None
            assert config.applications == applications
        else:
            assert isinstance(excludes, list)
            assert len(config.applications) == 3
            assert config.applications[0] == {
                "name": "no_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"working_dir": working_dir, "excludes": excludes},
            }

            assert config.applications[1] == {
                "name": "empty_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"working_dir": working_dir, "excludes": excludes},
            }
            assert config.applications[2] == {
                "name": "has_runtime_env",
                "import_path": "main:app",
                "runtime_env": {
                    "working_dir": working_dir,
                    # Existing `excludes` field should be extended.
                    "excludes": ["something-else", *excludes],
                    "env_vars": {"abc": "123"},
                },
            }

    @pytest.mark.parametrize("config_file", TEST_CONFIG_FILES)
    def test_from_config_file(self, config_file: ConfigFile):
        if config_file.expected_error is not None:
            with pytest.raises(Exception, match=config_file.expected_error):
                ServiceConfig.from_yaml(config_file.get_path())

            return

        assert config_file.expected_config == ServiceConfig.from_yaml(
            config_file.get_path()
        )


class TestServiceStatus:
    @pytest.mark.parametrize(
        "canary_version",
        [
            None,
            ServiceVersionStatus(
                name="test-canary-version",
                weight=0,
                config=ServiceConfig(
                    applications=[
                        {"import_path": "main:app", "arguments": {"version": "canary"}}
                    ],
                    image="test-image",
                    compute_config="test-compute-config",
                ),
            ),
        ],
    )
    @pytest.mark.parametrize(
        "primary_version",
        [
            None,
            ServiceVersionStatus(
                name="test-primary-version",
                weight=100,
                config=ServiceConfig(
                    applications=[
                        {"import_path": "main:app", "arguments": {"version": "primary"}}
                    ],
                    image="test-image",
                    compute_config="test-compute-config",
                ),
            ),
        ],
    )
    @pytest.mark.parametrize("query_auth_token", [None, "test_abc123"])
    @pytest.mark.parametrize("state", list(ServiceState))
    def test_to_dict_and_back(
        self,
        state: ServiceState,
        query_auth_token: Optional[str],
        primary_version: Optional[ServiceVersionStatus],
        canary_version: Optional[ServiceVersionStatus],
    ):
        """Test that all fields can be serialized to and from dictionaries."""
        status = ServiceStatus(
            name="test-service-name",
            state=state,
            query_url="http://test.com/",
            query_auth_token=query_auth_token,
            primary_version=primary_version,
            canary_version=canary_version,
        )

        status_dict = status.to_dict()
        assert ServiceStatus(**status_dict) == status

    def test_unknown_state(self):
        with pytest.raises(
            ValueError, match="'SOME_FAKE_NEWS_STATE' is not a valid ServiceState"
        ):
            ServiceStatus(
                name="test-service-name",
                state="SOME_FAKE_NEWS_STATE",
                query_url="http://test.com/",
                query_auth_token=None,
                primary_version=None,
                canary_version=None,
            )
