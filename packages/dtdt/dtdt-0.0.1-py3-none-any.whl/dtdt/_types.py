import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, IntEnum, StrEnum
from typing import Any, Dict, List, Tuple, Union

import numpy as np
from pydantic import BaseModel


class TankEventType(IntEnum):
    UNKNOWN = int("00000000", 16)
    STRON = int("00000101", 16)
    STROFF = int("00000102", 16)
    SCALAR = int("00000201", 16)
    STREAM = int("00008101", 16)
    SNIP = int("00008201", 16)
    MARK = int("00008801", 16)
    HASDATA = int("00008000", 16)
    UCF = int("00000010", 16)
    PHANTOM = int("00000020", 16)
    MASK = int("0000FF0F", 16)
    INVALID_MASK = int("FFFF0000", 16)


class EventMarker(IntEnum):
    STARTBLOCK = int("0001", 16)
    STOPBLOCK = int("0002", 16)


class AllowedFormats(Enum):
    FLOAT = np.float32
    LONG = np.int32
    SHORT = np.int16
    BYTE = np.int8
    DOUBLE = np.float64
    QWORD = np.int64


class DataFormatEnum(IntEnum):
    FLOAT = 0
    LONG = 1
    SHORT = 2
    BYTE = 3
    DOUBLE = 4
    QWORD = 5
    TYPE_COUNT = 6

    def to_np(self):
        if self.name in [x.name for x in AllowedFormats]:
            return AllowedFormats[self.name].value
        else:
            raise ValueError(f"DataFormatEnum {self.name} not in AllowedFormats")


class AllowedEvtypes(StrEnum):
    ALL = "all"
    EPOCS = "epocs"
    SNIPS = "snips"
    STREAMS = "streams"
    SCALARS = "scalars"



class StoreType(BaseModel):
    CircType: int = 0
    DataFormat: DataFormatEnum = DataFormatEnum.DOUBLE
    Enabled: bool = False
    HeadName: str = ""
    NumChan: int = 0
    NumPoints: int = 0
    SampleFreq: float = 0
    SecTag: str = ""
    StoreName: str = ""
    StrobeBuddy: str = ""
    StrobeMode: int = 0
    TankEvType: int = 0


class EventHeader(BaseModel):
    name: str = ""
    type: str = ""
    start_time: List[float] = []
    type_str: AllowedEvtypes = AllowedEvtypes.EPOCS
    size: int = 0

    def __repr__(self):
        return f"""
name: {self.name}
type: {self.type}
start_time: {self.start_time}
type_str: {self.type_str}
size: {self.size}
"""

    def __str__(self):
        return self.__repr__()


class TDTNote(BaseModel):
    name: List = []
    index: List = []
    text: List = []
    ts: List = []


class TDTDataHeader(BaseModel):
    tev_path: str = ""
    start_time: Union[float, None] = None
    stop_time: Union[float, None] = None


class Event(BaseModel):
    header: EventHeader = EventHeader()
    ts: np.ndarray = np.array([])
    data: np.ndarray = np.array([])
    code: int = 0
    dform: DataFormatEnum = DataFormatEnum.DOUBLE

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return (
            str(self.header)
            + f"""ts: {self.ts}
data: {self.data}
code: {self.code}
dform: {self.dform}
    """
        )

    def __str__(self):
        return self.__repr__()


class TDTEpoc(Event):
    buddy: str = ""
    onset: np.ndarray = np.array([])
    offset: np.ndarray = np.array([])
    notes: List[TDTNote] = []

    def __repr__(self):
        super().__repr__()
        return (
            str(self.header)
            + f"""onset: {self.onset}
offset: {self.offset}
    """
        )


class TDTSnip(Event):
    fs: np.double = 0.0
    chan: np.ndarray = np.array([])
    sortcode: np.ndarray = np.array([])
    sortname: str = ""
    sortchannels: np.ndarray = np.array([])

    def __repr__(self):
        super().__repr__()
        return (
            str(self.header)
            + f"""fs: {self.fs}
chan: {self.chan}
sortcode: {self.sortcode}
sortname: {self.sortname}
sortchannels: {self.sortchannels}
"""
        )


