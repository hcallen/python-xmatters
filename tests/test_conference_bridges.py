import pytest

import xmatters.objects.conference_bridges
import xmatters.errors


class TestCreateGetUpdateDelete:

    @pytest.mark.order(1)
    def test_create(self, xm_sb):
        data = {"name": "INC-211 Zoom Conference",
                "description": "Call to discuss incident 211 and restore services",
                "tollNumber": "1-877-394-2905",
                "tollFreeNumber": "1-888-223-4343",
                "preferredConnectionType": "TOLL_FREE",
                "pauseBeforeBridgePrompt": "3"}
        bridge = xm_sb.conference_bridges_endpoint().create_conference_bridge(data)
        assert isinstance(bridge, xmatters.objects.conference_bridges.ConferenceBridge)
        assert bridge.name == "INC-211 Zoom Conference"

    @pytest.mark.order(2)
    def test_get(self, xm_sb):
        bridges = xm_sb.conference_bridges_endpoint().get_conference_bridges()
        assert len(bridges) > 0
        assert iter(bridges)
        for bridge in bridges:
            assert bridge.id is not None

    @pytest.mark.order(3)
    def test_update(self, xm_sb):
        bridge = list(xm_sb.conference_bridges_endpoint().get_conference_bridges(name="INC-211 Zoom Conference"))[0]
        data = {"id": bridge.id,
                "name": "INC-211 Zoom Conference Updated"}
        mod_bridge = xm_sb.conference_bridges_endpoint().update_conference_bridge(data)
        assert isinstance(mod_bridge, xmatters.objects.conference_bridges.ConferenceBridge)
        assert mod_bridge.name == "INC-211 Zoom Conference Updated"

    @pytest.mark.order(4)
    def test_delete(self, xm_sb):
        bridge = list(xm_sb.conference_bridges_endpoint().get_conference_bridges(name="INC-211 Zoom Conference Updated"))[0]
        del_bridge = xm_sb.conference_bridges_endpoint().delete_conference_bridge(bridge_id=bridge.id)
        assert isinstance(del_bridge, xmatters.objects.conference_bridges.ConferenceBridge)
        assert del_bridge.name == "INC-211 Zoom Conference Updated"
        with pytest.raises(xmatters.errors.NotFoundError):
            xm_sb.conference_bridges_endpoint().get_conference_bridge_by_id(del_bridge.id)
