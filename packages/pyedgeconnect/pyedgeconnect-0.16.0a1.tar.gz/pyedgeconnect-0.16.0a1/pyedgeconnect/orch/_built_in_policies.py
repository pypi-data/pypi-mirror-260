# MIT License
# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
#
# builtInPolicies : GET built-in policy information


def get_built_in_policies(
    self,
    ne_pk: str,
) -> dict:
    """
    Get built-in policy information from appliance

    .. list-table::
        :header-rows: 1

        * - Swagger Section
          - Method
          - Endpoint
        * - builtInPolicies
          - GET
          - /saMap/{nePk}

    :param ne_pk: Network Primary Key (nePk) of existing appliance,
        e.g. ``3.NE``
    :type ne_pk: str
    :return: Returns appliance policy information
    :rtype: dict
    """
    if self.orch_version >= 9.3:
        path = f"/saMap?nePk={ne_pk}"
    else:
        path = f"/saMap/{ne_pk}"

    return self._get(path)
