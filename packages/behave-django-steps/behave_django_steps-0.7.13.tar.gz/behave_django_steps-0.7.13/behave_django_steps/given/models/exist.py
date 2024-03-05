"""Model existence steps."""
from behave import given, step


@given("models are available")
def models_are_available(context):
    """Load all models."""
    # pylint: disable-next=import-outside-toplevel
    import django.apps

    # pylint: disable-next=import-outside-toplevel
    from django.contrib.auth import get_user_model

    models = django.apps.apps.get_models(
        include_auto_created=True, include_swapped=True
    )
    models_excluding_user = []
    for model in models:
        if (  # pylint: disable=protected-access
            model._meta.model_name.lower() == "user"
            or model._meta.object_name.lower() == "user"
        ):
            continue
        models_excluding_user.append(model)
    models_excluding_user.append(get_user_model())
    # pylint: disable=protected-access
    context.models = {
        **{model._meta.model_name: model for model in models_excluding_user},
        **{model._meta.object_name: model for model in models_excluding_user},
        **{model._meta.db_table: model for model in models_excluding_user},
        **{model._meta.verbose_name: model for model in models_excluding_user},
        **{model._meta.verbose_name_plural: model for model in models_excluding_user},
    }


@step('a "{model_name}" model is available')
def model_is_available(context, model_name):
    """Check if a model is available."""
    if not getattr(context, "models", None):
        context.execute_steps("Given models are available")
    model = context.models.get(model_name)
    context.test.assertTrue(model)
