# © Copyright 2023-2024 Hewlett Packard Enterprise Development LP
from argparse import Namespace
from typing import Any, Dict, List, Optional

import aiolirest
from aioli import cli
from aioli.cli import render
from aioli.common import api
from aioli.common.api import authentication
from aioli.common.api.errors import NotFoundException
from aioli.common.declarative_argparse import Arg, ArgsDescription, Cmd
from aiolirest.models.autoscaling import Autoscaling
from aiolirest.models.configuration_resources import ConfigurationResources
from aiolirest.models.resource_profile import ResourceProfile
from aiolirest.models.service import Service
from aiolirest.models.service_model_version import ServiceModelVersion
from aiolirest.models.service_request import ServiceRequest


@authentication.required
def list_services(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)
        response = api_instance.services_get()

    def format_service(e: Service, models_api: aiolirest.ModelsApi) -> List[Any]:
        model = models_api.models_id_get(e.model)

        auto_scaling = e.auto_scaling
        if auto_scaling is None:
            auto_scaling = Autoscaling()

        resources = e.resources
        if resources is None:
            resources = ConfigurationResources()

        requests = resources.requests
        if requests is None:
            requests = ResourceProfile()

        limits = resources.limits
        if limits is None:
            limits = ResourceProfile()

        result = [
            e.name,
            e.description,
            model.name,
            auto_scaling.min_replicas,
            auto_scaling.max_replicas,
            auto_scaling.metric,
            auto_scaling.target,
            requests.cpu,
            requests.memory,
            requests.gpu,
            limits.cpu,
            limits.memory,
            limits.gpu,
            resources.gpu_type,
            e.canary_traffic_percent,
            format_environment(e.environment),
            format_arguments(e.arguments),
        ]
        return result

    headers = [
        "Name",
        "Description",
        "Model",
        "Min\nReplicas",
        "Max\nReplicas",
        "Metric",
        "Target",
        "Request\nCPU",
        "Request\nMem",
        "Request\nGPU",
        "Limit\nCPU",
        "Limit\nMem",
        "Limit\nGPU",
        "GPU\nType",
        "Canary\nTraffic\nPercent",
        "Environment",
        "Arguments",
    ]

    models_api = aiolirest.ModelsApi(session)
    values = [format_service(r, models_api) for r in response]
    render.tabulate_or_csv(headers, values, args.csv)


# format_environment formats the given environment for display . Presently it returns
# the environment as a comma-separated list name=value pairs.
def format_environment(env: Optional[Dict[str, str]]) -> str:
    if env is None:
        return ""
    formatted_variables: List[str] = []
    for key in env.keys():
        formatted_variables.append(f"{key}={env[key]}")
    return ",".join(formatted_variables)


def format_arguments(args: Optional[List[str]]) -> str:
    if args is None:
        return ""
    return " ".join(args)


@authentication.required
def create(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)

        auto = Autoscaling(
            metric=args.autoscaling_metric,
        )

        if args.autoscaling_target is not None:
            auto.target = args.autoscaling_target

        if args.autoscaling_max_replicas is not None:
            auto.max_replicas = args.autoscaling_max_replicas

        if args.autoscaling_min_replicas is not None:
            auto.min_replicas = args.autoscaling_min_replicas

        requests = ResourceProfile(
            cpu=args.requests_cpu, gpu=args.requests_gpu, memory=args.requests_memory
        )
        limits = ResourceProfile(
            cpu=args.limits_cpu, gpu=args.limits_gpu, memory=args.limits_memory
        )

        resources = ConfigurationResources(gpuType=args.gpu_type, requests=requests, limits=limits)

        r = ServiceRequest(
            arguments=construct_arguments(args),
            name=args.name,
            description=args.description,
            environment=construct_environment(args),
            model=args.model,
            autoScaling=auto,
            resources=resources,
            canaryTrafficPercent=args.canary_traffic_percent,
        )
        api_instance.services_post(r)


def construct_arguments(args: Namespace) -> List[str]:
    arguments: List[str] = []
    if args.arg is None:
        return arguments

    for entry in args.arg:
        arguments.append(entry.strip())
    return arguments


def construct_environment(args: Namespace) -> Dict[str, str]:
    environment: Dict[str, str] = {}
    if args.env is None:
        return environment

    for entry in args.env:
        # split to name & value
        the_split = entry.split("=", maxsplit=1)
        name: str = the_split[0]
        value: str = ""
        if len(the_split) > 1:
            value = the_split[1]
        environment[name] = value
    return environment


def lookup_service(name: str, api: aiolirest.ServicesApi) -> Service:
    for r in api.services_get():
        if r.name == name:
            return r
    raise NotFoundException(f"service {name} not found")


