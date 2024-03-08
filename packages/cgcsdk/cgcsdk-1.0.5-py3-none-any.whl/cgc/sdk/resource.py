import json as _json
import re
import cgc.sdk.exceptions as _exceptions
import cgc.utils.prepare_headers as _prepare_headers
import cgc.commands.compute.compute_utills as _compute_utills
import cgc.utils.requests_helper as _requests_helper
import cgc.utils.response_utils as _response_utils
from enum import Enum as _Enum
from cgc.commands.compute.compute_models import GPUsList


def start_function_loop(function, infinite: bool = True, *args, **kwargs):
    """
    Starts a function in a loop until it gets response code 200.

    Args:
        function: The function to be executed.
        infinite: A boolean indicating whether the loop should be infinite (default: True).
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Raises:
        _SDKException: If the app fails to start within 10 iterations (when infinite is False).

    Returns:
        None
    """
    from time import sleep

    counter = 0
    try:
        response = function(*args, **kwargs)
        if type(response) is bool:
            while not response:
                counter += 1
                if not infinite and counter > 10:
                    raise _exceptions.SDKException(-1, response)
                sleep(5)
                response = function(*args, **kwargs)
        elif type(response) is dict:
            while response["code"] != 200:
                counter += 1
                if not infinite and counter > 10:
                    raise _exceptions.SDKException(-1, response)
                sleep(5)
                response = function(*args, **kwargs)
        else:
            raise _exceptions.SDKException(-1, response)
    except _exceptions.SDKException as e:
        import logging

        if e.code == 409:
            logging.warning(e)
        else:
            raise e
    else:
        return response


def stop_function_loop(function, infinite: bool = True, *args, **kwargs):
    """
    Stop function loop, proceed on response code 200.

    Args:
        function: The function to be stopped.
        infinite (bool): Flag indicating whether the loop should run infinitely or not.
        *args: Variable length argument list to be passed to the function.
        **kwargs: Arbitrary keyword arguments to be passed to the function.

    Raises:
        _SDKException: If the app fails to stop within 10 attempts (when infinite is False).

    Returns:
        None
    """
    from time import sleep

    counter = 0
    response = function(*args, **kwargs)
    if type(response) is bool:
        while not response:
            counter += 1
            if not infinite and counter > 10:
                raise _exceptions.SDKException(-1, response)
            sleep(5)
            response = function(*args, **kwargs)
    elif type(response) is dict:
        while response["code"] != 200:
            counter += 1
            if not infinite and counter > 10:
                raise _exceptions.SDKException(-1, response)
            sleep(5)
            response = function(*args, **kwargs)
    else:
        raise _exceptions.SDKException(-1, response)
    return response


def compute_list():
    """
    List all compute apps for user namespace.
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/list?resource_type=compute"
    metric = "compute.list"
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.get,
        url=url,
        headers=headers,
    )
    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


class ResourceTypes(_Enum):
    compute = "compute"
    db = "db"


def _resource_status_ready(name: str, response: dict):
    """
    Check if a resource is ready.

    Args:
        name: The name of the resource.
        response: The response from the API call.

    Returns:
        The response from the API call.
    """
    for pod in response["details"]["pods_list"]:
        try:
            if pod["labels"]["app-name"] == name:
                return pod["status"] == "Running"
        except KeyError:
            return False
    return False


def resource_ready(
    name: str, resource_type: ResourceTypes = ResourceTypes.compute
) -> bool:
    """
    Check if a resource is ready.

    Args:
        name: The name of the resource.
        resource_type: The type of resource to check (default: ResourceTypes.compute).

    Returns:
        bool: A boolean indicating whether the resource is ready.
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/list?resource_type={resource_type.value}"
    metric = "resource.list"
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.get,
        url=url,
        headers=headers,
    )
    validated_response = (
        _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
            __res, metric
        )
    )
    return _resource_status_ready(name, validated_response)


