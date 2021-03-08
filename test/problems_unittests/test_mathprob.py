import pytest

from examgen.lib.base_classes import MathProb


@pytest.mark.skip("slow and flaky. run manually as needed")
def test_get_coeffs():
    mathprob = MathProb()
    for i in range(50):
        assert 0 not in mathprob.get_coeffs(n=10, start=-10, stop=10, include_zero=False), \
            f"output contains 0"
    for i in range(50):
        out = mathprob.get_coeffs(n=10, start=-5, stop=6, unique=True)
        assert len(out) == 10, f"output contains wrnog # of elements"
        assert len(set(out)) == len(out), "output contains duplicate elements"
    assert set(mathprob.get_coeffs(n=2, start=-1, stop=1, unique=True, include_zero=False)) == {-1, 1}

    with pytest.raises(TypeError):
        mathprob.get_coeffs(n="asdf", start=10, stop=20)
    with pytest.raises(ValueError):
        mathprob.get_coeffs(n=-1, start=10, stop=20)
    with pytest.raises(ValueError):
        mathprob.get_coeffs(n=1, start=10, stop=-10)
