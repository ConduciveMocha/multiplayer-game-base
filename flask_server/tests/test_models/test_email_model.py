import pytest

from server.db.models import Email
from server.logging import make_test_logger, log_test

logger = make_test_logger(__name__)


@pytest.mark.parametrize(
    "address,expected",
    [
        ("email.email@email.com", True),
        ("email@wisc.edu", True),
        ("email@government.gov", True),
        ("this is definitely not an email", False),
        ("@fails.com", False),
        ("email@email", False),
    ],
)
@log_test(logger)
def test_email_validation(with_app, address, expected):
    if expected:
        email = Email(address)
        assert email.email == address
        assert email.verified == False

    else:
        try:
            email = Email(address)
            assert False
        except AssertionError:
            assert True
