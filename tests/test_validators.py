import pytest
from src.validators import JSONRequestValidator
from src.exceptions import ValidationError

class TestJSONRequestValidator:
    def test_valid_compute_request(self):
        """Test valid compute request validation"""
        validator = JSONRequestValidator()
        request = {
            "command_type": "compute",
            "expression": "2 + 2"
        }
        validator.validate(request)  # Should not raise

    def test_invalid_command_type(self):
        """Test invalid command type"""
        validator = JSONRequestValidator()
        request = {
            "command_type": "invalid_type"
        }
        try:
            validator.validate(request)
            pytest.fail("ValidationError was not raised")
        except ValidationError as e:
            assert str(e) == "Invalid command_type: invalid_type", f"Unexpected error message: {str(e)}"
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {type(e).__name__}, {str(e)}")