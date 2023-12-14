"""Steps for testing authorization."""
from behave import then
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
    for permission in permissions:
        context.test.assertTrue(
            dest_group.permissions.filter(pk=permission.pk).exists()
        )
