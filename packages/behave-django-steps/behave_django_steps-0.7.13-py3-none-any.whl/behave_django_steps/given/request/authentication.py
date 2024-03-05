"""Authentication steps."""
import base64

from behave import given
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

HTTP_HEADER_ENCODING = "iso-8859-1"

User = get_user_model()


def basic_auth_header(username: str, password: str) -> str:
    """Return a dict with the basic auth header.

    Args:
        username (str): The username.
        password (str): The password.
    """
    credentials = f"{username}:{password}"
    base64_credentials = base64.b64encode(
        credentials.encode(HTTP_HEADER_ENCODING)
    ).decode(HTTP_HEADER_ENCODING)
    return f"Basic {base64_credentials}"


@given('the user has a password of "{password}"')
def user_with_password(context, password):
    """Setup password.

    Args:
        context (behave.runner.Context): The test context.
        password (str): The password to use.
    """
    context.user_password = password


@given('the user has a username of "{username}"')
def user_with_username(context, username):
    """Setup username.

    Args:
        context (behave.runner.Context): The test context.
        username (str): The username to use.
    """
    context.user_username = username


@given('the user has a first name of "{first_name}"')
def user_with_firstname(context, first_name):
    """Setup first_name.

    Args:
        context (behave.runner.Context): The test context.
        first_name (str): The first name to use.
    """
    context.user_first_name = first_name


@given('the user has a last name of "{last_name}"')
def user_with_lastname(context, last_name):
    """Setup last_name.

    Args:
        context (behave.runner.Context): The test context.
        last_name (str): The username to use.
    """
    context.user_last_name = last_name


@given("the user is staff")
def user_with_staff(context):
    """Setup staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user_is_staff = True


@given("the user is a superuser")
def user_with_superuser(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user_is_superuser = True


@given("the user is active")
def user_is_active(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user_is_active = True


@given("the user is not active")
def user_is_not_active(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user_is_active = False


@given("I am a user")
def is_user(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username=getattr(context, "user_username", "test"),
        password=getattr(context, "user_password", "test"),
        is_active=getattr(context, "user_is_active", True),
        is_staff=getattr(context, "user_is_staff", False),
        is_superuser=getattr(context, "user_is_superuser", False),
        first_name=getattr(context, "user_first_name", "Test"),
        last_name=getattr(context, "user_last_name", "User"),
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am a superuser")
def is_superuser(context):
    """Setup superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username=getattr(context, "user_username", "test_superuser"),
        password=getattr(context, "user_password", "test"),
        is_active=getattr(context, "user_is_active", True),
        is_staff=getattr(context, "user_is_staff", False),
        is_superuser=True,
        first_name=getattr(context, "user_first_name", "Test"),
        last_name=getattr(context, "user_last_name", "Superuser"),
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am a registered user")
def setup_registered_user(context):
    """Setup registered user.

    Args:
        context (behave.runner.Context): The test context.
    """
    print(context)
    for key, value in context.__dict__.items():
        print(key, value)
    user = User.objects.create_user(
        username=getattr(context, "user_username", "test_user"),
        password=getattr(context, "user_password", "test"),
        is_active=getattr(context, "user_is_active", True),
        is_staff=getattr(context, "user_is_staff", False),
        is_superuser=getattr(context, "user_is_superuser", False),
        first_name=getattr(context, "user_first_name", "Test"),
        last_name=getattr(context, "user_last_name", "User"),
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am a staff user")
def setup_staff_user(context):
    """Setup staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    user = User.objects.create_user(
        username=getattr(context, "user_username", "test_staff_user"),
        password=getattr(context, "user_password", "test"),
        is_active=getattr(context, "user_is_active", True),
        is_staff=True,
        is_superuser=getattr(context, "user_is_superuser", False),
        first_name=getattr(context, "user_first_name", "Test"),
        last_name=getattr(context, "user_last_name", "StaffUser"),
    )
    context.user = user
    context.test.client.force_login(user)


@given("I am an anonymous user")
def setup_anon_user(context):
    """Setup anonymous user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.user = AnonymousUser()
    context.credentials = basic_auth_header("test", "bad_password")
