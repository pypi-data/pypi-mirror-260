"""Constants and reusable definitions for the OpenDAPI Python client."""

TEAMS_SUFFIX = [".teams.yaml", ".teams.yml", ".teams.json"]
DATASTORES_SUFFIX = [".datastores.yaml", ".datastores.yml", ".datastores.json"]
PURPOSES_SUFFIX = [".purposes.yaml", ".purposes.yml", ".purposes.json"]
DAPI_SUFFIX = [".dapi.yaml", ".dapi.yml", ".dapi.json"]

OPENDAPI_URL = "https://opendapi.org/"
OPENDAPI_SPEC_URL = OPENDAPI_URL + "spec/{version}/{entity}.json"

PLACEHOLDER_TEXT = "placeholder text"

CONFIG_FILEPATH_FROM_ROOT_DIR = "opendapi.config.yaml"
DEFAULT_DAPIS_DIR = "dapis"
GITHUB_ACTIONS_FILEPATH_FROM_ROOT_DIR = ".github/workflows/opendapi_ci.yml"
DEFAULT_DAPI_SERVER_HOSTNAME = "https://api.wovencollab.com"
TESTS_FILEPATH_FROM_TESTS_DIR = "test_opendapi.py"
