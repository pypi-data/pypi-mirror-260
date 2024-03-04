from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum


def _is_organic(cycle: dict):
    lookup = download_lookup('standardsLabels.csv', True)

    def term_organic(lookup, term_id: str):
        return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'

    practices = list(filter(lambda p: p.get('term') is not None, cycle.get('practices', [])))
    return any([term_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def _is_irrigated(cycle: dict):
    practice = find_term_match(cycle.get('practices', []), 'irrigated', None)
    return practice is not None and list_sum(practice.get('value', [100])) > 0
