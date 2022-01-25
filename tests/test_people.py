import pytest

@pytest.mark.skip()
@pytest.mark.usefixtures('people')
def test_get_people_devices(people):
    for person in people:
        devices = person.get_devices()
        return isinstance(devices, list)
