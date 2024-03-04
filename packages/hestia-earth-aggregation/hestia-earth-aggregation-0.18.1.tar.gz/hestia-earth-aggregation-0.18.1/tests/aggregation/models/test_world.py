from unittest.mock import patch
import json

from tests.utils import (
    PRODUCT, SOURCE, WORLD, fixtures_path, start_year, end_year, fake_download, fake_aggregated_version, filter_cycles
)
from hestia_earth.aggregation.utils import _group_by_product
from hestia_earth.aggregation.models.world import aggregate
from hestia_earth.aggregation.cycle.utils import (
    AGGREGATION_KEYS, _format_for_grouping, _update_cycle, _format_world_results
)
from hestia_earth.aggregation.utils.quality_score import calculate_score
from hestia_earth.aggregation.utils.impact_assessment import new_impact

class_path = 'hestia_earth.aggregation.models.world'


@patch('hestia_earth.aggregation.cycle.emission._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.input._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.practice.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.cycle.practice._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.product._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.measurement._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.impact_assessment._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.queries.download_hestia', side_effect=fake_download)
def test_aggregate_cycle(*args):
    with open(f"{fixtures_path}/cycle/countries/aggregated.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    with open(f"{fixtures_path}/cycle/world/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    cycles = _format_for_grouping(filter_cycles(cycles))
    results = aggregate(AGGREGATION_KEYS, _group_by_product(PRODUCT, cycles, AGGREGATION_KEYS, False))
    results = list(map(_format_world_results, results))
    results = list(map(_update_cycle(WORLD, start_year, end_year, SOURCE, False), results))
    results = list(map(calculate_score, results))
    results = results + list(map(new_impact, results))
    print(json.dumps(results, indent=2))
    assert results == expected
