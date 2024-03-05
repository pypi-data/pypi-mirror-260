"""Steps for testing authorization."""
import json

from behave import then
from behave.runner import Context
from django.contrib.auth.models import Group


@then('I should have the role "{role_name}"')
def has_role(context, role_name):
    """Check that the user has the role.

    Args:
        context (behave.runner.Context): The test context.
        role_name (str): The name of the role.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertTrue(context.user.groups.filter(name=role_name).exists())


@then('I should have the group "{group_name}"')
def has_group(context, group_name):
    """Check that the user has the group.

    Args:
        context (behave.runner.Context): The test context.
        group_name (str): The name of the group.
    """
    context.execute_steps(f'Then I should have the role "{group_name}"')


@then('I should not have the role "{role_name}"')
def does_not_have_role(context, role_name):
    """Check that the user does not have the role.

    Args:
        context (behave.runner.Context): The test context.
        role_name (str): The name of the role.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.test.assertFalse(context.user.groups.filter(name=role_name).exists())


@then('I should not have the group "{group_name}"')
def does_not_have_group(context, group_name):
    """Check that the user does not have the group.

    Args:
        context (behave.runner.Context): The test context.
        group_name (str): The name of the group.
    """
    context.execute_steps(f'Then I should not have the role "{group_name}"')


@then('I should have the permission "{permission_name}" for model "{model_name}"')
def has_permission(context, permission_name, model_name):
    """Check that the user has the role.

    Args:
        context (behave.runner.Context): The test context.
        permission_name (str): The name of the role.
        model_name (str): The name of the model.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.execute_steps(f'Given a "{model_name}" model is available')
    app_label = context.models[  # pylint: disable=protected-access
        model_name
    ]._meta.app_label
    context.test.assertTrue(context.user.has_perm(f"{app_label}.{permission_name}"))


@then('I should not have the permission "{permission_name}" for model "{model_name}"')
def does_not_have_permission(context, permission_name, model_name):
    """Check that the user does not have the role.

    Args:
        context (behave.runner.Context): The test context.
        permission_name (str): The name of the role.
        model_name (str): The name of the model.
    """
    context.test.assertTrue(getattr(context, "user", None) is not None)
    context.execute_steps(f'Given a "{model_name}" model is available')
    app_label = context.models[  # pylint: disable=protected-access
        model_name
    ]._meta.app_label
    context.test.assertFalse(context.user.has_perm(f"{app_label}.{permission_name}"))


@then(
    'the role "{dest_role}" should have the permissions from the "{source_role}" role'
)
def inherit_permissions_from_role(context, dest_role, source_role):
    """Check the role has the permissions from the other role.

    Args:
        context (behave.runner.Context): The test context.
        dest_role (str): The role to give the permissions to.
        source_role (str): The role to inherit the permissions from.
    """
    source_group = Group.objects.filter(name=source_role).first()
    context.test.assertTrue(source_group is not None)
    dest_group = Group.objects.filter(name=dest_role).first()
    context.test.assertTrue(dest_group is not None)
    permissions = source_group.permissions.all()
    for permission in permissions:
        context.test.assertTrue(
            dest_group.permissions.filter(pk=permission.pk).exists()
        )


@then("clean default permissions")
def then_clean_default_permissions(context: Context) -> None:
    """Removes default permissions created by django.

    Keeps permissions that start with "can_".

    This solves the problem of loading permissions after django has created them.

    Args:
        context (behave.runner.Context): The behave context.

    Returns:
        None
    """
    exception_raised = False
    try:
        with open("fixtures/Permission.json", "r", encoding="utf-8") as f:
            content = f.read()
        with open("fixtures/Permission.json", "w", encoding="utf-8") as f:
            data = json.loads(content)
            data = [x for x in data if x["fields"]["codename"].startswith("can_")]
            f.write(json.dumps(data, indent=2))
    except:  # noqa: E722 pylint: disable=bare-except pragma: no cover
        exception_raised = True  # pragma: no cover
    context.test.assertFalse(exception_raised)
