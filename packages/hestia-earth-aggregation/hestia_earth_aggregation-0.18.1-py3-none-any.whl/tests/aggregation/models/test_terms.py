from unittest.mock import patch
import json

from tests.utils import (
    SOURCE, fixtures_path, fake_download, fake_grouped_cycles, start_year, end_year, fake_aggregated_version
)
from hestia_earth.aggregation.models.terms import aggregate
from hestia_earth.aggregation.cycle.utils import (
    AGGREGATION_KEYS, _update_cycle, _format_terms_results
)
from hestia_earth.aggregation.utils.quality_score import calculate_score
from hestia_earth.aggregation.utils.impact_assessment import new_impact

class_path = 'hestia_earth.aggregation.models.terms'


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
    with open(f"{fixtures_path}/cycle/terms/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles()
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE), results))
    results = list(map(calculate_score, results))
    results = results + list(map(new_impact, results))
    print(json.dumps(results, indent=2))
    assert results == expected


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
def test_aggregate_cycle_relative(*args):
    with open(f"{fixtures_path}/cycle/terms/relative-unit-aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles(is_relative=True)
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE, False), results))
    results = list(map(calculate_score, results))
    results = results + list(map(new_impact, results))
    print(json.dumps(results, indent=2))
    assert results == expected
