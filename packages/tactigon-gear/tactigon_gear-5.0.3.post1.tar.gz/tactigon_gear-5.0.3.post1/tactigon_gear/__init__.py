__version__ = "5.0.3.post1"
__all__ = ["TSkin", "TSkinConfig", "GestureConfig", "TSkinState", "Hand", "Touch", "Angle", "Gyro", "Acceleration", "Gesture", "OneFingerGesture", "TwoFingerGesture"]

import logging
from typing import Optional
from multiprocessing import Pipe
from multiprocessing.connection import _ConnectionBase

from .hal import BLE
from .middleware import Tactigon_Gesture
from .models import TBleSelector, Gesture, Touch, OneFingerGesture, TwoFingerGesture, Angle, Acceleration, Gyro, TSkinState, TSkinConfig, Hand, GestureConfig

class TSkin:
    logger: logging.Logger
    config: TSkinConfig

    ble: BLE
    tgesture: Tactigon_Gesture

    sensor_rx: Optional[_ConnectionBase] = None
    sensor_tx: Optional[_ConnectionBase] = None

    adpcm_rx: Optional[_ConnectionBase] = None
    adpcm_tx: Optional[_ConnectionBase] = None


    def __init__(self,
                config: TSkinConfig,
                debug: bool = False
                ):
        
        self.logger = logging.getLogger()
        self.logger.addHandler(logging.StreamHandler())

        if debug:
            self.logger.setLevel(logging.DEBUG)

        self.debug = debug
        self.config = config

        if self.config.gesture_config:
            self.sensor_rx, self.sensor_tx = Pipe(duplex=False)

            self.tgesture = Tactigon_Gesture(
                self.config.gesture_config,
                self.sensor_rx,
                self.logger,
            )

        self.ble = BLE(self.config.name, self.config.address, self.config.hand, self.logger, self.sensor_tx, None, self.adpcm_tx)

        self.logger.debug("[TSkin] Object create. Config: %s", self.config)
           
    def start(self):
        self.ble.start()

        if self.config.gesture_config:
            self.tgesture.start()

        self.logger.debug("[TSkin] TSkin %s (%s) started", self.config.name, self.config.address)

    def terminate(self):
        if self.config.gesture_config:
            self.tgesture.terminate()

        self.ble.terminate()

        self.logger.debug("[TSkin] TSkin %s (%s) terminated", self.config.name, self.config.address)

    def select_sensors(self) -> None:
        if self.debug:
            logging.info("[TSkin] TSkin %s (%s) select sensors stream.", self.config.name, self.config.address)
        return self.ble.select_sensors()
    
    def select_voice(self) -> None:
        if self.debug:
            logging.info("[TSkin] TSkin %s (%s) select voice stream.", self.config.name, self.config.address)
        return self.ble.select_voice()
    
    @property
    def selector(self) -> TBleSelector:
        return self.ble.selector
    
    @property
    def connected(self) -> bool:
        return self.ble.connected
    
    @property
    def gesture(self) -> Optional[Gesture]:
        if not self.config.gesture_config:
            return None
        
        return self.tgesture.gesture(reset=True)
    
    @property
    def gesture_preserve(self) -> Optional[Gesture]:
        if not self.config.gesture_config:
            return None
        
        return self.tgesture.gesture(reset=False)

   
    @property
    def angle(self) -> Optional[Angle]:
        return self.ble.angle
    
    @property
    def acceleration(self) -> Optional[Acceleration]:
        return self.ble.acceleration
    
    @property
    def gyro(self) -> Optional[Gyro]:
        return self.ble.gyro
    
    @property
    def touch(self) -> Optional[Touch]:
        return self.ble.touch
    
    @property
    def battery(self) -> float:
        return self.ble.battery
    
    @property
    def state(self) -> TSkinState:
        return TSkinState(
            self.connected,
            self.battery,
            self.ble.selector,
            self.touch,
            self.angle,
            self.gesture,
        )
    
    @property
    def state_preserve_gesture(self) -> TSkinState:
        s = self.ble.selector

        return TSkinState(
            self.connected,
            self.battery,
            self.ble.selector,
            self.touch,
            self.angle,
            self.gesture_preserve,
        )
    
    def __str__(self):
        return "TSkin(name='{0}', address='{1}', gesture={2})".format(self.config.name, self.config.address, self.config.gesture_config)