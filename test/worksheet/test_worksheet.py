import pytest


@pytest.mark.parametrize(
    argnames=["fix_worksheet", "fix_sections"],
    argvalues=[
        (
            ["test_file", "test_title"],
            [
                [
                    "Linear equations",
                    10,
                    "Linear equations",
                    "Solve the following equations for the specified variable."
                ]
            ]
        )
    ],
    ids=[
        "empty_worksheet"
        # "second_run",
        # "third_run"
    ],
    indirect=[
        "fix_worksheet",
        "fix_sections"
    ]
)
def test_example(
        fix_worksheet,
        fix_sections
):
    fix_worksheet.write()