@authentication.required
def update(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)
        found = lookup_service(args.servicename, api_instance)
        request = ServiceRequest(
            arguments=found.arguments,
            autoScaling=found.auto_scaling,
            canaryTrafficPercent=found.canary_traffic_percent,
            description=found.description,
            environment=found.environment,
            model=found.model,
            name=found.name,
            resources=found.resources,
        )

        if (
            request.resources is None
            or request.auto_scaling is None
            or request.resources.requests is None
            or request.resources.limits is None
        ):
            # Not likely, but testing these prevents complaints from mypy
            raise api.errors.BadResponseException("Unexpected null result")

        if args.name is not None:
            request.name = args.name

        if args.description is not None:
            request.description = args.description

        if args.model is not None:
            request.model = args.model

        if args.autoscaling_min_replicas is not None:
            request.auto_scaling.min_replicas = args.autoscaling_min_replicas

        if args.autoscaling_max_replicas is not None:
            request.auto_scaling.max_replicas = args.autoscaling_max_replicas

        if args.autoscaling_metric is not None:
            request.auto_scaling.metric = args.autoscaling_metric

        if args.autoscaling_target is not None:
            request.auto_scaling.target = args.autoscaling_target

        if args.requests_cpu is not None:
            request.resources.requests.cpu = args.requests_cpu

        if args.requests_memory is not None:
            request.resources.requests.memory = args.requests_memory

        if args.requests_gpu is not None:
            request.resources.requests.gpu = args.requests_gpu

        if args.limits_cpu is not None:
            request.resources.limits.cpu = args.limits_cpu

        if args.limits_memory is not None:
            request.resources.limits.memory = args.limits_memory

        if args.limits_gpu is not None:
            request.resources.limits.gpu = args.limits_gpu

        if args.gpu_type is not None:
            request.resources.gpu_type = args.gpu_type

        if args.canary_traffic_percent is not None:
            request.canary_traffic_percent = args.canary_traffic_percent

        if args.env is not None:
            request.environment = construct_environment(args)

        if args.arg is not None:
            request.arguments = construct_arguments(args)

        headers = {"Content-Type": "application/json"}
        api_instance.services_id_put(found.id, request, _headers=headers)


@authentication.required
def delete_service(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)
        found = lookup_service(args.name, api_instance)
        assert found.id is not None
        api_instance.services_id_delete(found.id)


@authentication.required
def list_versions(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)
        found = lookup_service(args.name, api_instance)
        assert found.id is not None
        response = api_instance.services_id_versions_get(found.id)

    def format_versions(e: ServiceModelVersion) -> List[Any]:
        result = [
            e.deployed,
            e.native_app_name,
            e.model,
            e.mdl_version,
            e.canary_traffic_percent,
        ]
        return result

    headers = [
        "Deployed",
        "Native App Name",
        "Model",
        "Model\nVersion",
        "Canary\nTraffic\nPercent",
    ]

    values = [format_versions(r) for r in response]
    render.tabulate_or_csv(headers, values, args.csv)


@authentication.required
def auth_token(args: Namespace) -> None:
    with cli.setup_session(args) as session:
        api_instance = aiolirest.ServicesApi(session)
        found = lookup_service(args.name, api_instance)
        assert found.id is not None
        response = api_instance.services_id_token_get(found.id)

    t = response.to_dict()
    print(render.format_object_as_yaml(t))


common_service_args: ArgsDescription = [
    Arg(
        "-a",
        "--arg",
        help="Argument to be added to the service command line. "
        "If specifying an argument that starts with a '-', use the form --arg=<your-argument>",
        action="append",
    ),
    Arg("--autoscaling-min-replicas", help="Minimum number of replicas", type=int),
    Arg(
        "--autoscaling-max-replicas",
        help="Maximum number of replicas created based upon demand",
        type=int,
    ),
    Arg("--autoscaling-metric", help="Metric name which controls autoscaling"),
    Arg("--autoscaling-target", help="Metric target value", type=int),
    Arg(
        "--canary-traffic-percent",
        help="Percent traffic to pass to new model version",
        type=int,
        default=100,
    ),
    Arg("--description", help="Description of the service"),
    Arg(
        "-e",
        "--env",
        help="Specifies an environment variable & value as name=value, "
        "to be passed to the launched container",
        action="append",
    ),
    Arg("--gpu-type", help="GPU type required"),
    Arg("--limits-cpu", help="CPU limit"),
    Arg("--limits-memory", help="Memory limit"),
    Arg("--limits-gpu", help="GPU limit"),
    Arg("--requests-cpu", help="CPU request"),
    Arg("--requests-memory", help="Memory request"),
    Arg("--requests-gpu", help="GPU request"),
]

main_cmd = Cmd(
    "s|ervice",
    None,
    "manage inference services",
    [
        # Inspection commands.
        Cmd(
            "list ls",
            list_services,
            "list services",
            [
                Arg("--csv", action="store_true", help="print as CSV"),
            ],
            is_default=True,
        ),
        # Create command.
        Cmd(
            "create",
            create,
            "create a service",
            [
                Arg(
                    "name",
                    help="The name of the service. Must begin with a letter, but may contain "
                    "letters, numbers, underscore, and hyphen",
                ),
                Arg("--model", help="Model to be deployed", required="true"),
            ]
            + common_service_args,
        ),
        Cmd(
            "update",
            update,
            "modify a service",
            [
                Arg("servicename", help="The name of the service"),
                Arg(
                    "--name",
                    help="The new name of the service. Must begin with a letter, but may contain "
                    "letters, numbers, underscore, and hyphen",
                ),
                Arg("--model", help="Model to be deployed"),
            ]
            + common_service_args,
        ),
        Cmd(
            "delete",
            delete_service,
            "delete a service",
            [
                Arg("name", help="The name of the service"),
            ],
        ),
        Cmd(
            "versions lv",
            list_versions,
            "list model versions for a service",
            [
                Arg("--csv", action="store_true", help="print as CSV"),
                Arg("name", help="The name of the service"),
            ],
        ),
        Cmd(
            "token",
            auth_token,
            "get service auth token",
            [
                Arg("name", help="The name of the service"),
            ],
        ),
    ],
)


args_description = [main_cmd]  # type: List[Any]
