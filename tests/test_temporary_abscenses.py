from .conftest import my_vcr


class TestTemporaryAbsences:

    @my_vcr.use_cassette('test_temporary_absences.json')
    def test_temporary_absences(self, xm):
        tas = list(xm.temporary_absences().get_temporary_absences())
        assert iter(tas)