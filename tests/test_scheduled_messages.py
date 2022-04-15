from .conftest import my_vcr

class TestScheduledMessages:

    @my_vcr.use_cassette('test_scheduled_messages.json')
    def test_scheduled_messages(self, xm_test):
        scheduled_messages = xm_test.scheduled_messages_endpoint().get_scheduled_messages()
        assert iter(scheduled_messages)
        for msg in scheduled_messages:
            assert msg.id is not None
            assert msg.name is not None
