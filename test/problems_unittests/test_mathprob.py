import pytest

from examgen.problems.base_classes import MathProb


# @pytest.mark.skip("slow and flaky. run manually as needed")
def test_get_coeffs():
    mathprob = MathProb()
    for i in range(50):
        assert 0 not in mathprob.get_coeffs(n=10, start=-10, stop=10, include_zero=False), \
            f"output contains 0"
    for i in range(50):
        out = mathprob.get_coeffs(n=5, start=-5, stop=6, unique=True)
        assert len(out) == 5, f"output contains wrnog # of elements"
        assert len(set([abs(i) for i in out])) == len(out), "output contains duplicate elements"

    with pytest.raises(TypeError):
        mathprob.get_coeffs(n="asdf", start=10, stop=20)
    with pytest.raises(ValueError):
        mathprob.get_coeffs(n=-1, start=10, stop=20)
    with pytest.raises(ValueError):
        mathprob.get_coeffs(n=1, start=10, stop=-10)


def test_init():

    mathprob = MathProb(var="x")
    assert mathprob.get_variable() == "x", "get_variable returned the wrong letter"

    with pytest.raises(TypeError):
        MathProb(var=["a", "b"])
    with pytest.raises(ValueError):
        MathProb(var="")
