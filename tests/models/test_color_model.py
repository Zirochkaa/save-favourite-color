from app import db
from app.models import Color


def test_new_color():
    """
    For this test we are checking that `Color` object is being created properly.
    """
    color = "blue"
    is_active = False
    color_object = Color(color=color, is_active=is_active)

    assert color_object.color == color
    assert color_object.is_active == is_active


def test_check_exists(app_with_migrations):
    """
    For this test we are checking an active color, so we get random color from db since they all have `is_active=True`.
        This random color is active and exists, so the expected result of `Color.check_exists()` function is
        `Color` object which means that color exists.
    """
    active_color = Color.get_random_color()
    color = Color.check_exists(color=active_color.color)

    assert color
    assert color.color == active_color.color


def test_check_exists_not_active_color(app_with_migrations):
    """
    For this test we are checking not active color, so we get random color from db and since they all have
        `is_active=True` we also need to set `is_active=False` for this random color. The expected result of
        `Color.check_exists()` function is `None` because this random color is not active.
    """
    random_color = Color.get_random_color()
    random_color.is_active = False
    db.session.add(random_color)
    db.session.commit()

    color = Color.check_exists(color=random_color.color)

    assert color is None


def test_check_exists_wrong_color(app_with_migrations):
    """
    For this test we are checking not existing color. Since this color not exists so the expected result of
        `Color.check_exists()` function is `None`.
    """
    color = Color.check_exists(color="wrong_color")

    assert color is None


def test_get_all_active_colors_three_active_colors(app_with_migrations):
    """
    For this test we are checking that if in db there are both not active and active colors then the expected result of
        `Color.get_all_active_colors()` function will be a list with amount of elements equal to the amount of
        active colors.
    """
    # We have 13 test colors in db. We will set `is_active=False` to ten colors.
    list_of_all_colors = list(map(lambda c: c.color, Color.query.all()))
    Color.query.filter(Color.color.in_(list_of_all_colors[:-3])).update({Color.is_active: False})
    db.session.commit()

    colors = Color.get_all_active_colors()
    assert len(colors) == 3


def test_get_all_active_colors_zero_active_colors(app_with_migrations):
    """
    For this test we are checking that if there is no active colors then the expected result of
        `Color.get_all_active_colors()` function is `[]`.
    """
    Color.query.update({Color.is_active: False})
    db.session.commit()

    colors = Color.get_all_active_colors()
    assert not colors


def test_get_random_color(app_with_migrations):
    """
    When `only_active=True` flag is passed to `Color.get_random_color()` then random color have to be picked up from
        list of colors in which `is_active` field is set to `True`.
    For this test we need to have colors with both `is_active=True` and `is_active=False`. So we need to
        update some colors to have `is_active=False` before test since all colors in db have
        `is_active=True` by default.
    """
    # We have 13 test colors in db. We will set `is_active=False` to ten colors.
    list_of_all_colors = list(map(lambda c: c.color, Color.query.all()))
    Color.query.filter(Color.color.in_(list_of_all_colors[:-3])).update({Color.is_active: False})
    db.session.commit()

    active_colors = list(map(lambda c: c.color, Color.query.filter(Color.is_active.is_(True)).all()))
    color = Color.get_random_color()

    assert color
    assert color.is_active is True
    assert color.color in active_colors


def test_get_random_color_all_not_active(app_with_migrations):
    """
    When `only_active=True` flag is passed to `Color.get_random_color()` then random color have to be picked up from
        list of colors in which `is_active` field is set to `True`.
    If all colors in db is not active meaning that they all have `is_active=False`, then result should be `None`.
    """
    Color.query.update({Color.is_active: False})
    db.session.commit()
    color = Color.get_random_color()

    assert color is None


def test_get_random_color_only_active_false(app_with_migrations):
    """
    When `only_active=False` flag is passed to `Color.get_random_color()` then the value  of `is_active` doesn't matter
    while picking up a random color meaning that `is_active` field can have either `True` or `False` value.
    Because of that for this test we set `is_active` field to `False` for all colors in db.
    """
    Color.query.update({Color.is_active: False})
    db.session.commit()
    color = Color.get_random_color(only_active=False)

    assert color
    assert color.is_active is False
