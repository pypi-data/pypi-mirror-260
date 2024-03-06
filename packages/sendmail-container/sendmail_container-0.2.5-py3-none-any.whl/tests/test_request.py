import pytest

from sendmail_container.request import FormDataRequest


def test_request_one_recipients():
    # GIVEN a request with a single recipient
    recipient: str = "test_email@example.com"

    # WHEN creating a FormDataRequest
    request = FormDataRequest(
        sender_prefix="maildaemon",
        email_server_alias="localhost",
        recipients=recipient,
        mail_title="Title",
        mail_body="Body",
        request_uri="http://localhost:8000/sendmail/",
    )

    # THEN the recipient field should be a list with a single recipient
    assert request.recipients == [recipient]
    assert isinstance(request.recipients, list)


def test_request_multiple_recipients_in_list():
    # GIVEN a request with multiple recipients
    recipients: list = ["test_email@example.com", "second_email@example.com"]

    # WHEN creating a FormDataRequest
    request = FormDataRequest(
        sender_prefix="maildaemon",
        email_server_alias="localhost",
        recipients=recipients,
        mail_title="Title",
        mail_body="Body",
        request_uri="http://localhost:8000/sendmail/",
    )

    # THEN the recipient field should be a list with both recipients
    assert request.recipients == recipients
    assert isinstance(request.recipients, list)


def test_request_multiple_recipients_in_string():
    # GIVEN a request with multiple recipients
    recipients: str = "test_email@example.com,second_email@example.com"

    # WHEN creating a FormDataRequest
    request = FormDataRequest(
        sender_prefix="maildaemon",
        email_server_alias="localhost",
        recipients=recipients,
        mail_title="Title",
        mail_body="Body",
        request_uri="http://localhost:8000/sendmail/",
    )

    # THEN the recipient field should be a list with both recipients
    assert isinstance(request.recipients, list)
    assert request.recipients == recipients.split(",")


@pytest.mark.xfail(reason="Additional setup needed. See docstring")
def test_request_submit():
    """This test will fail as it requires a running sendmail app serving port 8000, as well as a running
    SMTP server to pass."""

    # GIVEN a valid request
    request = FormDataRequest(
        sender_prefix="maildaemon",
        email_server_alias="localhost",
        recipients="test_email@example.com",
        mail_title="Title",
        mail_body="Body",
        request_uri="http://localhost:8000/sendmail/",
    )

    # WHEN submitting the request
    response = request.submit()

    # THEN the response should be successful
    assert response.ok
