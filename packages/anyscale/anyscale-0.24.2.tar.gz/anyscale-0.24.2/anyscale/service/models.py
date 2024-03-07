import copy
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import yaml


class ServiceConfig:
    def __init__(
        self,
        *,
        applications: List[Dict[str, Any]],
        name: Optional[str] = None,
        image: Optional[str] = None,
        compute_config: Optional[Union[Dict, str]] = None,
        working_dir: Optional[str] = None,
        excludes: Optional[List[str]] = None,
        requirements: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ):
        if len(kwargs) > 0:
            raise ValueError(f"Unrecognized options: {list(kwargs.keys())}.")

        if name is not None and not isinstance(name, str):
            raise TypeError("'name' must be a string.")

        if image is not None and not isinstance(image, str):
            raise TypeError("'image' must be a string.")

        if compute_config is not None and not isinstance(compute_config, (str, dict)):
            raise TypeError("'compute_config' must be a string or dictionary.")

        if working_dir is not None and not isinstance(working_dir, str):
            raise TypeError("'working_dir' must be a string.")

        if excludes is not None and (
            not isinstance(excludes, list)
            or not all(isinstance(e, str) for e in excludes)
        ):
            raise TypeError("'excludes' must be a list of strings.")

        if not isinstance(applications, list):
            raise TypeError("'applications' must be a list.")
        elif len(applications) == 0:
            raise ValueError("'applications' cannot be empty.")

        self._name = name
        self._image = image
        self._compute_config = compute_config
        self._applications = self._override_application_runtime_envs(
            applications=applications,
            working_dir=working_dir,
            excludes=excludes,
            requirements=requirements,
        )

        self._validate_import_paths(self._applications)

    def _validate_import_paths(self, applications: List[Dict[str, Any]]):
        for app in applications:
            import_path = app.get("import_path", None)
            if not import_path:
                raise ValueError("Every application must specify an import path.")

            if not isinstance(import_path, str):
                raise TypeError(f"'import_path' must be a string, got: {import_path}")

            if ":" in import_path:
                if import_path.count(":") > 1:
                    raise ValueError(
                        f"Got invalid import path '{import_path}'. An "
                        "import path may have at most one colon."
                    )
                if (
                    import_path.rfind(":") == 0
                    or import_path.rfind(":") == len(import_path) - 1
                ):
                    raise ValueError(
                        f"Got invalid import path '{import_path}'. An "
                        "import path may not start or end with a colon."
                    )
            else:
                if import_path.count(".") < 1:
                    raise ValueError(
                        f"Got invalid import path '{import_path}'. An "
                        "import path must contain at least one period or colon."
                    )
                if (
                    import_path.rfind(".") == 0
                    or import_path.rfind(".") == len(import_path) - 1
                ):
                    raise ValueError(
                        f"Got invalid import path '{import_path}'. An "
                        "import path may not start or end with a period."
                    )

    def _override_application_runtime_envs(
        self,
        applications: List[Dict[str, Any]],
        *,
        working_dir: Optional[str],
        excludes: Optional[List[str]],
        requirements: Union[None, str, List[str]],
    ) -> List[Dict[str, Any]]:
        """Override the runtime_env field of the provided applications.

        Fields that are modified:
            - 'working_dir' is overwritten with the passed working_dir.
            - 'pip' is overwritten with the passed requirements.
            - 'excludes' is extended with the passed excludes list.
        """
        applications = copy.deepcopy(applications)
        for application in applications:
            runtime_env = application.get("runtime_env", {})
            if working_dir is not None:
                runtime_env["working_dir"] = working_dir

            if excludes is not None:
                # Extend the list of excludes rather than overwriting it.
                runtime_env["excludes"] = runtime_env.get("excludes", []) + excludes

            if requirements is not None:
                runtime_env["pip"] = requirements

            if runtime_env:
                application["runtime_env"] = runtime_env

        return applications

    def to_dict(self) -> Dict[str, Any]:
        # TODO(edoakes): include cluster compute here.
        return {
            "name": self._name,
            "image": self._image,
            "compute_config": self._compute_config,
            "applications": self._applications,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(**d)

    @classmethod
    def from_yaml(cls, path: str):
        with open(path) as f:
            return cls.from_dict(yaml.safe_load(f))

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def image(self) -> Optional[str]:
        return self._image

    @property
    def compute_config(self) -> Optional[Union[str, Dict]]:
        return self._compute_config

    @property
    def applications(self) -> List[Dict[str, Any]]:
        return self._applications

    def options(  # noqa: PLR0913
        self,
        applications: Optional[List[Dict[str, Any]]] = None,
        name: Optional[str] = None,
        image: Optional[str] = None,
        compute_config: Optional[str] = None,
        working_dir: Optional[str] = None,
        excludes: Optional[List[str]] = None,
        requirements: Optional[Union[str, List[str]]] = None,
    ) -> "ServiceConfig":
        return ServiceConfig(
            applications=applications or self.applications,
            name=name or self.name,
            image=image or self.image,
            compute_config=compute_config or self.compute_config,
            working_dir=working_dir,
            excludes=excludes,
            requirements=requirements,
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceConfig):
            return all(
                [
                    self.name == other.name,
                    self.image == other.image,
                    self.compute_config == other.compute_config,
                    self.applications == other.applications,
                ]
            )

        return False

    def __str__(self) -> str:
        return str(self.to_dict())


class ServiceState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    # TODO(edoakes): UPDATING comes up while rolling out and rolling back.
    # This is very unexpected from a customer's point of view, we should fix it.
    UPDATING = "UPDATING"
    ROLLING_OUT = "ROLLING_OUT"
    ROLLING_BACK = "ROLLING_BACK"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    UNHEALTHY = "UNHEALTHY"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"

    def __str__(self):
        return self.name


# TODO(edoakes): we should have a corresponding ServiceVersionState.
class ServiceVersionStatus:
    def __init__(
        self, *, name: str, weight: int, config: Union[ServiceConfig, Dict],
    ):
        self._name: str = name
        self._weight: int = weight

        if isinstance(config, Dict):
            config = ServiceConfig(**config)

        self._config: ServiceConfig = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def config(self) -> ServiceConfig:
        return self._config

    def to_dict(self, *, exclude_details: bool = False) -> Dict[str, Any]:
        d = {
            "name": self._name,
            "weight": self._weight,
        }
        if not exclude_details:
            d["config"] = self._config.to_dict()

        return d

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceVersionStatus):
            return all(
                [
                    self.name == other.name,
                    self.weight == other.weight,
                    self.config == other.config,
                ]
            )

        return False

    def __repr__(self) -> str:
        return f"ServiceVersionStatus(name='{self._name}', weight='{self._weight}')"

    def __str__(self) -> str:
        return str(self.to_dict())


