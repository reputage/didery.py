import pytest
from click.testing import CliRunner
from pydidery.cli import main


def testConfig():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test valid config file
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]}')

        result = runner.invoke(main, ['config.json'])

        assert result.exit_code == 0
        assert result.output == "No options given. For help use --help. Exiting Didery.py\n"

        # Test invalid json
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: Invalid JSON.\n"

        # Test non list "servers" value
        with open('config.json', 'w') as f:
            f.write('{"servers": "http://localhost:8080"}')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: \"servers\" field must be a list.\n"

        # Test missing required fields
        with open('config.json', 'w') as f:
            f.write('{"urls": ["http://localhost:8080", "http://localhost:8000"]}')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: Missing required field servers.\n"


# def testInception():
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         # Test valid config file
#         with open('config.json', 'w') as f:
#             f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]}')
#
#         result = runner.invoke(main, ['config.json', '--incept'], input="y\n")
#         print(result.output)
#         assert False
