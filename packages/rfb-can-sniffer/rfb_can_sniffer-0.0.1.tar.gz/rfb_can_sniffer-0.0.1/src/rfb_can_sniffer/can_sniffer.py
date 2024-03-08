#!/usr/bin/python3
"""
This module will manage CAN messages and channels
in order to configure channels and send/received messages.
"""
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
from typing import List
#######################         GENERIC IMPORTS          #######################
from threading import Event
from enum import Enum
from can import ThreadSafeBus, Message, CanOperationError

#######################       THIRD PARTY IMPORTS        #######################

#######################    SYSTEM ABSTRACTION IMPORTS    #######################
from rfb_logger_tool import sys_log_logger_get_module_logger, SysLogLoggerC, Logger

#######################       LOGGER CONFIGURATION       #######################
if __name__ == '__main__':
    cycler_logger = SysLogLoggerC(file_log_levels='../log_config.yaml')
log: Logger = sys_log_logger_get_module_logger(__name__)

from rfb_shared_tool import SysShdIpcChanC, SysShdNodeC, SysShdNodeParamsC, SysShdNodeStatusE
#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################

######################             CONSTANTS              ######################
from .context import (DEFAULT_CHAN_NUM_MSG, DEFAULT_MAX_MSG_SIZE, DEFAULT_TIMEOUT_SEND_MSG,
                      DEFAULT_TIMEOUT_RX_MSG, DEFAULT_NODE_PERIOD, DEFAULT_NODE_NAME,
                      DEFAULT_TX_NAME, DEFAULT_IFACE_NAME, DEFAULT_IFACE_CHAN_NAME)


#######################              ENUMS               #######################


#######################             CLASSES              #######################
class _Constants:
    """
    Class to store constants used in the module.
    """
    MAX_DLC_SIZE : int = 8
    MIN_ID          = 0x000     # As the last 4 bits will identify the messages are reserved
    MAX_ID          = 0x7FF     # In standard mode the can id max value is 0x7FF
class DrvCanCmdTypeE(Enum):
    """
    Type of command for the CAN
    """
    MESSAGE = 0
    ADD_FILTER = 1
    REMOVE_FILTER = 2

class DrvCanMessageC:
    """The class to create messages correctly to be send by can .
    """
    def __init__(self, addr : int, size : int, payload : int | bytearray) -> None:
        '''
        Initialize a CAN message.

        Args:
            addr (int): CAN datafrane addres.
            size (int): Message payload size on bytes.
            data (int): Can message payload.

        Raises:
            BytesWarning: Throw an exception if the payload size of message is too long (size > 8).
        '''
        self.addr = addr
        self.dlc = size
        if self.dlc > _Constants.MAX_DLC_SIZE:
            log.error(f"Message payload size on bytes (size = {self.dlc}) \
                      is higher than {_Constants.MAX_DLC_SIZE}")
            raise BytesWarning("To many element for a CAN message")
        if isinstance(payload,int):
            self.payload = payload.to_bytes(size, byteorder='little', signed = False)
        else:
            self.payload = payload

class DrvCanFilterC:
    """This class is used to create objects that
    works as messages to make write or erase filters in can .
    """
    def __init__(self, addr : int, mask : int, chan_name: str):
        if _Constants.MIN_ID <= addr <= _Constants.MAX_ID:
            self.addr = addr
        else:
            log.error("Wrong value for address, value must be between 0-0x7ff")
            raise ValueError("Wrong value for address, value must be between 0-0x7ff")

        if _Constants.MIN_ID <= mask <= _Constants.MAX_ID:
            self.mask = mask
        else:
            log.error("Wrong value for mask, value must be between 0 and 0x7ff")
            raise ValueError("Wrong value for mask, value must be between 0 and 0x7ff")

        self.chan_name = chan_name

class _CanActiveFilterC(DrvCanFilterC):
    """This class is used to create objects that contains active filters.
    """
    def __init__(self, addr : int, mask : int, chan_name: str):
        super().__init__(addr, mask, chan_name)
        self.chan: SysShdIpcChanC = SysShdIpcChanC(name= self.chan_name, max_message_size= 150)

    def match(self, id_can: int) -> bool:
        """Checks if the id_can matches with the selected filter.

        Args:
            id_can (int): [complete id of the message received by can]
        """
        aux = False
        if (id_can & self.mask) == (self.addr & self.mask):
            aux = True
        return aux

    def close_chan(self):
        """Closes the communication channel.
        """
        log.debug(f"Closing channel {self.chan_name}")
        self.chan.terminate()

