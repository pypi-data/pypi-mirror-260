import copy
from typing import Dict, List, Optional, Union

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    ComputeTemplateConfig,
    DecoratedComputeTemplateConfig,
)
from anyscale.sdk.anyscale_client.models import (
    ApplyServiceModel,
    ProductionServiceV2VersionModel,
    ServiceEventCurrentState,
    ServiceModel,
)
from anyscale.service._private.anyscale_client import (
    AnyscaleClientWrapper,
    RealAnyscaleClient,
    WORKSPACE_CLUSTER_NAME_PREFIX,
)
from anyscale.service.models import (
    ServiceConfig,
    ServiceState,
    ServiceStatus,
    ServiceVersionStatus,
)
from anyscale.utils.runtime_env import is_dir_remote_uri, parse_requirements_file
from anyscale.utils.workspace_notification import (
    WorkspaceNotification,
    WorkspaceNotificationAction,
)


logger = BlockLogger()


class ServiceSDK:
    def __init__(self, *, client: Optional[AnyscaleClientWrapper] = None):
        self._client = client or RealAnyscaleClient()

    def _override_and_load_requirements_files(
        self, config: ServiceConfig, *, autopopulate_in_workspace: bool = True
    ) -> ServiceConfig:
        """Replaces any pip fields in runtime_envs with their parsed file contents.

        If autopopulate_from_workspace is passed and this code is running inside a
        workspace, any applications that do not have a "pip" or "conda" field
        specified in the runtime_env will have it autopopulated with the
        workspace-tracked dependencies.
        """
        new_applications = copy.deepcopy(config.applications)

        local_path_to_parsed_requirements: Dict[str, List[str]] = {}

        def _load_requirements_file_memoized(
            target: Union[str, List[str]]
        ) -> List[str]:
            if isinstance(target, list):
                return target
            elif target in local_path_to_parsed_requirements:
                return local_path_to_parsed_requirements[target]
            elif isinstance(target, str):
                parsed_requirements = parse_requirements_file(target)
                if parsed_requirements is None:
                    raise FileNotFoundError(
                        f"Requirements file {target} does not exist."
                    )
                local_path_to_parsed_requirements[target] = parsed_requirements
                return parsed_requirements
            else:
                raise TypeError("pip field in runtime_env must be a list or string.")

            return parsed_requirements

        for application in new_applications:
            runtime_env = application.get("runtime_env", {})
            if "pip" in runtime_env:
                # Allow `None` to be used as a signal not to override.
                if runtime_env["pip"] is not None:
                    # If the user passed a "pip" field, load from the file if necessary.
                    runtime_env["pip"] = _load_requirements_file_memoized(
                        runtime_env["pip"]
                    )
            elif (
                "conda" not in runtime_env
                and autopopulate_in_workspace
                and self._client.inside_workspace()
            ):
                # If no "pip" or "conda" field was specified, try filling it in from
                # the workspace-tracked requirements file.
                workspace_requirements_path = (
                    self._client.get_workspace_requirements_path()
                )
                if workspace_requirements_path is not None:
                    logger.info("Including workspace-managed pip dependencies.")
                    runtime_env["pip"] = _load_requirements_file_memoized(
                        self._client.get_workspace_requirements_path()
                    )

        return config.options(applications=new_applications)

    def _override_and_upload_local_dirs(
        self,
        config: ServiceConfig,
        *,
        autopopulate_in_workspace: bool = True,
        cloud_id: Optional[str] = None,
    ) -> ServiceConfig:
        """Returns a copy of the config with all local dirs converted to remote URIs.

        Local dirs can be specified in the working_dir or py_modules fields of the runtime_env.

        Each unique local directory across these fields will be uploaded once to cloud storage,
        then all occurrences of it in the config will be replaced with the corresponding remote URI.
        """
        new_applications = copy.deepcopy(config.applications)

        local_path_to_uri: Dict[str, str] = {}

        def _upload_dir_memoized(target: str, *, excludes: Optional[List[str]]) -> str:
            if is_dir_remote_uri(target):
                return target
            if target in local_path_to_uri:
                return local_path_to_uri[target]

            logger.info(f"Uploading local dir '{target}' to cloud storage.")
            uri = self._client.upload_local_dir_to_cloud_storage(
                target, cloud_id=cloud_id, excludes=excludes,
            )
            local_path_to_uri[target] = uri
            return uri

        for application in new_applications:
            runtime_env = application.get("runtime_env", {})
            excludes = runtime_env.pop("excludes", None)
            if "working_dir" in runtime_env:
                # Allow `None` to be used as a signal not to override.
                if runtime_env["working_dir"] is not None:
                    runtime_env["working_dir"] = _upload_dir_memoized(
                        runtime_env["working_dir"], excludes=excludes
                    )
            elif autopopulate_in_workspace and self._client.inside_workspace():
                runtime_env["working_dir"] = _upload_dir_memoized(
                    ".", excludes=excludes,
                )

            py_modules = runtime_env.get("py_modules", None)
            if py_modules is not None:
                new_py_modules = []
                for py_module in py_modules:
                    new_py_modules.append(
                        _upload_dir_memoized(py_module, excludes=excludes)
                    )

                application["runtime_env"]["py_modules"] = new_py_modules

            if runtime_env:
                application["runtime_env"] = runtime_env

        return config.options(applications=new_applications)

    def _resolve_compute_config_to_id(
        self, compute_config: Optional[Union[str, Dict]]
    ) -> str:
        if compute_config is None:
            compute_config_id = self._client.get_compute_config_id()
            assert compute_config_id is not None
        elif isinstance(compute_config, str):
            compute_config_id = self._client.get_compute_config_id(
                compute_config_name=compute_config,
            )
            if compute_config_id is None:
                raise ValueError(
                    f"The compute config '{compute_config}' does not exist."
                )
        else:
            try:
                compute_config_template = ComputeTemplateConfig(**compute_config)
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid compute config: {e}.")

            compute_config_id = self._client.create_anonymous_compute_config(
                compute_config_template
            )

        return compute_config_id

    def _get_default_name(self) -> Optional[str]:
        """Get a default name for the service.

        A default is currently only generated when running inside a workspace
        (from the workspace cluster name), so this function errors if called outside
        a workspace.
        """
        if not self._client.inside_workspace():
            raise ValueError(
                "A service name must be provided when running outside of a workspace."
            )

        name = self._client.get_current_workspace_cluster().name
        # Defensively default to the workspace cluster name as-is if it doesn't
        # start with the expected prefix.
        if name.startswith(WORKSPACE_CLUSTER_NAME_PREFIX):
            name = name[len(WORKSPACE_CLUSTER_NAME_PREFIX) :]

        logger.info(f"No name was specified, using default: '{name}'.")
        return name

    def deploy(
        self,
        config: ServiceConfig,
        *,
        in_place: bool = False,
        canary_percent: Optional[int] = None,
        max_surge_percent: Optional[int] = None,
    ):
        if not isinstance(in_place, bool):
            raise TypeError("in_place must be a bool.")

        if canary_percent is not None:
            if not isinstance(canary_percent, int):
                raise TypeError("canary_percent must be an int.")
            if canary_percent < 0 or canary_percent > 100:
                raise ValueError("canary_percent must be between 0 and 100.")

        if max_surge_percent is not None:
            if not isinstance(max_surge_percent, int):
                raise TypeError("max_surge_percent must be an int.")

            if max_surge_percent < 0 or max_surge_percent > 100:
                raise ValueError("max_surge_percent must be between 0 and 100.")

        name = config.name or self._get_default_name()
        build_id = self._client.get_cluster_env_build_id(cluster_env_name=config.image,)
        if build_id is None:
            raise ValueError(f"The image '{config.image}' does not exist.")

        compute_config_id = self._resolve_compute_config_to_id(config.compute_config)

        # If a compute config was specified, we need to make sure to used the correct
        # cloud_id when uploading local directories.
        cloud_id = self._client.get_cloud_id(
            compute_config_id=None
            if config.compute_config is None
            else compute_config_id
        )
        config = self._override_and_upload_local_dirs(config, cloud_id=cloud_id)
        config = self._override_and_load_requirements_files(config)

        service: ServiceModel = self._client.roll_out_service(
            ApplyServiceModel(
                name=name,
                project_id=self._client.get_project_id(),
                # TODO(edoakes): if this logic gets more complex, move this to a
                # utility method and test it.
                ray_serve_config={"applications": config.applications},
                build_id=build_id,
                compute_config_id=compute_config_id,
                canary_percent=canary_percent,
                max_surge_percent=max_surge_percent,
                rollout_strategy="IN_PLACE" if in_place else "ROLLOUT",
            )
        )

        canary_percent_info = (
            ""
            if canary_percent is None
            else f" (target canary percent: {canary_percent})"
        )
        message = f"Service '{name}' deployed{canary_percent_info}."
        logger.info(message)
        if self._client.inside_workspace():
            self._client.send_workspace_notification(
                WorkspaceNotification(
                    body=message,
                    action=WorkspaceNotificationAction(
                        type="navigate-service", title="View Service", value=service.id,
                    ),
                ),
            )
        else:
            # NOTE(edoakes): this link does not currently work for AIOA clouds.
            logger.info(
                f"View the service in the UI: {self._client.get_service_ui_url(service.id)}"
            )

        logger.info(
            "Query the service once it's running using the following curl command:"
        )
        logger.info(
            f"curl -H 'Authorization: Bearer {service.auth_token}' {service.base_url}/"
        )

    def _strip_none_values_from_dict(self, d: Dict) -> Dict:
        """Return a copy of the dictionary without any keys whose values are None.

        Recursively calls into any dictionary values.
        """
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = self._strip_none_values_from_dict(v)
            elif v is not None:
                result[k] = v

        return result

    def _get_compute_config_for_status(
        self, compute_config_id: str,
    ) -> Union[str, Dict]:
        """Get the compute config to be displayed in the status for this ID.

        If the compute config refers to an anonymous compute config, its config
        will be returned. Else the name of the compute config will be returned.
        """
        compute_config = self._client.get_compute_config(compute_config_id)
        if compute_config is None:
            raise RuntimeError(
                f"Failed to get compute config for ID {compute_config_id}."
            )

        if not compute_config.anonymous:
            return compute_config.name

        config: DecoratedComputeTemplateConfig = compute_config.config
        config_dict = {
            # Strip some internal fields that we don't want to expose to the user.
            # TODO(edoakes): we should improve the compute config model and avoid this.
            k: v
            for k, v in config.to_dict().items()
            if k
            not in {
                "cloud",
                "cloud_id",
                "maximum_uptime_minutes",
                "idle_termination_minutes",
            }
        }
        return self._strip_none_values_from_dict(config_dict)

    def _service_version_model_to_status(
        self, model: ProductionServiceV2VersionModel, *, service_name: str,
    ) -> ServiceVersionStatus:
        cluster_env_name = self._client.get_cluster_env_name(model.build_id)
        if cluster_env_name is None:
            raise RuntimeError(
                f"Failed to get cluster env name for ID {model.build_id}."
            )

        return ServiceVersionStatus(
            name=model.version,
            # NOTE(edoakes): there is also a "current_weight" field but it does not match the UI.
            weight=model.weight,
            config=ServiceConfig(
                name=service_name,
                applications=model.ray_serve_config["applications"],
                image=cluster_env_name,
                compute_config=self._get_compute_config_for_status(
                    model.compute_config_id
                ),
            ),
        )

    def _service_model_to_status(self, model: ServiceModel) -> ServiceStatus:
        # TODO(edoakes): for some reason the primary_version is populated
        # when the service is terminated. This should be fixed in the backend.
        is_terminated = model.current_state == ServiceEventCurrentState.TERMINATED

        primary_version = None
        if not is_terminated and model.primary_version is not None:
            primary_version = self._service_version_model_to_status(
                model.primary_version, service_name=model.name,
            )

        canary_version = None
        if not is_terminated and model.canary_version is not None:
            canary_version = self._service_version_model_to_status(
                model.canary_version, service_name=model.name,
            )

        # If we add a new state to the backend, old clients may not recognize it.
        # Rather than erroring out and causing old code to crash, return UNKNOWN.
        try:
            state = ServiceState(model.current_state)
        except ValueError:
            state = ServiceState.UNKNOWN
            logger.warning(
                f"Got unrecognized state: '{model.current_state}'. "
                "You likely need to update the 'anyscale' package. "
                "If you still see this message after upgrading, contact Anyscale support."
            )

        return ServiceStatus(
            name=model.name,
            state=state,
            query_url=model.base_url,
            query_auth_token=model.auth_token,
            primary_version=primary_version,
            canary_version=canary_version,
        )

    def status(self, name: Optional[str] = None) -> ServiceStatus:
        if name is None:
            name = self._get_default_name()

        model: Optional[ServiceModel] = self._client.get_service(name)
        if model is None:
            raise RuntimeError(f"Service with name '{name}' was not found.")

        return self._service_model_to_status(model)
