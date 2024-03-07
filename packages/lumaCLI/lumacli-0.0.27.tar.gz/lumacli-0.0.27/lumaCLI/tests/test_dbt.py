from typer.testing import CliRunner

from lumaCLI.main import app
from lumaCLI.tests.utils import METADATA_DIR

import os

runner = CliRunner()


def test_ingest_requires_only_manifest_and_catalog_json(test_server):
    """
    Test if the 'ingest' command requires only manifest.json and catalog.json
    """
    # Get result when the required files are present
    result_no_changes = get_result(test_server, "ingest")

    # Get result when the rest of the json files are missing
    result_manifest_missing = get_result_after_renaming(test_server, "ingest", "manifest.json")
    result_catalog_missing = get_result_after_renaming(test_server, "ingest", "catalog.json")
    result_sources_missing = get_result_after_renaming(test_server, "ingest", "sources.json")
    result_run_results_missing = get_result_after_renaming(test_server, "ingest", "run_results.json")

    # Check ingest works when no files are changed, or sources.json or run_results.json are missing
    assert result_no_changes.exit_code == 0
    assert result_sources_missing.exit_code == 0
    assert result_run_results_missing.exit_code == 0

    # Check ingest fails when either manifest.json or catalog.json is missing
    assert result_manifest_missing.exit_code == 1
    assert result_catalog_missing.exit_code == 1


def test_sendtestresults_requires_only_run_results_json(test_server):
    """
    Test if the 'send-test-results' command of the dbt module requires only run_results.json
    """

    # Get result when the required files are present
    result_no_changes = get_result(test_server, "send-test-results")

    # Get result when the rest of the json files are missing
    result_manifest_missing = get_result_after_renaming(test_server, "send-test-results", "manifest.json")
    result_catalog_missing = get_result_after_renaming(test_server, "send-test-results", "catalog.json")
    result_sources_missing = get_result_after_renaming(test_server, "send-test-results", "sources.json")
    result_run_results_missing = get_result_after_renaming(test_server, "send-test-results", "run_results.json")

    # Check ingest works when no files are changed, or any other json file but run_result.json is missing
    assert result_no_changes.exit_code == 0
    assert result_sources_missing.exit_code == 0
    assert result_manifest_missing.exit_code == 0
    assert result_catalog_missing.exit_code == 0

    # Check ingest fails when run_results.json is missing
    assert result_run_results_missing.exit_code == 1


# Rename files, get result, and rename them back
def get_result_after_renaming(test_server, command, file_name):
    os.rename(f'{METADATA_DIR}/{file_name}', f'{METADATA_DIR}/missing_{file_name}')
    result = get_result(test_server, command)
    os.rename(f'{METADATA_DIR}/missing_{file_name}', f'{METADATA_DIR}/{file_name}')

    return result


# Get result from invoking the runner ("ingest" is the default command)
def get_result(test_server, command):
    result = runner.invoke(
        app,
        [
            "dbt",
            command,
            "--metadata-dir",
            METADATA_DIR,
            "--luma-url",
            test_server,
        ],
    )
    
    return result
