from functools import reduce
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import parse_node_value, weighted_average, _min, _max, _sd
from hestia_earth.aggregation.utils.completeness import blank_node_completeness_key


def _debugNodes(nodes: list):
    for node in nodes:
        if node.get('yield'):
            logger.debug(
                'id=%s, yield=%s, weight=%s, ratio=%s/%s, organic=%s, irrigated=%s',
                node.get('@id'),
                round(node.get('yield')),
                100/len(nodes),
                1,
                len(nodes),
                node.get('organic'),
                node.get('irrigated')
            )


def _weighted_value(node: dict):
    value = parse_node_value(node.get('value'))
    weight = node.get('productValue', 1)
    return None if (value is None or weight is None) else (value, weight)


def _missing_weights(nodes: list, completeness: dict):
    first_node = nodes[0]
    completeness_key = blank_node_completeness_key(first_node)
    completeness_count = len([node for node in nodes if node.get('completeness', False)])
    completeness_count_total = completeness.get(completeness_key, 0)
    completeness_count_missing = (
        completeness_count_total - completeness_count
    ) if completeness_count_total > completeness_count else 0

    return ([(0, 1)] * completeness_count_missing)


def _aggregate(nodes: list, completeness: dict):
    first_node = nodes[0]
    term = first_node.get('term')

    values = non_empty_list(map(_weighted_value, nodes))
    # account for complete nodes which have no value
    values_with_weight = values + _missing_weights(nodes, completeness)
    value = weighted_average(values_with_weight)
    values = [value for value, _w in values_with_weight]

    return {
        'nodes': nodes,
        'node': first_node,
        'term': term,
        'value': value,
        'max': _max(values),
        'min': _min(values),
        'sd': _sd(values),
        'observations': len(values)
    } if len(values) > 0 else None


def _aggregate_term(aggregates_map: dict, completeness: dict):
    def aggregate(term_id: str):
        blank_nodes = [node for node in aggregates_map.get(term_id, []) if not node.get('deleted')]
        return _aggregate(blank_nodes, completeness) if len(blank_nodes) > 0 else None
    return aggregate


def _aggregate_nodes(aggregate_key: str, index=0):
    def aggregate(data: dict):
        if index == 0:
            _debugNodes(data.get('nodes', []))
        completeness = data.get('completeness', {})
        terms = data.get(aggregate_key).keys()
        aggregates = non_empty_list(map(_aggregate_term(data.get(aggregate_key), completeness), terms))
        return (aggregates, data) if len(aggregates) > 0 else ([], {})

    def aggregate_multiple(data: dict):
        return reduce(
            lambda prev, curr: {**prev, curr[1]: _aggregate_nodes(curr[1], curr[0])(data)}, enumerate(aggregate_key), {}
        )

    return aggregate if isinstance(aggregate_key, str) else aggregate_multiple


def aggregate(aggregate_key: str, groups: dict) -> list:
    return non_empty_list(map(_aggregate_nodes(aggregate_key), groups.values()))
