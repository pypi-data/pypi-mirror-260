import json

from .network import Network
from .heartbeat import HeartbeatConsumer
from .packet import PacketAssembler
from .can_frame import (
    CanFrame,
    FULL_MASK,
    ID_SYNC,
    ID_HEARTBEAT,
    ID_TC,
    ID_TM,
    ID_SCET,
    ID_UTC,
)


class Responder:
    def __init__(
        self,
        interface,
        channel_a,
        channel_b,
        node_id,
        period_heartbeat=None,
        max_miss_heartbeat=3,
        max_bus_switch=None,
    ):
        if node_id == 0 or node_id > 127:
            raise ValueError("node id must be in range 1..127")
        self.node_id = node_id
        self.interface = interface
        self.channel_a = channel_a
        self.channel_b = channel_b
        self.period_heartbeat = period_heartbeat
        self.max_miss_heartbeat = max_miss_heartbeat
        self.max_bus_switch = max_bus_switch

        self.network = None
        self.heartbeat = HeartbeatConsumer(self) if period_heartbeat else None

        self.received_heartbeat = None
        self.received_sync = None
        self.received_scet = None
        self.received_utc = None
        self.received_telecommand = None
        self.received_packet = None
        self.packet_assembler = PacketAssembler(self)

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            config = json.load(f)

        return cls(
            config.get("interface"),
            config.get("channel_a"),
            config.get("channel_b"),
            config.get("node_id"),
            config.get("heartbeat_period"),
            config.get("max_miss_heartbeat"),
            config.get("max_bus_switch"),
        )

    def connect(self):
        if self.interface == "socketcan":
            from .bus.socketcan import SocketCanBus

            bus_a = SocketCanBus(self, channel=self.channel_a)
            bus_b = SocketCanBus(self, channel=self.channel_b)
            # receive sync, heartbeat, and telecommands from controller node
            filters = [
                {"can_id": ID_HEARTBEAT, "can_mask": FULL_MASK},
                {"can_id": ID_SYNC, "can_mask": FULL_MASK},
                {"can_id": ID_SCET, "can_mask": FULL_MASK},
                {"can_id": ID_UTC, "can_mask": FULL_MASK},
                {"can_id": ID_TC + self.node_id, "can_mask": FULL_MASK},
            ]
            bus_a.set_filters(filters)
            bus_b.set_filters(filters)
            self.network = Network(self, self.node_id, bus_a, bus_b)
        else:
            raise NotImplementedError

    def disconnect(self):
        self.network.bus_a.disconnect()
        self.network.bus_b.disconnect()

    def start(self):
        self.network.start()
        if self.heartbeat:
            self.heartbeat.start(
                self.period_heartbeat, self.max_miss_heartbeat, self.max_bus_switch
            )

    def stop(self):
        if self.heartbeat:
            self.heartbeat.stop()
        self.network.stop()

    def switch_bus(self):
        self.network.stop()
        if self.network.selected_bus == self.network.bus_a:
            self.network.selected_bus = self.network.bus_b
        elif self.network.selected_bus == self.network.bus_b:
            self.network.selected_bus = self.network.bus_a
        self.network.start()
        self.on_bus_switch()

    def on_bus_switch(self):
        # to be overwritten
        pass

    def send_telemetry(self, data):
        can_id = ID_TM + self.node_id
        can_frame = CanFrame(can_id, data)
        self.network.send(can_frame)

    def send_packet(self, packet):
        can_id = ID_TM + self.node_id
        for data in packet.split():
            can_frame = CanFrame(can_id, data)
            self.network.send(can_frame)

    def frame_received(self, can_frame):
        func_id = can_frame.get_func_id()
        node_id = can_frame.get_node_id()

        if func_id == ID_HEARTBEAT:
            if self.heartbeat:
                self.heartbeat.received()

        elif func_id == ID_SYNC:
            if self.received_sync is not None:
                self.received_sync()

        elif func_id == ID_SCET:
            if self.received_scet is not None:
                self.received_scet(can_frame.data)

        elif func_id == ID_UTC:
            if self.received_utc is not None:
                self.received_utc(can_frame.data)

        # responder node receives TC
        elif func_id == ID_TC and node_id == self.node_id:
            if self.received_telecommand is not None:
                self.received_telecommand(can_frame.data)
            elif self.received_packet is not None:
                packet = self.packet_assembler.process_frame(can_frame)
                if packet is not None:
                    self.received_packet(packet.data, node_id)