class ServiceStatus:
    def __init__(
        self,
        *,
        name: str,
        state: ServiceState,
        query_url: str,
        query_auth_token: Optional[str] = None,
        primary_version: Optional[Union[ServiceVersionStatus, Dict]] = None,
        canary_version: Optional[Union[ServiceVersionStatus, Dict]] = None,
    ):
        self._name: str = name
        self._state: ServiceState = ServiceState(state)
        self._query_url: str = query_url
        self._query_auth_token: Optional[str] = query_auth_token

        if isinstance(primary_version, dict):
            primary_version = ServiceVersionStatus(**primary_version)
        self._primary_version: Optional[ServiceVersionStatus] = primary_version

        if isinstance(canary_version, dict):
            canary_version = ServiceVersionStatus(**canary_version)
        self._canary_version: Optional[ServiceVersionStatus] = canary_version

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> ServiceState:
        return self._state

    @property
    def query_url(self) -> str:
        return self._query_url

    @property
    def query_auth_token(self) -> Optional[str]:
        return self._query_auth_token

    @property
    def primary_version(self) -> Optional[ServiceVersionStatus]:
        return self._primary_version

    @property
    def canary_version(self) -> Optional[ServiceVersionStatus]:
        return self._canary_version

    def to_dict(self, *, exclude_details: bool = False) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "name": self._name,
            "state": str(self._state),
            "query_url": self._query_url,
        }
        if self._query_auth_token is not None:
            d["query_auth_token"] = self._query_auth_token

        if self._primary_version is not None:
            d["primary_version"] = self._primary_version.to_dict(
                exclude_details=exclude_details
            )

        if self._canary_version is not None:
            d["canary_version"] = self._canary_version.to_dict(
                exclude_details=exclude_details
            )

        return d

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceStatus):
            return all(
                [
                    self.name == other.name,
                    self.state == other.state,
                    self.query_url == other.query_url,
                    self.query_auth_token == other.query_auth_token,
                    self.primary_version == other.primary_version,
                    self.canary_version == other.canary_version,
                ]
            )

        return False

    def __repr__(self) -> str:
        return f"ServiceStatus(name='{self._name}')"

    def __str__(self) -> str:
        return str(self.to_dict())
