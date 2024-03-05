"""Authentication steps."""
from behave import given
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


@given('I am assigned to the group "{group_name}"')
def assign_user_to_group(context, group_name):
    """Assigns a user to a group.

    Args:
        context: behave.runner.Context
        group_name: str
    """
    if not getattr(context, "user", None):
        context.execute_steps("Given I am a registered user")
    if not getattr(context, "models", None):
        context.execute_steps('Given a "Group" model is available')
    context.execute_steps(
        f"""Given a "Group" with values
                          | name |
                          | {group_name} |"""
    )
    model = context.models.get("Group")
    context.user.groups.add(model.objects.get(name=group_name))


@given('I am assigned to the role "{role_name}"')
def assign_user_to_role(context, role_name):
    """Checks if a user is assigned to a role.

    Args:
        context: behave.runner.Context
        role_name: str
    """
    context.execute_steps(f'Given I am assigned to the group "{role_name}"')


@given(
    'The group "{group_name}" has the permission "{permission_name}"'
    ' with codename "{codename}" for model "{model_name}"'
)
def give_group_permission(context, group_name, permission_name, codename, model_name):
    """Gives a group a permission for a model.

    Args:
        context: behave.runner.Context
        group_name: str
        permission_name: str
        codename: str
        model_name: str
    """
    context.execute_steps('Given a "Group" model is available')
    context.execute_steps(
        f"""Given a "Group" with values
                          | name |
                          | {group_name} |"""
    )
    model = context.models.get("Group")
    group = model.objects.get(name=group_name)
    context.execute_steps(
        f'Given the permission "{permission_name}" with codename "{codename}" '
        f'for model "{model_name}" exists'
    )
    model = context.models.get(model_name)
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    group.permissions.add(permission)


@given(
    'the permission "{permission_name}" with codename "{codename}" '
    'for model "{model_name}" exists'
)
def create_permission_for_model(context, permission_name, codename, model_name):
    """Creates a permission for a model.

    Args:
        context: behave.runner.Context
        permission_name: str
        codename: str
        model_name: str
    """
    context.execute_steps(f'Given a "{model_name}" model is available')
    model = context.models.get(model_name)
    content_type = ContentType.objects.get_for_model(model)
    if not Permission.objects.filter(
        codename=codename, content_type=content_type
    ).exists():
        Permission.objects.create(
            codename=codename,
            name=permission_name,
            content_type=content_type,
        )


@given('the role "{dest_role}" inherits permissions from the "{source_role}" role')
def given_role_inherit_permissions_from_role(context, dest_role, source_role):
    """Give the role the permissions from the other role.

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
    dest_group.permissions.add(*permissions)