class TDTStream(Event):
    ucf: bool = False
    fs: np.double = 0.0
    chan: np.ndarray = np.array([])

    def __repr__(self):
        super().__repr__()
        return (
            str(self.header)
            + f"""ucf: {self.ucf}
fs: {self.fs}
chan: {self.chan}
"""
        )


class TDTScalar(Event):
    chan: List = []
    notes: List[TDTNote] = []

    def __repr__(self):
        super().__repr__()
        return (
            str(self.header)
            + f"""chan: {self.chan}
notes: {self.notes}
"""
        )


class TDTInfo(Event):
    tankpath: str = ""
    blockname: str = ""
    start_date: datetime = datetime.now()
    utc_start_time: Union[str, None] = None
    stop_date: Union[datetime, None] = None
    utc_stop_time: Union[str, None] = None
    duration: Union[timedelta, None] = None
    stream_channel: int = 0
    snip_channel: int = 0
    experiment: str = ""
    subject: str = ""
    user: str = ""
    start: str = ""
    stop: str = ""

    def __repr__(self):
        return f"""
tankpath: {self.tankpath}
blockname: {self.blockname}
start_date: {self.start_date}
utc_start_time: {self.utc_start_time}
stop_date: {self.stop_date}
utc_stop_time: {self.utc_stop_time}
duration: {self.duration}
stream_channel: {self.stream_channel}
snip_channel: {self.snip_channel}
experiment: {self.experiment}
subject: {self.subject}
user: {self.user}
start: {self.start}
stop: {self.stop}
"""

    def __str__(self):
        return self.__repr__()


