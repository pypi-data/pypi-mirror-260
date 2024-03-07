# MIT License
# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
#
# natPolicy : ECOS SaaS NAT policies


def get_nat_policy(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get NAT policy configurations from Edge Connect appliance

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - natPolicy
          - GET
          - /natMaps/{neId}?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary where each key is a segment id that
        contains its associated DNS proxy configuration (profiles,
        domain groups and maps).
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/natMaps?nePk={ne_id}&cached={cached}"
    else:
        path = f"/natMaps/{ne_id}?cached={cached}"

    return self._get(path)


def get_nat_policy_inbound_outbound(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get all NAT inbound/ountboud settings from Edge Connect appliance

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - natPolicy
          - GET
          - /natAll/{neId}?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary where each key is a segment id that
        contains its associated DNS proxy configuration (profiles,
        domain groups and maps).
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/natAll?nePk={ne_id}&cached={cached}"
    else:
        path = f"/natAll/{ne_id}?cached={cached}"

    return self._get(path)


def get_nat_policy_dynamic(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get all NAT dynamic rules settings from Edge Connect appliance

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - natPolicy
          - GET
          - /natMapsDynamic/{neId}?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary where each key is a segment id that
        contains its associated DNS proxy configuration (profiles,
        domain groups and maps).
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/natMapsDynamic?nePk={ne_id}&cached={cached}"
    else:
        path = f"/natMapsDynamic/{ne_id}?cached={cached}"

    return self._get(path)
