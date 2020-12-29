from ansible.errors import AnsibleFilterError


def container2volumes(container, vol_type="all"):
    vol_types = ["generated", "persistent", "volatile"]
    catch_all_type = "all"
    if vol_type != catch_all_type and vol_type not in vol_types:
        raise AnsibleFilterError(
            f"container2volumes: {vol_type} is not in allowed volume types ('all', 'generated', 'persistent', 'volatile')"
        )

    return list(
        filter(
            lambda vol: vol_type == "all" or vol.get("type") == vol_type,
            container.get("volumes", {}).values(),
        )
    )


def containers2volumes(containers, vol_type="all"):
    vol_types = ["generated", "persistent", "volatile"]
    catch_all_type = "all"
    if vol_type != catch_all_type and vol_type not in vol_types:
        raise AnsibleFilterError(
            f"containers2volumes: {vol_type} is not in allowed volume types ('all', 'generated', 'persistent', 'volatile')"
        )
    return sum(
        (container2volumes(c, vol_type) for c in containers.values()), []
    )


class FilterModule(object):
    """Get volume information from a container or a container list."""

    def filters(self):
        return {
            "containers2volumes": containers2volumes,
            "container2volumes": container2volumes,
        }
