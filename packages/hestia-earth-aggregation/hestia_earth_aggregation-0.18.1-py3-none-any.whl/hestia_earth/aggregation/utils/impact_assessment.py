from hestia_earth.schema import NodeType, ImpactAssessmentAllocationMethod
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import non_empty_list

from . import _aggregated_node
from .cycle import is_irrigated, is_organic
from .term import (
    _format_country_name, _format_irrigated, _format_organic
)


def _impact_assessment_id(n: dict, include_matrix=True):
    # TODO: handle impacts that dont have organic/irrigated version => only 1 final version
    return '-'.join(non_empty_list([
        n.get('product', {}).get('term', {}).get('@id'),
        _format_country_name(n.get('country', {}).get('name')),
        _format_organic(n.get('organic', False)) if include_matrix else '',
        _format_irrigated(n.get('irrigated', False)) if include_matrix else '',
        n.get('startDate'),
        n.get('endDate')
    ]))


def _impact_assessment_name(n: dict, include_matrix=True):
    return ' - '.join(non_empty_list([
        n.get('product', {}).get('term', {}).get('name'),
        n.get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if n.get('organic', False) else 'Conventional') if include_matrix else '',
            ('Irrigated' if n.get('irrigated', False) else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([n.get('startDate'), n.get('endDate')])
    ]))


def new_impact(cycle: dict):
    impact = {'type': NodeType.IMPACTASSESSMENT.value}
    impact['id'] = cycle.get('id')
    impact['name'] = cycle.get('name')
    impact['cycle'] = {
        'type': NodeType.CYCLE.value,
        'id': cycle.get('id')
    }
    site = cycle.get('site', {})
    if site:
        impact['site'] = {
            'type': NodeType.SITE.value,
            'id': site.get('id')
        }
        impact['country'] = site.get('country')

    impact['source'] = cycle.get('defaultSource')
    impact['aggregatedQualityScore'] = cycle.get('aggregatedQualityScore')
    impact['aggregatedQualityScoreMax'] = cycle.get('aggregatedQualityScoreMax')
    impact['aggregatedSources'] = cycle.get('aggregatedSources', [])
    impact['startDate'] = cycle.get('startDate')
    impact['endDate'] = cycle.get('endDate')
    product = find_primary_product(cycle)
    impact['product'] = product
    impact['functionalUnitQuantity'] = 1
    impact['allocationMethod'] = ImpactAssessmentAllocationMethod.NONE.value
    impact['organic'] = is_organic(cycle)
    impact['irrigated'] = is_irrigated(cycle)
    impact['dataPrivate'] = False
    return _aggregated_node(impact)
