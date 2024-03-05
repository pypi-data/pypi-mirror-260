import pytest
from dossier_competence.main import (
    trigrammer,
    TrigrammerError,
    get_trigrammer,
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


def test_get_trigrammer():
    print("____test_get_trigrammer____")
    assert get_trigrammer("yao.xin/dataScience.md") == "yao.xin"
    assert get_trigrammer("yaoxin/dataScience.md") == "yaoxin"
    assert get_trigrammer("yao/xin/dataScience.md") == "xin"
    assert get_trigrammer("y/a/o/xin/dataScience.md") == "xin"
    assert get_trigrammer("y//a//o/xin/dataScience.md") == "xin"
    assert get_trigrammer("y//a//o//xin//dataScience.md") == ""


def test_get_trigrammer_failed():
    with pytest.raises(TrigrammerError):
        get_trigrammer("xin.dataScience.md")


def test_get_output_name():
    print("____test_get_output_name____")
    assert (
        get_output_name("yao.xin/export.yaml", "dataScience", anonimized=True)
        == "xya/dataScience_a"
    )
    assert (
        get_output_name(
            "yao/abc.xin/export.yaml", "dataScience", anonimized=True
        )  # noqa:
        == "xab/dataScience_a"
    )
    assert (
        get_output_name(
            "y/a/o/ab.x/export.yaml", "dataScience", anonimized=True
        )  # noqa:
        == "xab/dataScience_a"
    )
    assert (
        get_output_name("yao.xin/export.yaml", "dataScience", anonimized=False)
        == "xya/dataScience"
    )
    assert (
        get_output_name(
            "yao/abc.xin/export.yaml", "dataScience", anonimized=False
        )  # noqa:
        == "xab/dataScience"
    )
    assert (
        get_output_name(
            "y/a/o/ab.x/export.yaml", "dataScience", anonimized=False
        )  # noqa:
        == "xab/dataScience"
    )


if __name__ == "__main__":
    pytest.main(["-s", "test_main.py"])
