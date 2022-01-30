from .conftest import my_vcr


class TestImportJobs:

    @my_vcr.use_cassette('test_import_jobs.json')
    def test_import_jobs(self, xm):
        jobs = list(xm.import_jobs().get_import_jobs())
        assert iter(jobs)
        for job in jobs:
            assert iter(job.get_messages())
