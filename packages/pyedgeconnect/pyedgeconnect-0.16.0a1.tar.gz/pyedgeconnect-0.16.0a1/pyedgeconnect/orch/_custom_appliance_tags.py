# MIT License
# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
#
# customApplianceTags : Custom Appliance Tags


def get_custom_appliance_tags(
    self,
    ne_id: str,
    cached: bool,
) -> dict:
    """Get user-defined appliance tags

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - customApplianceTags
          - GET
          - /customApplianceTags/{neId}?cached={cached}

    :param ne_id: Network Primary Key (nePk) of existing appliance,
        e.g. ``3.NE``
    :type ne_id: str
    :param cached: ``True`` retrieves last known value to Orchestrator,
        ``False`` retrieves values directly from Appliance
    :type cached: bool
    :return: Returns user-defined appliance tags
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/customApplianceTags?nePk={ne_id}&cached={cached}"
    else:
        path = f"/customApplianceTags/{ne_id}?cached={cached}"

    return self._get(path)
