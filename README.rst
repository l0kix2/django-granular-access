
Granular access is django app for giving permissions on set of models for users
or groups.


Quick start
-----------

1. Add "granular_access" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'granular_access',
    )

2. Run south command for createing tables in database::

      ./manage.py migrate granular_access

3. Create permission for user or group on some set of models via admin or using
`create_permission` function::

    >>> from granular_settings import create_permission
    >>> create_permission(user=joker, action='kill_and_rob', app_label='auth',
    ...     model_name='user', conditions=[{'username__startswith': 'victim'}])

    You can find more examples in tests.

4. Filter available models using filter_available function::

    >>> from granular_settings import filter_available
    >>> available_users = filter_available(to=joker, action='kill_and_rob',
    ...     queryset=User.objects.all())

5. Profit.


Settings
--------

You can define some settings for customize app behaviour:

  * GRANULAR_ACCESS_USER_MODEL -- user model in your project for assigning
    permissions.

    Example: 'users.Profile'.
    Default: 'auth.User'.

  * GRANULAR_ACCESS_GROUP_MODEL -- group model in your project for assigning
    permissions.

    Example: 'groups.UserGroup'.
    Default: 'auth.Group'.

  * GRANULAR_ACCESS_USER_GROUP_RELATED_NAME -- related name in user model for
    relatinon with groups. So you can get user groups by calling
    >>> user_instance.related_name.all()

    It will be used if GRANULAR_ACCESS_GET_USER_GROUPS_FUNCTION settings is not
    set or set to None.

    Example: 'user_groups'.
    Default: 'groups'.

  * GRANULAR_ACCESS_GET_USER_GROUPS_FUNCTION -- path to function, witch receives
    user instance as first argument and return iterable with groups or group
    ids. You can use this function if you have more complex logic for gettings
    user groups, than via related_name.

    Example: 'project_name.users_app.helpers.get_user_groups'.
    Default: None.

  * GRANULAR_ACCESS_CONSIDER_SUPERUSER -- boolean value, which indicates should
    superusers get all permissions on all models or not.

    Default: True.


Extras
------

You can use AccessManager in your model::

    from granular_access import AccessManager

    class MyModel(models.Model):
        objects = AccessManager()

Or if you already have some special manager for your model, you can use
AccessManagerMixin in it.


ALso you can utilize AccessQuerySet or AccessQuerySetMixin.
