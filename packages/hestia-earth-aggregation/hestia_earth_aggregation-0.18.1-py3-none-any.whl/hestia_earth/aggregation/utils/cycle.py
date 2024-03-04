from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_sum


def is_organic(cycle: dict):
    lookup = download_lookup('standardsLabels.csv', True)

    def term_organic(lookup, term_id: str):
        return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'

    practices = list(filter(lambda p: p.get('term') is not None, cycle.get('practices', [])))
    return any([term_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def is_irrigated(cycle: dict):
    practice = next(
        (p for p in cycle.get('practices', []) if p.get('term', {}).get('@id').startswith('irrigated')), None
    )
    return practice is not None and list_sum(practice.get('value', [100])) > 0
