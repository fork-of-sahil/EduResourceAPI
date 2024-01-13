import pytest
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

def test_base_assert():
    with pytest.raises(FyleError) as e:
        base_assert(500, 'Test message')
    assert str(e.value) == 'Test message'
    assert e.value.status_code == 500

def test_assert_auth():
    with pytest.raises(FyleError) as e:
        assert_auth(False, 'Test auth message')
    assert str(e.value) == 'Test auth message'
    assert e.value.status_code == 401

def test_assert_true():
    with pytest.raises(FyleError) as e:
        assert_true(False, 'Test true message')
    assert str(e.value) == 'Test true message'
    assert e.value.status_code == 403

def test_assert_valid():
    with pytest.raises(FyleError) as e:
        assert_valid(False, 'Test valid message')
    assert str(e.value) == 'Test valid message'
    assert e.value.status_code == 400

def test_assert_found():
    with pytest.raises(FyleError) as e:
        assert_found(None, 'Test found message')
    assert str(e.value) == 'Test found message'
    assert e.value.status_code == 404