from unittest.mock import patch
import json

from tests.utils import (
    PRODUCT, SOURCE, fixtures_path, start_year, end_year, fake_download, fake_aggregated_version, filter_cycles
)
from hestia_earth.aggregation.utils import _group_by_product
from hestia_earth.aggregation.models.countries import aggregate, _irrigated_weight
from hestia_earth.aggregation.cycle.utils import (
    AGGREGATION_KEYS, _format_for_grouping, _update_cycle, _format_country_results
)
from hestia_earth.aggregation.utils.quality_score import calculate_score
from hestia_earth.aggregation.utils.impact_assessment import new_impact

class_path = 'hestia_earth.aggregation.models.countries'


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
        cycles = json.load(f)
    with open(f"{fixtures_path}/cycle/countries/aggregated.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    cycles = _format_for_grouping(filter_cycles(cycles))
    results = aggregate(AGGREGATION_KEYS, _group_by_product(PRODUCT, cycles, AGGREGATION_KEYS, False))
    results = list(map(_format_country_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE, False), results))
    results = list(map(calculate_score, results))
    results = results + list(map(new_impact, results))
    print(json.dumps(results, indent=2))
    assert results == expected


def test_irrigated_weight():
    country_id = 'GADM-ECU'
    assert _irrigated_weight(country_id, 2019) == 0.06885166693509422
