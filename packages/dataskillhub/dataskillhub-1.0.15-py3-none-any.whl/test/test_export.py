import pytest
from data_skill_hub.export import (
    trigrammer,
    TrigrammerError,
    get_output_name,
)


# part test


def test_trigrammer():
    print("____test_trigrammer____")
    assert trigrammer("yao.xin") == "xya"
    assert trigrammer("yyy.xin") == "xyy"
    assert trigrammer("y_dsqghjao.xin") == "xy_"
    assert trigrammer("yqsdg_dsqghjao.xin") == "xyq"
    assert trigrammer("yao.jin.xin") == "jya"  # Identifiez le premier point


def test_trigrammer_failed():
    with pytest.raises(TrigrammerError):
        trigrammer("yao..xin")


def test_get_output_name():
    print("____test_get_output_name____")
    assert (
        get_output_name("yao.xin", "dataScience", anonimized=True)
        == "xya/dataScience_a"
    )
    assert (
        get_output_name("yao/abc.xin", "dataScience", anonimized=True)  # noqa:
        == "xya/dataScience_a"
    )
    assert (
        get_output_name("y/a/o/ab.x", "dataScience", anonimized=True)  # noqa:
        == "xy//dataScience_a"
    )
    assert (
        get_output_name("yao.xin", "dataScience", anonimized=False) == "xya/dataScience"
    )
    assert (
        get_output_name("yao/abc.xin", "dataScience", anonimized=False)  # noqa:
        == "xya/dataScience"
    )
    assert (
        get_output_name("y/a/o/ab.x", "dataScience", anonimized=False)  # noqa:
        == "xy//dataScience"
    )