class DrvCanCmdDataC:
    """
    Returns a function that can be called when the command is not available .
    """
    def __init__(self, data_type: DrvCanCmdTypeE, payload: DrvCanMessageC|DrvCanFilterC):
        self.data_type = data_type
        self.payload = payload

class DrvCanNodeC(SysShdNodeC): #pylint: disable= abstract-method
    """Class to manage the CAN communication.
    """

    def __init__(self, working_flag : Event, tx_buffer_size: int= DEFAULT_CHAN_NUM_MSG,
                 name: str= DEFAULT_NODE_NAME,
                cycle_period: int = DEFAULT_NODE_PERIOD,
                can_params: SysShdNodeParamsC = SysShdNodeParamsC()) -> None:
        """ Initialize the CAN node.

        Args:
            tx_buffer_size (int): [description]
            working_flag (Event): [description]
            name (str, optional): [description]. Defaults to "CAN_NODE".
            cycle_period (int, optional): [Period in miliseconds]. Defaults to 100.
            can_params (SysShdNodeParamsC, optional): [description]. Defaults to SysShdNodeParamsC()
        """
        super().__init__(name=name, cycle_period=cycle_period, working_flag=working_flag,
                        node_params=can_params)
        self.working_flag = working_flag
        # cmd_can_down = 'sudo ip link set down can0'
        self.__can_bus : ThreadSafeBus = ThreadSafeBus(interface=DEFAULT_IFACE_NAME,
                                channel=DEFAULT_IFACE_CHAN_NAME, bitrate=125000,
                                receive_own_messages=False, fd=True)
        self.__can_bus.flush_tx_buffer()

        self.tx_buffer: SysShdIpcChanC = SysShdIpcChanC(name= DEFAULT_TX_NAME,
                                            max_msg = tx_buffer_size,
                                            max_message_size= DEFAULT_MAX_MSG_SIZE)

        self.__active_filter: List[_CanActiveFilterC] = []

    def __parse_msg(self, message: DrvCanMessageC) -> None:
        '''
        Check if the received message matches any of the active filter, in case it matches will
        add that message to the specific queue of the filter

        Args:
            message (DrvCanMessageC): Message received from CAN
        '''
        #Search if the message id match any active filter
        # if true, add the message to that queue
        for act_filter in self.__active_filter:
            if act_filter.match(message.addr):
                act_filter.chan.send_data(message)
                break

    def __apply_filter(self, add_filter : _CanActiveFilterC) -> None:
        '''Created a shared object and added it to the active filter list

        Args:
            data_frame (DrvCanFilterC): Filter to apply.
        '''
        already_in = False
        for act_filter in self.__active_filter:
            if act_filter.addr == add_filter.addr and act_filter.mask == add_filter.mask:
                already_in = True
                if act_filter.chan_name == add_filter.chan_name:
                    log.warning("Filter already added")
                else:
                    log.error("Filter already added with different channel name")
                    raise ValueError("Filter already added with different channel name")
        if not already_in:
            log.info(f"Adding new filter with id {hex(add_filter.addr)} "+
            f"and mask {hex(add_filter.mask)}")
            self.__active_filter.append(add_filter)
            log.debug("Filter added correctly")

    def __remove_filter(self, del_filter : DrvCanFilterC) -> None:
        '''Delete a shared object from the active filter list

        Args:
            del_filter (DrvCanFilterC): Filter to remove.
        '''
        already_out = True
        filter_pos=0
        for act_filter in self.__active_filter:
            if act_filter.addr == del_filter.addr and act_filter.mask == del_filter.mask:
                already_out = False
                if act_filter.chan_name == del_filter.chan_name:
                    log.info(f"Removing filter with id {hex(del_filter.addr)} "+
                        f"and mask {hex(del_filter.mask)}")
                    filter_chn: _CanActiveFilterC = self.__active_filter.pop(filter_pos)
                    filter_chn.close_chan()
                    log.debug("Filter removed correctly")
                else:
                    log.error("Filter in with different channel name")
                    raise ValueError("Filter already added with different channel name")
            else:
                filter_pos += 1
        if already_out:
            log.warning("Filter already removed")

    def __send_message(self, data : DrvCanMessageC) -> None:
        '''Send a CAN message

        Args:
            data (DrvCanMessageC): Messsage to send.

        Raises:
            err (CanOperationError): Raised when error with CAN connection occurred
        '''
        msg = Message(arbitration_id=data.addr, is_extended_id=False,
                    dlc=data.dlc, data=bytes(data.payload))
        try:
            self.__can_bus.send(msg, timeout=DEFAULT_TIMEOUT_SEND_MSG)
            log.debug("Message correctly send")
        except CanOperationError as err:
            log.error(err)
            raise err
        # log.debug(f"CAN Message sent: \tarbitration_id :
        # {msg.arbitration_id:04X} \tdlc : {msg.dlc} \tdata :
        # 0x{data_frame.data}, 0x{data_frame.data.hex()}")

    def __apply_command(self, command : DrvCanCmdDataC) -> None:
        '''Apply a command to the CAN drv of the device.

        Args:
            command (DrvCanCmdDataC): Data to process, does not know if its for the channel or
            a message to a device

        Raises:
            err (CanOperationError): Raised when error with CAN connection occurred
        '''
        #Check which type of command has been received and matchs the payload type
        if (command.data_type == DrvCanCmdTypeE.MESSAGE
            and isinstance(command.payload,DrvCanMessageC)):
            self.__send_message(command.payload)
        elif (command.data_type == DrvCanCmdTypeE.ADD_FILTER
            and isinstance(command.payload,DrvCanFilterC)):
            self.__apply_filter(_CanActiveFilterC(**command.payload.__dict__))
        elif (command.data_type == DrvCanCmdTypeE.REMOVE_FILTER
            and isinstance(command.payload,DrvCanFilterC)):
            self.__remove_filter(command.payload)
        else:
            log.error("Can`t apply command. \
                      Error in command format, check command type and payload type")


    def stop(self) -> None:
        """
        Stop the CAN thread .
        """
        log.critical("Stopping CAN thread.")
        for filters in self.__active_filter:
            filters.close_chan()
        self.working_flag.clear()
        self.tx_buffer.terminate()
        self.__can_bus.shutdown()
        self.status = SysShdNodeStatusE.STOP

    def process_iteration(self) -> None:
        '''
        Main method executed by the CAN thread. It receive data from EPCs and PLAKs
        and store it on the corresponding chan.
        '''
        log.debug(f"CAN thread status {self.status}")
        try:
            if not self.tx_buffer.is_empty():
                # Ignore warning as receive_data return an object,
                # which in this case must be of type DrvCanCmdDataC
                command : DrvCanCmdDataC = self.tx_buffer.receive_data() # type: ignore
                log.debug(f"Command to apply: {command.data_type.name}")
                self.__apply_command(command)
                self.status = SysShdNodeStatusE.OK
            msg : Message = self.__can_bus.recv(timeout=DEFAULT_TIMEOUT_RX_MSG)
            if isinstance(msg,Message):
                if (_Constants.MIN_ID <= msg.arbitration_id <= _Constants.MAX_ID
                    and not msg.is_error_frame):
                    self.__parse_msg(DrvCanMessageC(msg.arbitration_id,msg.dlc,msg.data))
                else:
                    log.error(f"Message receive can`t be parsed, id: {hex(msg.arbitration_id)}"+
                                f" and error in frame is: {msg.is_error_frame}")
        except CanOperationError as err:
            log.error(f"Error while sending CAN message\n{err}")
            self.status = SysShdNodeStatusE.COMM_ERROR
        except ValueError as err:
            log.error(f"Error while applying/removing filter with error {err}")
            self.status = SysShdNodeStatusE.COMM_ERROR
        except Exception:
            log.error("Error in can thread")
            self.status = SysShdNodeStatusE.INTERNAL_ERROR
            self.working_flag.clear()
#######################            FUNCTIONS             #######################
