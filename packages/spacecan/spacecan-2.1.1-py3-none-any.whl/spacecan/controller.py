import json

from .network import Network
from .heartbeat import HeartbeatProducer
from .sync import SyncProducer
from .packet import PacketAssembler
from .can_frame import CanFrame, FUNCTION_MASK, ID_TM, ID_TC, ID_SCET, ID_UTC, ID_SYNC


class Controller:
    def __init__(
        self, interface, channel_a, channel_b, heartbeat_period=None, sync_period=None
    ):
        self.node_id = 0  # controller node id is always 0
        self.interface = interface
        self.channel_a = channel_a
        self.channel_b = channel_b
        self.heartbeat_period = heartbeat_period
        self.sync_period = sync_period

        self.network = None
        self.heartbeat = HeartbeatProducer(self) if heartbeat_period else None
        self.sync = SyncProducer(self) if self.sync_period else None

        self.received_heartbeat = None
        self.received_telemetry = None
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
            config.get("heartbeat_period"),
            config.get("sync_period"),
        )

    def connect(self):
        if self.interface == "socketcan":
            from .bus.socketcan import SocketCanBus

            bus_a = SocketCanBus(self, channel=self.channel_a)
            bus_b = SocketCanBus(self, channel=self.channel_b)
            # receive telemetry from all responder nodes
            filters = [{"can_id": ID_TM, "can_mask": FUNCTION_MASK}]
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
            self.heartbeat.start(self.heartbeat_period)
        if self.sync:
            self.sync.start(self.sync_period)

    def stop(self):
        if self.sync:
            self.sync.stop()
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

    def send_scet(self, coarse_time, fine_time=0, precision=8):
        can_id = ID_SCET
        if precision == 8:
            fine_time = fine_time << 16
        elif precision == 16:
            fine_time = fine_time << 8
        data = bytearray(
            [
                fine_time >> 16,
                (fine_time >> 8) & 0xFF,
                fine_time & 0xFF,
                coarse_time >> 24,
                (coarse_time >> 16) & 0xFF,
                (coarse_time >> 8) & 0xFF,
                coarse_time & 0xFF,
            ]
        )
        can_frame = CanFrame(can_id, data)
        self.network.send(can_frame)

    def send_utc(self, day, ms_of_day, sub_ms=0):
        can_id = ID_UTC
        data = bytearray(
            [
                sub_ms >> 8,
                sub_ms & 0xFF,
                ms_of_day >> 24,
                (ms_of_day >> 16) & 0xFF,
                (ms_of_day >> 8) & 0xFF,
                ms_of_day & 0xFF,
                day >> 8,
                day & 0xFF,
            ]
        )
        can_frame = CanFrame(can_id, data)
        self.network.send(can_frame)

    def send_sync(self):
        can_id = ID_SYNC
        can_frame = CanFrame(can_id, bytearray())
        self.network.send(can_frame)

    def send_telecommand(self, data, node_id):
        can_id = ID_TC + node_id
        can_frame = CanFrame(can_id, data)
        self.network.send(can_frame)

    def send_packet(self, packet, node_id):
        can_id = ID_TC + node_id
        for data in packet.split():
            can_frame = CanFrame(can_id, data)
            self.network.send(can_frame)

    def frame_received(self, can_frame):
        func_id = can_frame.get_func_id()
        node_id = can_frame.get_node_id()

        # controller should only receive telemetry from other nodes
        if func_id == ID_TM:
            if self.received_telemetry is not None:
                self.received_telemetry(can_frame.data, node_id)
            elif self.received_packet is not None:
                packet = self.packet_assembler.process_frame(can_frame)
                if packet is not None:
                    self.received_packet(packet.data, node_id)
        else:
            print(can_frame)