def db_list():
    """
    List all db apps for user namespace.
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/list?resource_type=db"
    metric = "compute.list"
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.get,
        url=url,
        headers=headers,
    )
    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def compute_create_custom(
    name: str,
    image_name: str,
    cpu: int = 1,
    memory: int = 2,
    shm_size: int = 0,
    gpu: int = 0,
    gpu_type: str = "A5000",
    volumes: list = [],
    volume_full_path: str = "",
    startup_command: str = "",
    repository_secret: str = "",
    resource_data: list = [],
    config_maps_data: list = [],
    node_port_enabled: bool = False,
):
    """
    Create a custom compute resource.

    :param name: The name of the compute resource.
    :type name: str
    :param image_name: The name of the image to use for the compute resource.
    :type image_name: str,
    :param cpu: The number of CPUs for the compute resource, defaults to 1.
    :type cpu: int, optional
    :param memory: The amount of memory (in GB) for the compute resource, defaults to 2.
    :type memory: int, optional
    :param shm_size: The size of the shared memory (in GB) for the compute resource, defaults to 0.
    :type shm_size: int, optional
    :param gpu: The number of GPUs for the compute resource, defaults to 0.
    :type gpu: int, optional
    :param gpu_type: The type of GPU for the compute resource, defaults to "A5000".
    :type gpu_type: str, optional
    :param volumes: The list of volumes to attach to the compute resource, defaults to [].
    :type volumes: list, optional
    :param volume_full_path: The full path of the volume, defaults to "".
    :type volume_full_path: str, optional
    :param startup_command: The startup command for the compute resource, defaults to "".
    :type startup_command: str, optional
    :param repository_secret: The secret for accessing the repository, defaults to "".
    :type repository_secret: str, optional
    :param resource_data: The additional resource data, defaults to [].
    :type resource_data: list, optional
    :param config_maps_data: The additional config maps data, defaults to [].
    :type config_maps_data: list, optional
    :param node_port_enabled: A flag indicating whether the node port is enabled, defaults to False.
    :type node_port_enabled: bool, optional
    :raises _SDKException: If the image name is not provided.
    :raises _SDKException: If an invalid GPU type is specified.
    :return: The response from the API call.
    :rtype: _type_
    """
    if not image_name:
        raise _exceptions.SDKException(-2, "Image name is required")
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/create"
    metric = "compute.create"
    gpu_type = gpu_type.upper()
    if gpu_type not in GPUsList.get_list():
        raise _exceptions.SDKException(-3, f"Invalid GPU type: {gpu_type}")
    __payload = _compute_utills.compute_create_payload(
        name=name,
        entity="custom",
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        gpu_type=gpu_type,
        volumes=volumes,
        volume_full_path=volume_full_path,
        resource_data=resource_data,
        config_maps_data=config_maps_data,
        shm_size=shm_size,
        image_name=image_name,
        startup_command=startup_command,
        repository_secret=repository_secret,
        node_port_enabled=node_port_enabled,
    )

    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.post,
        url=url,
        headers=headers,
        data=_json.dumps(__payload),
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def resource_update_port(
    name: str, port_name: str, new_port: int, ingress: bool = True
):
    """
    Update a port for an app using backend endpoint.

    :param name: name of app to edit
    :type name: str
    :param port_name: name of port to edit
    :type port_name: str
    :param new_port: new port number
    :type new_port: int
    :return: response from the API call
    :rtype: dict
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/ports?port_modification_mode=UPDATE"
    metric = "resource.ports.update"
    __payload = _compute_utills.port_modification_payload(
        port_name=port_name,
        port_number=new_port,
        ingress=ingress,
        app_name=name,
    )
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.post,
        url=url,
        headers=headers,
        data=_json.dumps(__payload),
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def resource_add_port(name: str, port_name: str, new_port: int, ingress: bool = True):
    """
    Add a port for an app using backend endpoint.

    :param name: name of app to edit
    :type name: str
    :param port_name: name of port to add
    :type port_name: str
    :param new_port: new port number
    :type new_port: int
    :return: response from the API call
    :rtype: dict
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/ports?port_modification_mode=ADD"
    metric = "resource.ports.add"
    __payload = _compute_utills.port_modification_payload(
        port_name=port_name,
        port_number=new_port,
        ingress=ingress,
        app_name=name,
    )
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.post,
        url=url,
        headers=headers,
        data=_json.dumps(__payload),
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def resource_delete_port(
    name: str,
    port_name: str,
):
    """
    Add a port for an app using backend endpoint.

    :param name: name of app to edit
    :type name: str
    :param port_name: name of port to delete
    :type port_name: str
    :return: response from the API call
    :rtype: dict
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/ports?port_modification_mode=DELETE"
    metric = "resource.ports.delete"
    __payload = _compute_utills.port_delete_payload(
        port_name=port_name,
        app_name=name,
    )
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.post,
        url=url,
        headers=headers,
        data=_json.dumps(__payload),
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def resource_list_ports(name: str):
    """
    List ports for an app using backend endpoint.

    :param name: name of app to list ports for
    :type name: str
    :return: response from the API call
    :rtype: dict
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/ports?resource_name={name}"
    metric = "resource.ports.list"
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.get,
        url=url,
        headers=headers,
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )


def resource_delete(name: str):
    """
    Delete an app using backend endpoint.

    :param name: name of app to delete
    :type name: str
    :return: response from the API call
    :rtype: dict
    """
    api_url, headers = _prepare_headers.get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/delete"
    metric = "resource.delete"
    __payload = _compute_utills.compute_delete_payload(name=name)
    __res = _requests_helper.call_api(
        request=_requests_helper.EndpointTypes.delete,
        url=url,
        headers=headers,
        data=_json.dumps(__payload),
    )

    return _response_utils.retrieve_and_validate_response_send_metric_for_sdk(
        __res, metric
    )