class DynamicDictAccessor(dict):
    """
    A Dict that allows access to the list items by their attribute names. This is bad practice and should be avoided but to keep the TDTData struct access simmilar to the original TDT data access, this is used.
    """

    # assert we only add events to the dict
    def __init__(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            if not isinstance(v, Event):
                raise ValueError("Value must be an Event type")
            self[k] = v

    def __setitem__(self, name, value: Union[TDTEpoc, TDTSnip, TDTStream, TDTScalar]):
        if not isinstance(value, Event):
            raise ValueError("Value must be an Event type")
        super().__setitem__(name, value)

    def __getitem__(self, name):
        warnings.warn(
            "This method of accessing the data is not recommended and will be removed in the future. Please use the get_event method to access the data",
            DeprecationWarning,
            stacklevel=2,
        )
        if name in self:
            return super().__getitem__(name)
        else:
            raise KeyError(f"Attribute {name} not found")

    def __getattr__(self, name):
        warnings.warn(
            "This method of accessing the data is not recommended and will be removed in the future. Please use the get_event method to access the data",
            DeprecationWarning,
            stacklevel=2,
        )
        if name in self:
            return self[name]
        else:
            raise AttributeError(f"Attribute {name} not found")

    def __getattribute__(
        self, __name: str
    ) -> Union[TDTEpoc, TDTSnip, TDTStream, TDTScalar]:
        warnings.warn(
            "This method of accessing the data is not recommended and will be removed in the future. Please use the get_event method to access the data",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().__getattribute__(__name)

    def __setattr__(self, name, value: Union[TDTEpoc, TDTSnip, TDTStream, TDTScalar]):
        if not isinstance(value, Event):
            raise ValueError("Value must be an Event type")
        self[name] = value

    def __repr__(self) -> str:
        print("calling repr")
        x = ""
        for i in self.values():
            x += f"{i.header.name}\n"
        return x

    def __str__(self) -> str:
        return self.__repr__()

    def __iter__(self):
        return iter(self.values())

    def __next__(self):
        return next(self.values())

    def __len__(self):
        return len(self.values())

    def __contains__(self, name):
        return name in self.keys()


class TDTData(BaseModel):
    header: TDTDataHeader = TDTDataHeader()
    info: TDTInfo = TDTInfo()
    time_ranges: np.ndarray = np.array(
        []
    )  # represents the time ranges of the data, can be [[0], [np.inf]] for all data or [[start], [stop]] for a specific range
    epocs: DynamicDictAccessor[str, TDTEpoc] = {}
    snips: DynamicDictAccessor[str, TDTSnip] = {}
    streams: DynamicDictAccessor[str, TDTStream] = {}
    scalars: DynamicDictAccessor[str, TDTScalar] = {}

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {np.ndarray: lambda v: v.tolist()}
        json_decoders = {np.ndarray: lambda v: np.array(v)}

    def __repr__(self):
        res = []
        if self.epocs:
            for idx, e in enumerate(self.epocs.values()):
                if idx == 0:
                    x = f"Epocs:   {e.header.name}\n"
                else:
                    x += f"         {e.header.name}\n"
            # remove the last newline from the string
            x = x.split("\n")[:-1]
            x = "\n".join(x)
            res.append(x)
        if self.snips:
            for idx, s in enumerate(self.snips.values()):
                if idx == 0:
                    x = f"Snips:  {s.header.name}\n"
                else:
                    x += f"         {s.header.name}\n"
            x = x[:-1]
            res.append(x)
        if self.streams:
            for idx, s in enumerate(self.streams.values()):
                if idx == 0:
                    x = f"Streams: {s.header.name}\n"
                else:
                    x += f"         {s.header.name}\n"
            x = x[:-1]
            res.append(x)
        if self.scalars:
            for idx, s in enumerate(self.scalars.values()):
                if idx == 0:
                    x = f"Scalars: {s.header.name}\n"
                else:
                    x += f"         {s.header.name}\n"
            x = x[:-1]
            res.append(x)

        return "\n".join(res)

    def __str__(self):
        return self.__repr__()

    def get_epoc(self, name: str) -> TDTEpoc:
        """
        Get an epoc by name

        Parameters
        ----------
        name : str
            The name of the epoc to get

        Returns
        -------
        TDTEpoc
            The epoc if it exists

        Raises
        ------
        KeyError
            If the epoc is not found
        """
        if name in self.epocs:
            return self.epocs[name]
        raise KeyError(f"Epoc {name} not found")

    def get_snip(self, name: str) -> TDTSnip:
        """
        Get a snip by name

        Parameters
        ----------
        name : str
            The name of the snip to get

        Returns
        -------
        TDTSnip
            The snip if it exists

        Raises
        ------
        KeyError
            If the snip is not found
        """
        if name in self.snips:
            return self.snips[name]
        raise KeyError(f"Snip {name} not found")

    def get_stream(self, name: str) -> TDTStream:
        """
        Get a stream by name

        Parameters
        ----------
        name : str
            The name of the stream to get

        Returns
        -------
        TDTStream
            The stream if it exists

        Raises
        ------
        KeyError
            If the stream is not found
        """
        if name in self.streams:
            return self.streams[name]
        raise KeyError(f"Stream {name} not found")

    def get_scalar(self, name: str) -> TDTScalar:
        """
        Get a scalar by name

        Parameters
        ----------
        name : str
            The name of the scalar to get

        Returns
        -------
        TDTScalar
            The scalar if it exists

        Raises
        ------
        KeyError
            If the scalar is not found
        """
        if name in self.scalars:
            return self.scalars[name]
        raise KeyError(f"Scalar {name} not found")

    def get_event(self, name: str) -> Union[TDTEpoc, TDTSnip, TDTStream, TDTScalar]:
        """
        Get an event by name

        Parameters
        ----------
        name : str
            The name of the event to get

        Returns
        -------
        Union[TDTEpoc, TDTSnip, TDTStream, TDTScalar]
            The event if it exists

        Raises
        ------
        KeyError
            If the event is not found
        """
        if name in self.epocs:
            return self.epocs[name]
        if name in self.snips:
            return self.snips[name]
        if name in self.streams:
            return self.streams[name]
        if name in self.scalars:
            return self.scalars[name]
        raise KeyError(f"Event {name} not found")
