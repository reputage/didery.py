import pytest
try:
    import simplejson as json
except ImportError:
    import json

from click.testing import CliRunner
from pydidery.cli import main
from pydidery.lib import generating as gen


def parsOutput(data):
    return list(filter(None, data.split('\n')))


def testValidConfigFile():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test valid config file
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]}')

        result = runner.invoke(main, ['config.json'])

        assert result.exit_code == 0
        assert result.output == "No options given. For help use --help. Exiting Didery.py\n"


def testInvalidConfigJson():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test invalid json
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: Invalid JSON.\n"


def testInvalidServerList():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test non list "servers" value
        with open('config.json', 'w') as f:
            f.write('{"servers": "http://localhost:8080"}')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: \"servers\" field must be a list.\n"


def testMissingConfigFields():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test missing required fields
        with open('config.json', 'w') as f:
            f.write('{"urls": ["http://localhost:8080", "http://localhost:8000"]}')

        result = runner.invoke(main, ['config.json', '--upload'])

        assert result.exit_code == 0
        assert result.output == "Error parsing the config file: Missing required field servers.\n"


def testValidInceptionDataFile():
    runner = CliRunner()
    history, vk, sk, pvk, psk = gen.historyGen()
    data = {
        "history": history
    }

    with runner.isolated_filesystem():
        # Test valid config file
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]}')

        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

        result = runner.invoke(main, ['config.json', '--incept', '--data=data.json', '-v'], input="{}\n".format(sk))

        output = parsOutput(result.output)
        expected_output = [
            "Please enter you signing/private key: {}".format(sk),
            "2/2 requests succeeded."
        ]

        assert result.exit_code == 0
        assert output == expected_output


def testValidInception():
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Test valid config file
        with open('config.json', 'w') as f:
            f.write('{"servers": ["http://localhost:8080", "http://localhost:8000"]}')

        result = runner.invoke(main, ['config.json', '--incept', '-v'], input="y\n")

        output = parsOutput(result.output)
        expected_output = [
            "Keys have been generated and stored in the current directory under didery.keys.json. ",
            "Make a copy and store them securely. ",
            "The file will be deleted after you enter a key: y",
            "didery.keys.json deleted.",
            "2/2 requests succeeded."
        ]

        assert result.exit_code == 0
        assert output == expected_output
