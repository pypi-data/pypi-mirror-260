"""Steps for testing the performance of queries."""
import time
from collections import defaultdict

from behave import when


@when('I execute the step `{step}` it should make "{query_count}" queries')
def check_query_count(context, step, query_count):
    """Check that the step only makes the expected number of queries."""
    with context.test.assertNumQueries(int(query_count)):
        context.execute_steps(step)


@when("I time the step `{step}`")
def check_execution_time(context, step):
    """Time the step."""
    before = time.time()
    context.execute_steps(step)
    after = time.time()
    if not hasattr(context, "step_execution_time"):
        context.step_execution_time = defaultdict(lambda: 0.0)
    context.step_execution_time[step] = after - before
