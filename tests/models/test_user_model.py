import pytest
from werkzeug.security import check_password_hash

from app import db
from app.models import User, Color


def test_new_user_default_is_active():
    """
    For this test we are checking that `User` object is being created properly.
    """
    username = "Spiderman"
    password = "Peter"
    favourite_color = "green"
    user = User(username=username, password=password, favourite_color=favourite_color)

    assert user.username == username
    assert check_password_hash(user.password, password)
    assert user.favourite_color == favourite_color
    assert user.is_active is True


def test_new_user():
    """
    For this test we are checking that `User` object is being created properly.
    """
    username = "Spiderman"
    password = "Peter"
    favourite_color = "green"
    is_active = False
    user = User(username=username, password=password, favourite_color=favourite_color, is_active=is_active)

    assert user.username == username
    assert check_password_hash(user.password, password)
    assert user.favourite_color == favourite_color
    assert user.is_active == is_active


def test_get_id(test_user_object):
    """
    For this test we are checking that `User.get_id()` returns user id field.
    """
    assert test_user_object.get_id() == test_user_object.id


@pytest.mark.parametrize(
    "password,expected_result",
    (
        ("Peter", True),
        ("Peter_wrong", False),
    )
)
def test_check_password(password: str, expected_result: bool, test_user_object):
    """
    For this test we are checking that `User.check_password()` compares given password with user's password.
    """
    assert test_user_object.check_password(password=password) is expected_result


def test_save_favourite_color(test_user):
    """
    For this test we are checking that `User.save_favourite_color()` updates `favourite_color` field for user.
    """
    new_color = Color.get_random_color()
    test_user.save_favourite_color(favourite_color=new_color.color)
    user = User.query.filter_by(username=test_user.username).first()

    assert user.favourite_color == new_color.color


def test_get_random_user(app_with_migrations):
    """
    When `only_active=True` flag is passed to `User.get_random_user()` then random user have to be picked up from
        list of users in which `is_active` field is set to `True`.
    For this test we need to have users with both `is_active=True` and `is_active=False`. So we need to
        update some users to have `is_active=False` before test since all users in db have `is_active=True` by default.
    """
    # We have 8 test users in db. We will set `is_active=False` to six users with ids in range(3, 9).
    User.query.filter(User.id > 2).update({User.is_active: False})
    db.session.commit()

    active_users_usernames = list(map(lambda u: u.username, User.query.filter(User.is_active.is_(True)).all()))
    user = User.get_random_user()

    assert user
    assert user.is_active is True
    assert user.username in active_users_usernames


def test_get_random_user_all_not_active(app_with_migrations):
    """
    When `only_active=True` flag is passed to `User.get_random_user()` then random user have to be picked up from
        list of users in which `is_active` field is set to `True`.
    If all users in db is not active meaning that they all have `is_active=False`, then result should be `None`.
    """
    User.query.update({User.is_active: False})
    db.session.commit()
    user = User.get_random_user()

    assert user is None


def test_get_random_user_only_active_false(app_with_migrations):
    """
    When `only_active=False` flag is passed to `User.get_random_user()` then the value  of `is_active` doesn't matter
    while picking up a random user meaning that `is_active` field can have either `True` or `False` value.
    Because of that for this test we set `is_active` field to `False` for all users in db.
    """
    User.query.update({User.is_active: False})
    db.session.commit()
    user = User.get_random_user(only_active=False)

    assert user
    assert user.is_active is False


def test_signup(app_with_migrations):
    """
    For this test we are checking that `User.signup()` creates new user in db.
    """
    username = "Thor_new"
    password = "Thor"
    favourite_color = "blue"
    User.signup(username=username, password=password, favourite_color=favourite_color)
    user = User.query.filter_by(username=username).first()

    assert user
    assert user.username == username
    assert check_password_hash(user.password, password)
    assert user.favourite_color == favourite_color
    assert user.is_active is True
