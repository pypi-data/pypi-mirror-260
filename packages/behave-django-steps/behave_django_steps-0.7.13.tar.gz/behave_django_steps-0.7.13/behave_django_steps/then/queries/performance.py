"""Steps for testing the performance of queries."""
from behave import then


@then('the step `{step}` execution should only take "{max_seconds}" seconds')
def check_execution_time(context, step, max_seconds):
    """Check that the step only takes the specified time."""
    context.test.assertTrue(context.step_execution_time[step] <= float(max_seconds))
