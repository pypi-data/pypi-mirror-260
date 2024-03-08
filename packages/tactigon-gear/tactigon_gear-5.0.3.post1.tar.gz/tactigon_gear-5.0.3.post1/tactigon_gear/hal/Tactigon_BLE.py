import asyncio
from bleak import BleakClient
import struct
import time
import math
import ctypes
import logging

from multiprocessing import Process, Value
from multiprocessing.connection import _ConnectionBase
from multiprocessing.sharedctypes import SynchronizedBase
from typing import Optional

from ..models import Hand, Angle, Gyro, Touch, OneFingerGesture, TwoFingerGesture, Acceleration, TBleConnectionStatus, TBleSelector

class BLE(Process):
    SENSORS_UUID: str = "bea5760d-503d-4920-b000-101e7306b005"
    TOUCHPAD_UUID: str =    "bea5760d-503d-4920-b000-101e7306b009"
    VOICE_DATA_UUID = "08000000-0001-11e1-ac36-0002a5d5c51b"
    VOICE_SYNCH_UUID = "40000000-0001-11e1-ac36-0002a5d5c51b"

    logger: logging.Logger

    ble_address: str
    hand: Hand
    is_running: SynchronizedBase
    connection_status: SynchronizedBase
    _selector: SynchronizedBase

    _roll: SynchronizedBase
    _pitch: SynchronizedBase
    _yaw: SynchronizedBase

    _accX: SynchronizedBase
    _accY: SynchronizedBase
    _accZ: SynchronizedBase

    _gyroX: SynchronizedBase
    _gyroY: SynchronizedBase
    _gyroZ: SynchronizedBase

    _one_finger: SynchronizedBase
    _two_finger: SynchronizedBase
    _x_pos: SynchronizedBase
    _y_pos: SynchronizedBase

    _battery: SynchronizedBase

    def __init__(self, 
                name: str, 
                ble_address: str,
                hand: Hand,
                logger: logging.Logger,
                sensor_pipe: Optional[_ConnectionBase] = None, 
                angle_pipe: Optional[_ConnectionBase] = None, 
                adpcm_pipe: Optional[_ConnectionBase] = None,
                debug_data: bool = False):

        self.logger = logger

        self.ble_address = ble_address
        self.hand = hand
        self.is_running = Value(ctypes.c_bool, True)
        self.connection_status = Value(ctypes.c_byte, TBleConnectionStatus.NONE.value)
        self._selector = Value(ctypes.c_byte, TBleSelector.SENSORS.value)

        self._roll = Value(ctypes.c_float, 0)
        self._pitch = Value(ctypes.c_float, 0)
        self._yaw = Value(ctypes.c_float, 0)

        self._accX = Value(ctypes.c_float, 0)
        self._accY = Value(ctypes.c_float, 0)
        self._accZ = Value(ctypes.c_float, 0)

        self._gyroX = Value(ctypes.c_float, 0)
        self._gyroY = Value(ctypes.c_float, 0)
        self._gyroZ = Value(ctypes.c_float, 0)

        self._one_finger = Value(ctypes.c_int, 0)
        self._two_finger = Value(ctypes.c_int, 0)
        self._x_pos = Value(ctypes.c_float, 0)
        self._y_pos = Value(ctypes.c_float, 0)

        self._battery = Value(ctypes.c_int, 0)

        super().__init__(
            target=self._init_, 
            args=(
                name,
                ble_address,
                hand,
                sensor_pipe,
                angle_pipe,
                adpcm_pipe,
                self.connection_status,
                self.is_running,
                self._selector,
                self._roll,
                self._pitch,
                self._yaw,
                self._accX,
                self._accY,
                self._accZ,
                self._gyroX,
                self._gyroY,
                self._gyroZ,
                self._one_finger,
                self._two_finger,
                self._x_pos,
                self._y_pos,
                self._battery,
                self.logger.level,
                debug_data
            )
        )

    def _init_(self,
                name: str, 
                ble_address: str,
                hand: Hand,
                sensor_pipe: Optional[_ConnectionBase], 
                angle_pipe: Optional[_ConnectionBase],
                adpcm_pipe: Optional[_ConnectionBase],
                connection_status: SynchronizedBase,
                is_running: SynchronizedBase,
                selector: SynchronizedBase,
                _roll: SynchronizedBase,
                _pitch: SynchronizedBase,
                _yaw: SynchronizedBase,
                _accX: SynchronizedBase,
                _accY: SynchronizedBase,
                _accZ: SynchronizedBase,
                _gyroX: SynchronizedBase,
                _gyroY: SynchronizedBase,
                _gyroZ: SynchronizedBase,
                _one_finger: SynchronizedBase,
                _two_finger: SynchronizedBase,
                _x_pos: SynchronizedBase,
                _y_pos: SynchronizedBase,
                _battery: SynchronizedBase,
                logger_level: int,
                debug_data: bool = False
            ):

        self.logger = logging.getLogger()
        self.logger.setLevel(logger_level)
        self.logger.addHandler(logging.StreamHandler())
        self.debug_data = debug_data

        self.name = name
        self.ble_address = ble_address
        self.hand = hand
        self.sensor_pipe = sensor_pipe
        self.angle_pipe = angle_pipe
        self.adpcm_pipe = adpcm_pipe
        self.connection_status = connection_status
        self.is_running = is_running

        self._roll = _roll
        self._pitch = _pitch
        self._yaw = _yaw
        self._accX = _accX
        self._accY = _accY
        self._accZ = _accZ
        self._gyroX = _gyroX
        self._gyroY = _gyroY
        self._gyroZ = _gyroZ
        self._one_finger = _one_finger
        self._two_finger = _two_finger
        self._x_pos = _x_pos
        self._y_pos = _y_pos
        self._battery = _battery

        self._selector = selector

        # self.adpcm_audio = FeatureAudioADPCM(None)
        self._selector = selector

        self.loop = asyncio.get_event_loop()
        main_task = self.loop.create_task(self._run())
        self.loop.run_until_complete(main_task)

    async def _run(self):
        self.logger.debug("[BLE] Main process initialized for %s (%s)", self.name, self.ble_address)

        def handle_voice_sync(char, data: bytearray):
            pass

        def handle_voice(char, data: bytearray):
            if self.adpcm_pipe:
                self.adpcm_pipe.send(data)

        def handle_sensors(char, data:bytearray):
            accX = float(struct.unpack("h", data[0:2])[0])
            accY = float(struct.unpack("h", data[2:4])[0])
            accZ = float(struct.unpack("h", data[4:6])[0])
            
            gyroX = float(struct.unpack("h", data[6:8])[0])
            gyroY = float(struct.unpack("h", data[8:10])[0])
            gyroZ = float(struct.unpack("h", data[10:12])[0])
            
            roll = float(struct.unpack("h", data[12:14])[0])
            pitch = float(struct.unpack("h", data[14:16])[0])
            yaw = float(struct.unpack("h", data[16:18])[0])

            battery = int(struct.unpack("h", data[18:20])[0])

            accX, accY, accZ, gyroX, gyroY, gyroZ, roll, pitch, yaw = BLE.gravity_comp(self.hand, accX, accY, accZ, gyroX, gyroY, gyroZ, roll, pitch, yaw)

            if self.debug_data:
                self.logger.debug("[BLE] Device %s (%s) | accX:%f accY:%f accZ:%f gyroX:%f gyroY:%f gyroZ:%f roll:%f pitch:%f yaw:%f battery:%i", 
                    self.name,
                    self.ble_address,
                    accX, 
                    accY, 
                    accZ,
                    gyroX,
                    gyroY,
                    gyroZ,
                    roll,
                    pitch,
                    yaw,
                    battery                
                    )

            with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
                self._roll.get_obj().value = roll
                self._pitch.get_obj().value = pitch
                self._yaw.get_obj().value = yaw

            with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
                self._accX.get_obj().value = accX
                self._accY.get_obj().value = accY
                self._accZ.get_obj().value = accZ

            with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
                self._gyroX.get_obj().value = gyroX
                self._gyroY.get_obj().value = gyroY
                self._gyroZ.get_obj().value = gyroZ

            with self._battery.get_lock():
                self._battery.get_obj().value = battery

            if self.sensor_pipe:
                self.sensor_pipe.send([accX, accY, accZ, gyroX, gyroY, gyroZ])
            
            if self.angle_pipe:
                self.angle_pipe.send([roll, pitch, yaw])

        def handle_touchpad(char, data: bytearray):
            
            with self._one_finger.get_lock() and self._two_finger.get_lock() and self._x_pos.get_lock() and self._y_pos.get_lock():
                self._one_finger.get_obj().value = int.from_bytes(data[0:1], "big")
                self._two_finger.get_obj().value = int.from_bytes(data[1:2], "big")
                self._x_pos.get_obj().value = float(struct.unpack("h", data[2:4])[0])
                self._y_pos.get_obj().value = float(struct.unpack("h", data[4:6])[0])

            if self.debug_data:
                self.logger.debug("[BLE-Touch] b1 %s b2 %s x %s y %s", 
                    data[0:1], 
                    data[1:2], 
                    float(struct.unpack("h", data[2:4])[0]),
                    float(struct.unpack("h", data[4:6])[0])
                )
        
        if self.is_running is None:
            raise Exception("is_running parameter should be a multiprocessing.Value")
        
        if self.connection_status is None:
            raise Exception("connection_status parameter should be a multiprocessing.Value")
        
        if self._selector is None:
            raise Exception("selector parameter should be a multiprocessing.Value")

        doing: bool = True
        current_selector: TBleSelector = TBleSelector.NONE
        client = None

        is_notifying_sensors: bool = False
        is_notifying_voice: bool = False

        while doing:
            with self.connection_status.get_lock():
                self.connection_status.get_obj().value = TBleConnectionStatus.CONNECTING.value
            
            try:
                self.logger.info("[BLE] Connecting to %s (%s)", self.name, self.ble_address)
                client = BleakClient(self.ble_address)
                await client.connect()
                
                with self.connection_status.get_lock():
                    self.connection_status.get_obj().value = TBleConnectionStatus.CONNECTED.value
                
                current_selector = TBleSelector.NONE
                is_notifying_sensors = False
                is_notifying_voice = False
                self.logger.info("[BLE] Connected to %s!", self.ble_address)

            except:
                client = None
                self.logger.info("[BLE] Cannot connect to %s (%s). Retry...", self.name, self.ble_address)
                time.sleep(2)
                continue

            await client.start_notify(self.TOUCHPAD_UUID, handle_touchpad)

            while client.is_connected:
                _running: bool
                with self.is_running.get_lock():
                    _running = self.is_running.get_obj().value

                if not _running:
                    with self.connection_status.get_lock():
                        self.connection_status.get_obj().value = TBleConnectionStatus.DISCONNECTING.value
                    
                    await client.disconnect()
                    
                    with self.connection_status.get_lock():
                        self.connection_status.get_obj().value = TBleConnectionStatus.DISCONNECTED.value
                    
                    doing = False
                    break

                _selector: TBleSelector
                with self._selector.get_lock():
                    _selector = TBleSelector(self._selector.get_obj().value)

                if current_selector != _selector:
                    current_selector = _selector

                    if is_notifying_sensors:
                        await client.stop_notify(self.SENSORS_UUID)
                        is_notifying_sensors = False
                        self.logger.debug("[BLE] Stopped notification on sensors (%s)", self.SENSORS_UUID)

                    if is_notifying_voice:
                        await client.stop_notify(self.VOICE_DATA_UUID)
                        await client.stop_notify(self.VOICE_SYNCH_UUID)
                        is_notifying_voice = False
                        self.logger.debug("[BLE] Stopped notification on voice (%s %s)", self.VOICE_SYNCH_UUID, self.VOICE_DATA_UUID)
                    
                    if current_selector == TBleSelector.SENSORS:
                        if client.is_connected:
                            
                            await client.start_notify(self.SENSORS_UUID, handle_sensors)
                            is_notifying_sensors = True
                            self.logger.debug("[BLE] Started notification on sensors (%s)", self.SENSORS_UUID)

                    elif current_selector == TBleSelector.VOICE:
                        if client.is_connected:
                            await client.start_notify(self.VOICE_SYNCH_UUID, handle_voice_sync)
                            await client.start_notify(self.VOICE_DATA_UUID, handle_voice)
                            is_notifying_voice = True
                            self.logger.debug("[BLE] Started notification on voice (%s %s)", self.VOICE_SYNCH_UUID, self.VOICE_DATA_UUID)
                else:
                    await asyncio.sleep(0.02)
        if client:
            await client.disconnect()
            self.logger.info("[BLE] Device %s (%s) disconnected", self.name, self.ble_address)

        self.logger.debug("[BLE] Main process stopped for %s (%s)", self.name, self.ble_address)

    @staticmethod
    def gravity_comp(hand: Hand, accX: float, accY: float, accZ: float, gyroX: float, gyroY: float, gyroZ: float, roll: float, pitch: float, yaw: float):
        """gravity compensation"""
        G_CONST = 9.81
        ANG_TO_RAD = math.pi / 180
        ACC_RATIO = 1000
        VEL_RATIO = 30

        if hand == Hand.LEFT:
            accX = -accX / ACC_RATIO
            accY = -accY / ACC_RATIO
            accZ = -accZ / ACC_RATIO

            gyroX = -gyroX / VEL_RATIO
            gyroY = -gyroY / VEL_RATIO
            gyroZ = -gyroZ / VEL_RATIO

            _pitch = roll * ANG_TO_RAD
            _roll = pitch * ANG_TO_RAD

        else:
            accX = accX / ACC_RATIO
            accY = accY / ACC_RATIO
            accZ = -accZ / ACC_RATIO

            gyroX = gyroX / VEL_RATIO
            gyroY = gyroY / VEL_RATIO
            gyroZ = -gyroZ / VEL_RATIO

            _pitch = -roll * ANG_TO_RAD
            _roll = -pitch * ANG_TO_RAD

        if accZ == 0:
            beta = math.pi / 2
        else:
            beta = math.atan(
                math.sqrt(math.pow(accX, 2) + math.pow(accY, 2)) / accZ
            )

        accX = accX - G_CONST * math.sin(_roll)
        accY = accY + G_CONST * math.sin(_pitch)
        accZ = accZ - G_CONST * math.cos(beta)

        return accX, accY, accZ, gyroX, gyroY, gyroX, roll, pitch, yaw

    def start(self):
        self.logger.debug("[BLE] BLE starting on address %s", self.ble_address)
        super().start()

    def terminate(self):
        self.logger.debug("[BLE] Stopping BLE on address %s", self.ble_address)
        with self.is_running.get_lock():
            self.is_running.get_obj().value = False
        
        super().join(10)
        super().terminate()

    def select_sensors(self):

        with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
            self._roll.get_obj().value = 0
            self._pitch.get_obj().value = 0
            self._yaw.get_obj().value = 0

        with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
            self._accX.get_obj().value = 0
            self._accY.get_obj().value = 0
            self._accZ.get_obj().value = 0

        with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
            self._gyroX.get_obj().value = 0
            self._gyroY.get_obj().value = 0
            self._gyroZ.get_obj().value = 0

        with self._selector.get_lock():
            self._selector.get_obj().value = TBleSelector.SENSORS.value

        self.logger.debug("[BLE] Selected sensors stream from address %s", self.ble_address)

    def select_voice(self):
        with self._selector.get_lock():
            self._selector.get_obj().value = TBleSelector.VOICE.value
        
        self.logger.debug("[BLE] Selected voice stream from address %s", self.ble_address)

    def select(self, selector: TBleSelector = TBleSelector.NONE):
        with self._selector.get_lock():
            self._selector.get_obj().value = selector.value

        self.logger.debug("[BLE] Selected %s stream from address %s", selector, self.ble_address)

    @property
    def selector(self) -> TBleSelector:
        with self._selector.get_lock():
            return TBleSelector(self._selector.get_obj().value)

    @property
    def connected(self) -> bool:
        with self.connection_status.get_lock():
            return TBleConnectionStatus(self.connection_status.get_obj().value) == TBleConnectionStatus.CONNECTED
    
    @property
    def angle(self) -> Optional[Angle]:
        if self.selector == TBleSelector.SENSORS:
            with self._roll.get_lock() and self._pitch.get_lock() and self._yaw.get_lock():
                return Angle(
                    self._roll.get_obj().value,
                    self._pitch.get_obj().value,
                    self._yaw.get_obj().value,
                )
            
        return None

    @property
    def gyro(self) -> Optional[Gyro]:
        if self.selector == TBleSelector.SENSORS:
            with self._gyroX.get_lock() and self._gyroY.get_lock() and self._gyroZ.get_lock():
                return Gyro(
                    self._gyroX.get_obj().value,
                    self._gyroY.get_obj().value,
                    self._gyroZ.get_obj().value,
                )
            
        return None

    @property
    def acceleration(self) -> Optional[Acceleration]:
        if self.selector == TBleSelector.SENSORS:
            with self._accX.get_lock() and self._accY.get_lock() and self._accZ.get_lock():
                return Acceleration(
                    self._accX.get_obj().value,
                    self._accY.get_obj().value,
                    self._accZ.get_obj().value,
                )
            
        return None
    
    @property
    def touch(self) -> Optional[Touch]:
        with self._one_finger.get_lock() and self._two_finger.get_lock() and self._x_pos.get_lock() and self._y_pos.get_lock():

            one_finger_g = OneFingerGesture(self._one_finger.get_obj().value)
            two_finger_g = TwoFingerGesture(self._two_finger.get_obj().value)
            x_p = self._x_pos.get_obj().value
            y_p = self._y_pos.get_obj().value

            self._one_finger.get_obj().value = 0
            self._two_finger.get_obj().value = 0
            self._x_pos.get_obj().value = 0
            self._y_pos.get_obj().value = 0

        if one_finger_g == OneFingerGesture.NONE and two_finger_g == TwoFingerGesture.NONE:
            return None
        
        return Touch(one_finger_g, two_finger_g, x_p, y_p)
    
    @property
    def battery(self) -> float:
        with self._battery.get_lock():
            return round(self._battery.get_obj().value / 1000, 2)