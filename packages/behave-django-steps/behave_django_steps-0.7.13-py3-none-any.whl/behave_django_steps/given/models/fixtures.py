"""Fixtures steps."""
from copy import copy

from behave import given
from behave.runner import Context


@given('these fixtures are used "{fixture_names}"')
def step_impl(context: Context, fixture_names: str):
    """Load fixtures.

    This step is used to load fixtures in the context of a test.

    Args:
        context (Context): The behave context.
        fixture_names (str): A comma separated list of fixture names.
    """
    fixture_names = (
        fixture_names.split(",") if "," in fixture_names else [fixture_names]
    )
    context.fixtures = fixture_names
    context.test.fixtures = copy(context.fixtures)
    # pylint: disable=import-outside-toplevel
    from django.core.management import call_command

    # pylint: disable-next=protected-access
    for db_name in context.test._databases_names(include_mirrors=False):
        try:
            call_command(
                "loaddata",
                *context.fixtures,
                **{"verbosity": 0, "database": db_name},
            )
        except Exception:
            # pylint: disable-next=protected-access
            context.test._rollback_atomics(context.test.cls_atomics)
            raise
