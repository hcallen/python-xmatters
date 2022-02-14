from .conftest import my_vcr


class TestTemporaryAbsences:

    @my_vcr.use_cassette('test_temporary_absences.json')
    def test_temporary_absences(self, xm_test):
        tas = xm_test.temporary_absences_endpoint().get_temporary_absences()
        assert iter(tas)
        for a in tas:
            assert a.id is not None

