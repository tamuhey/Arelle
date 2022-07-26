import os

import pytest

from tests.integration_tests.validation.validation_util import get_test_data

CONFORMANCE_SUITE = 'tests/resources/conformance_suites/oim-conformance-2021-10-13.zip/oim-conformance-2021-10-13'
ARGS = [
    '--keepOpen',
    '--plugins', 'loadFromOIM',
    '--testcaseResultsCaptureWarnings',
    '--validate',
    '--file', os.path.join(CONFORMANCE_SUITE, 'oim-index.xml'),
]

TEST_DATA = get_test_data(ARGS)


@pytest.mark.parametrize("result", TEST_DATA)
def test_oim_conformance_suite(result):
    assert result['status'] == 'pass', \
        'Expected these validation suffixes: {}, but received these validations: {}'.format(
            result.get('expected'), result.get('actual')
        )
