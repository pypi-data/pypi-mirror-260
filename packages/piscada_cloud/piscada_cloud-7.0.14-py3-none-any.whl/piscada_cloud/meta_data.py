"""Functions related to the Cloud Meta Data API."""
import json
import os
from uuid import UUID

import requests

from piscada_cloud.mappings import Tag


def _check_credentials(host: str | None = None, token: str | None = None, env_var: str | None = None) -> tuple[str, str]:
    if isinstance(host, str) and isinstance(token, str):
        return host, token
    if (host is None and token is not None) or (host is not None and token is None):
        raise RuntimeError("Both `host` and `token` must be provided when used as parameters.")
    host = os.getenv(f"{env_var}_HOST")
    token = os.getenv(f"{env_var}_TOKEN")
    if not host or not token:
        raise RuntimeError(f"Both environment variables {env_var}_HOST and {env_var}_TOKEN need to be defined when host and token are not provided as parameters.")
    return host, token


def get_controllers(uuid: UUID | None = None, host: str | None = None, token: str | None = None) -> list[dict]:
    """Get list of accessible controllers.

    Parameters
    ----------
    uuid: UUID, optional
        UUID of a specific controller to get it's detail view.
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Returns
    -------
    list[dict]
        List of accessible controllers.

    Raises
    ------
    KeyError
        if user is not authorized to make tha specific request. Typically when requesting a detail view.
    RuntimeError
        If credentials are not provided or response status from Cloud Meta Data API is not 200.
    """
    host, token = _check_credentials(host, token, env_var="CLOUD_META_DATA")
    url = f"https://{host}/v0/controllers"
    if uuid is not None:
        url += f"/{uuid}"
    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code == 404:
        raise KeyError(f"{response.json()['detail']}")
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return response.json()


def get_tags(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None,
    name: str | None = None,
    path: str | None = None,
    uuid: UUID | None = None,
    host: str | None = None,
    token: str | None = None,
    controller_version: str | None = None,
) -> list[Tag]:
    """
    List accessible tags with optional filtering.

    If the controller version is not specified it is assumed to be a v4 controller.
    If the provided parameters does not match any tags on v4 controllers we check if
    the provided controller UUID belongs to a v4 controller. If it's not, we try the API
    for v3 controllers.
    If a controller UUID is not provided, we assume it's a v4 controller since the
    API for v3 controllers require the UUID to be specified.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    name: str | None
        Tag name
    path: str | None
        Tag path
    uuid: UUID | None
        Tag UUID
    host: str, optional
        Endpoint to send get request.
    token: str, optional
        Access token associated with the host.
    controller_version: str | None
        Version of the controller. Valid values: 'v3' or 'v4'. None if not provided.
    """
    if controller_version == "v4":
        return get_tags_ver4(controller_uuid, name, path, uuid, host, token)
    if controller_version == "v3":
        return get_tags_ver3(controller_uuid, host, token)

    tags = get_tags_ver4(controller_uuid, name, path, uuid, host, token)
    if tags or controller_uuid is None:
        return tags

    if controller_uuid is not None:
        try:
            get_controllers(uuid=controller_uuid)
        except KeyError:
            pass
        else:
            return tags

    return get_tags_ver3(controller_uuid, host, token)


def get_tags_ver4(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None, name: str | None = None, path: str | None = None, uuid: UUID | None = None, host: str | None = None, token: str | None = None
) -> list[Tag]:
    """List accessible tags from V4 controller with filtering.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    name: str | None
        Filter tags with a matching name pattern. E.g. `*RT40*`
    path: str | None
        Filter tags that start with the provided path. E.g. `/S1/`
    uuid: UUID | None
        Get tag with this UUID.
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Returns
    -------
    list[Tag]
        Tags matching provided filter

    Raises
    ------
    RuntimeError
        if Cloud Meta Data API does not respond with status 200
    """
    host, token = _check_credentials(host, token, env_var="CLOUD_META_DATA")
    if not (controller_uuid is None or isinstance(controller_uuid, UUID)):
        raise ValueError("controller_uuid must be of type UUID")
    if not (uuid is None or isinstance(uuid, UUID)):
        raise ValueError("uuid must be of type UUID")
    query_params = [f"{key}={value}" for key, value in {"controller-uuid": controller_uuid, "name": name, "path": path, "uuid": uuid}.items() if value is not None]
    url = f"https://{host}/v0/tags"
    if host == "localhost":
        url = f"http://{host}:8000/v0/tags"
    if len(query_params) > 0:
        url += "?" + "&".join(query_params)
    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    tags = []
    for meta_data in response.json():
        tags.append(
            Tag(
                controller_id=meta_data["controller-uuid"],
                uuid=meta_data["uuid"],
                name=meta_data["name"],
                path=meta_data["path"],
                active=None if meta_data.get("active") is None else int(meta_data["active"]),
                alarm_settings={} if meta_data.get("alarm_settings") is None else json.loads(meta_data["alarm-settings"]),
                data_access=meta_data.get("data-access"),
                data_properties={} if meta_data.get("data-properties") is None else json.loads(meta_data["data-properties"]),
                data_type=meta_data.get("data-type"),
                data_unit=meta_data.get("data-unit"),
                device_properties={} if meta_data.get("device-properties") is None else json.loads(meta_data["device-properties"]),
                device_type=meta_data.get("device-type"),
                description=meta_data.get("description"),
                legacy_type=meta_data.get("legacy-type"),
                optional_name=meta_data.get("optional-name"),
                runtime={} if meta_data.get("runtime") is None else json.loads(meta_data["runtime"]),
            )
        )
    return tags


def get_tags_ver3(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None,
    host: str | None = None,
    token: str | None = None,
) -> list[Tag]:
    """List accessible tags from V3 controller with filtering.

    Get tags from V3 controller.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['WRITEAPI_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['WRITEAPI_TOKEN'].

    Returns
    -------
    list[Tag]
        Tags matching provided filter

    Raises
    ------
    RuntimeError
        if Cloud Meta Data API does not respond with status 200
    """
    host, token = _check_credentials(host, token, env_var="WRITEAPI")
    url = f"https://{host}/v1/controllers/{controller_uuid}/tags"
    url += "?fields=description%2Cname%2Cid%2Ctype"

    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(10, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return [
        Tag(controller_id=controller_uuid, name=meta_data[1]["name"], uuid=meta_data[2].get("id"), data_type=meta_data[3].get("type"))  # type: ignore
        for meta_data in response.json()
    ]
