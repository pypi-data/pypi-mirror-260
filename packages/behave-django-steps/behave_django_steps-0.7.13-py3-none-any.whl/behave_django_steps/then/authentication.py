"""Steps for testing authentication."""
from behave import then


@then("I should be a superuser")
def is_superuser(context):
    """Check that a user is a superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.is_superuser)


@then("I should not be a superuser")
def is_not_superuser(context):
    """Check that a user is not a superuser.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.is_superuser)


@then("I should be a staff user")
def is_staff_user(context):
    """Check that a user is a staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.is_staff)


@then("I should not be a staff user")
def is_not_staff_user(context):
    """Check that a user is not a staff user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.is_staff)


@then("I should not be an active user")
def then_is_not_active_user(context):
    """Check that a user is not an active user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.is_active)


@then("I should be an active user")
def then_should_be_active_user(context):
    """Check that a user is an active user.

    Args:
        context (behave.runner.Context): The test context.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.is_active)


@then('I should have a first name of "{first_name}"')
def has_first_name(context, first_name):
    """Check that a user has the correct first name.

    Args:
        context (behave.runner.Context): The test context.
        first_name (str): The first name to check.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.first_name == first_name)


@then('I should have a last name of "{last_name}"')
def has_last_name(context, last_name):
    """Check that a user has the correct last name.

    Args:
        context (behave.runner.Context): The test context.
        last_name (str): The last name to check.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.last_name == last_name)
