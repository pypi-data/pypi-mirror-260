from . import govc
from time import sleep


def get(name: str) -> bool:
    return govc.get("library.info -json /" + name)


def list() -> list:
    return govc.get("library.ls -json")


def create(datacenter_name: str, datastore_name: str, lib_name: str, wait: str = "1m"):
    if not get(lib_name):
        govc.get(
            f"library.create -json -ds=/{datacenter_name}/datastore/{datastore_name} {lib_name}",
            as_json=False,
            raise_on_failure=True,
        )
    if wait:
        _wait_for_lib_ready(lib_name, wait)
    return get(lib_name)


def _wait_for_lib_ready(name: str, timeout: str):
    # TODO
    sleep(1)


def _wait_for_lib_item_ready(lib_name: str, item_name: str, timeout: str):
    # TODO
    sleep(1)


def delete(name: str):
    return govc.run(f"library.rm {name}", raise_on_failure=True)


def get_item(library_name: str, item_name: str):
    ret = govc.get(f"library.ls -json /{library_name}/{item_name}")
    if not ret:
        return
    return ret[0]


def import_ovf(library_name: str, url: str, wait: str = "10m"):
    # govc library.ls -json /nanw-lib/edge-gw-2.3.0.0-20652183_OVF10
    # govc library.import -pull nanw-lib http://build-squid.eng.vmware.com/build/mts/release/bora-20652183/publish/edge-gw-2.3.0.0-20652183_OVF10.ovf

    name = get_ovf_name_from_url(url)
    if not get_item(library_name, name):
        govc.run(f"library.import -pull {library_name} {url}", raise_on_failure=True)
    if wait:
        _wait_for_lib_item_ready(library_name, name, wait)
    return get_item(library_name, name)


def get_ovf_name_from_url(url: str):
    # http://build-squid.eng.vmware.com/build/mts/release/bora-20652183/publish/edge-gw-2.3.0.0-20652183_OVF10.ovf
    if not url.endswith(".ovf"):
        raise Exception("Invalid URL: URL does not end with '.ovf'.")
    return url[url.rfind("/") + 1 : len(url) - 4]
