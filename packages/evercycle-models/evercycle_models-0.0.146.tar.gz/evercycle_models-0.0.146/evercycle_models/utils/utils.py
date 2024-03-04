import logging

from typing import List, Union, Any, Callable

from evercycle_models.utils.graphene_inputs import AddressInput
from smartystreets_python_sdk import StaticCredentials, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

from evercycle_models.models import Organization

logger = logging.getLogger(__name__)


def get_sub_orgs(
    organization: Organization,
    organizations_list: List[Union[Organization, Any]] = None,
    map_data_for_list: Callable[[Organization], List[Union[Organization, Any]]] = None
):
    if organizations_list is None:
        organizations_list = []

    if map_data_for_list is not None:
        organizations_list.extend(map_data_for_list(organization))
    else:
        organizations_list.append(organization)

    sub_organizations = organization.sub_organizations.all()

    for sub_organization in sub_organizations:
        get_sub_orgs(
            organization=sub_organization,
            organizations_list=organizations_list,
            map_data_for_list=map_data_for_list
        )

    return organizations_list


auth_id = 'e06de302-9cb3-038a-d3a5-5f702e85f65c'
auth_token = '3fMLafl7uCzKwa4K9Yse'
credentials = StaticCredentials(auth_id, auth_token)

client = ClientBuilder(credentials).with_licenses(["us-core-cloud"]).build_us_street_api_client()


def address_is_valid(address: AddressInput) -> (bool, str):
    lookup = Lookup()
    lookup.street = address.street
    lookup.secondary = address.secondary
    lookup.city = address.city
    lookup.state = address.state
    lookup.zipcode = address.postal_code

    client.send_lookup(lookup)
    result = lookup.result

    if result and len(result) > 0:
        first_candidate = result[0]

        unique_key = (f"{first_candidate.components.primary_number}-{first_candidate.components.street_name}-"
                      f"{first_candidate.components.city_name}-{first_candidate.components.state_abbreviation}-"
                      f"{first_candidate.components.zipcode}")
        logger.info(f"Unique Key: {unique_key}")

        return True, unique_key
    else:
        logger.warning("Address validation failed or returned no results.")
        return False, None
