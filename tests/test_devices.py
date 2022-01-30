from tests.conftest import my_vcr


class TestDevices:
    @my_vcr.use_cassette('test_devices.json')
    def test_devices(self, xm):
        devices = list(xm.devices().get_devices())
        for device in devices:
            assert iter(list(device.timeframes))
