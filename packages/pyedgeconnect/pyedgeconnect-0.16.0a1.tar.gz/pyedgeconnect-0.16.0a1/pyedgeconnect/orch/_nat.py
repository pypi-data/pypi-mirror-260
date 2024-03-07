# MIT License
# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
#
# nat : Gets Appliance NAT configurations


def get_appliance_nat_config(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get Edge Connect appliance NAT configuration

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - nat
          - GET
          - /nat/{neId}?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary of NAT configuration details
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/nat?nePk={ne_id}&cached={cached}"
    else:
        path = f"/nat/{ne_id}?cached={cached}"

    return self._get(path)


def get_appliance_nat_pools(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get Edge Connect appliance NAT pools configuration

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - nat
          - GET
          - /nat/{neId}/natPools?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary of NAT configuration details
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/nat/natPools?nePk={ne_id}&cached={cached}"
    else:
        path = f"/nat/{ne_id}/natPools?cached={cached}"

    return self._get(path)


def get_appliance_nat_maps(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get Edge Connect appliance NAT maps configuration

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - nat
          - GET
          - /nat/{neId}/maps?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary of NAT configuration details
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/nat/maps?nePk={ne_id}&cached={cached}"
    else:
        path = f"/nat/{ne_id}/maps?cached={cached}"

    return self._get(path)
