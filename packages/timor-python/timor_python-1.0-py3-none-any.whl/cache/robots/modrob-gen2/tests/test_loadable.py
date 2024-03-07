import json
from pathlib import Path
import unittest

import jsonschema

from timor import ModulesDB
from timor.utilities.file_locations import schema_dir
from timor.utilities.schema import get_schema_validator


class TestLoadable(unittest.TestCase):
    """Tests that modules.json loadable with timor and cobra schema compliant."""
    def setUp(self) -> None:
        self.package_dir = Path(__file__).parent.parent
        self.module_path = self.package_dir.joinpath("modules.json")

    def test_validation(self):
        _, validator = get_schema_validator(schema_dir.joinpath("ModuleSchema.json"))
        try:
            validator.validate(json.load(self.module_path.open("r")))
        except jsonschema.exceptions.ValidationError:
            self.fail("Failed to validate modules.json")

    def test_DB_init(self):
        ModulesDB.from_file(self.module_path, self.module_path.parent)
