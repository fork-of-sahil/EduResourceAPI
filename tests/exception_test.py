from core.libs.exceptions import FyleError

def test_FyleError():
    # Create an instance of FyleError
    error = FyleError(500, 'Test message')

    # Check if the properties are correctly set
    assert error.status_code == 500
    assert error.message == 'Test message'

    # Check if the to_dict() method returns the correct dictionary
    assert error.to_dict() == {'message': 'Test message'}