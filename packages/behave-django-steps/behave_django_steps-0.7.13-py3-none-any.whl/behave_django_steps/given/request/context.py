"""Given steps for context."""

from behave import given
from behave.runner import Context


@given('context key "{key}" is set to "{value}"')
def context_key_value(context: Context, key: str, value: str) -> None:
    """Set a key in the context.

    Args:
        context: behave.runner.Context
        key: str
        value: str

    Returns:
        None

    Raises:
        AttributeError: If the key is not in the context.
    """
    setattr(context, key, value)


@given('context parent key "{key}" of "{parent}" is set to "{value}"')
def context_parent_key_value(
    context: Context, key: str, parent: str, value: str
) -> None:
    """Set a key of a parent item in the context.

    Args:
        context: behave.runner.Context
        key: str
        parent: str
        value: str

    Returns:
        None

    Raises:
        AttributeError: If the parent is not in the context.
    """
    setattr(getattr(context, parent), key, value)


@given('I save context item "{key}"')
def save_context_key(context: Context, key: str) -> None:
    """Calls save on an item in the context.

    Args:
        context: behave.runner.Context
        key: str

    Returns:
        None

    Raises:
        AttributeError: If the key is not in the context
          or the item does not have a save method.
    """
    getattr(context, key).save()


@given('context "{key}" value "{value}" is set to context "{other_key}"')
def set_context_key_to_other_key(
    context: Context, key: str, value: str, other_key: str
) -> None:
    """Set a key in the context.

    Args:
        context: behave.runner.Context
        key: str
        value: str
        other_key: str

    Returns:
        None

    Raises:
        AttributeError: If the key is not in the context.
    """
    setattr(getattr(context, key), value, getattr(context, other_key, None))


@given(
    'context "{key}" value "{value}" is set to the context "{other_value}"'
    ' of "{other_key}"'
)
def set_context_key_to_other_value_of_other_key(
    context: Context, key: str, value: str, other_value: str, other_key: str
) -> None:
    """Set a key in the context from another key.

    Args:
        context: behave.runner.Context
        key: str
        value: str
        other_value: str
        other_key: str

    Returns:
        None

    Raises:
        AttributeError: If the key is not in the context.
    """
    other_context = getattr(context, other_key, None)
    if other_context is not None:
        other_value = getattr(other_context, other_value, None)
    else:
        raise ValueError(f"Other context key {other_key} not found")
    target_context = getattr(context, key, None)
    if target_context is None:
        raise ValueError(f"Target Context key {key} not found")
    if isinstance(target_context, dict):
        target_context[value] = other_value
    else:
        setattr(target_context, value, other_value)
