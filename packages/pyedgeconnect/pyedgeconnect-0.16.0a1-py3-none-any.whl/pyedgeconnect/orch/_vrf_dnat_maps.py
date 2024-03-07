# MIT License
# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
#
# vrfDnatMaps : Inter-Segment D-NAT Rule


def get_dnat_maps(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get VRF DNAT Map defined on appliance

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - vrfDnatMaps
          - GET
          - /dnatMaps/{neId}?cached={cached}

    :param ne_id: Appliance id in the format of integer.NE e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns dictionary of DNAT maps
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/dnatMaps?nePk={ne_id}&cached={cached}"
    else:
        path = f"/dnatMaps/{ne_id}?cached={cached}"

    return self._get(path)
