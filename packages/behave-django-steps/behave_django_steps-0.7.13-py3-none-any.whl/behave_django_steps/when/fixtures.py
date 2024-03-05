"""Fixtures steps."""
import os
from collections import defaultdict
from pathlib import Path

from behave import when
from behave.runner import Context


@when('the data for "{apps_maybe_model}" is dumped')
def step_impl(context: Context, apps_maybe_model: str):
    """Dump the database.

    This step is used to dump the database in the context of a test.

    Args:
        context (Context): The behave context.
        apps_maybe_model (str): A comma separated list of app and
         optionally model names.
    """
    apps_and_models = (
        apps_maybe_model.split(",") if "," in apps_maybe_model else [apps_maybe_model]
    )
    context.dumped_data = defaultdict(list)

    # pylint: disable=import-outside-toplevel
    from django.conf import settings
    from django.core.management import call_command

    if not settings.FIXTURE_DIRS:
        fixtures_dir = Path(settings.BASE_DIR) / "fixtures"
    else:
        fixtures_dir = Path(settings.FIXTURE_DIRS[0])
    for app_and_model in apps_and_models:
        app, model = (
            app_and_model.split(".") if "." in app_and_model else [app_and_model, None]
        )
        if app in ["auth"]:
            if not fixtures_dir.exists():
                os.makedirs(fixtures_dir)
            output_path = (
                fixtures_dir / f"{model}.json"
                if model
                else fixtures_dir / f"{app}.json"
            )
        else:
            app_fixtures = Path(f"{app}/fixtures")
            if not app_fixtures.exists():
                os.makedirs(app_fixtures)
            output_path = (
                app_fixtures / f"{model}.json"
                if model
                else app_fixtures / f"{app}.json"
            )
        call_command(
            "dumpdata",
            *[
                f"{app}.{model}" if model else app,
                "--natural-foreign",
                "--all",
                f"--output={output_path}",
                # Maybe add support for other databases?
                # f"--database=test_default"
            ],
            format="json",
            indent=2,
            stdout=context.stdout_capture,
        )
        context.dumped_data[app].append(model)
