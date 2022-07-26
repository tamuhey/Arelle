import os

from arelle.CntlrCmdLine import parseAndRun


CONFORMANCE_SUITE = 'tests/resources/conformance_suites/efm_conformance_suite_2022.zip/conf'
TAXONOMY_PACKAGE = 'tests/resources/taxonomy_packages/edgarTaxonomiesPackage-22.1.zip'
EFM_PLUGIN = 'validate/EFM'
IXDS_PLUGIN = 'inlineXbrlDocumentSet'
FILTER = '(?!arelle:testcaseDataUnexpected)'

BASE_ARGS = [
    '--file', os.path.abspath(os.path.join(CONFORMANCE_SUITE, 'testcases.xml')),
    '--logCodeFilter', FILTER,
    '--plugins', 'plugin/loadFromOIM',
    '--testcaseResultsCaptureWarnings',
    '--validate'
]


def run_oim_conformance_suite(args):
    """
    Kicks off the validation of the EFM conformance suite.

    :param args: The arguments to pass to Arelle in order to accurately validate the EFM conformance suite
    :param args: list of str
    :return: Returns the result of parseAndRun which in this case is the created controller object
    :rtype: ::class:: `~arelle.CntlrCmdLine.CntlrCmdLine`
    """
    return parseAndRun(args)


if __name__ == "__main__":
    print('Running OIM tests...')
    run_oim_conformance_suite(BASE_ARGS)
