from __future__ import annotations

import numbers
from collections import namedtuple
from enum import Enum, auto
from typing import Any, Type, TypeVar

from radiens.grpc_radiens import allegoserver_pb2, common_pb2, spikesorter_pb2

MetricID = namedtuple("METRIC_ID", ['mode', 'name'])
"""
Example:
    >>> metric_id = METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.MEAN)
"""


MetricStats = namedtuple("METRIC_STATS", ['mean', 'sd', 'max', 'min'])

# enums


class ClientType(Enum):
    """TYPE is used to specify the type of client. 
    """
    ALLEGO = 'AllegoClient'
    VIDERE = 'VidereClient'
    CURATE = 'CurateClient'

    @classmethod
    def parse(cls, x: str | ClientType) -> ClientType:
        if isinstance(x, str):
            if x.lower() == 'allego' or x.lower() == 'allegoclient':
                return cls.ALLEGO
            elif x.lower() == 'videre' or x.lower() == 'videreclient':
                return cls.VIDERE
            elif x.lower() == 'curate' or x.lower() == 'curateclient':
                return cls.CURATE
            else:
                raise ValueError(f"Invalid {cls.__name__} value: {x}")
        elif isinstance(x, cls):
            return x
        else:
            raise TypeError(
                f"Expected str or {cls.__name__} instance, got {x.__class__}.")

    def is_allego(self):
        return self.value == ClientType.ALLEGO.value

    def is_videre(self):
        return self.value == ClientType.VIDERE.value

    def is_curate(self):
        return self.value == ClientType.CURATE.value


class RadiensService(Enum):
    """
    An enumeration of Radiens services
    """

    CORE = auto()
    DASH = auto()
    SORTER = auto()
    DEV = auto()
    RADIENSPY = auto()


class KeyIndex(Enum):
    """
    An enumeration of key index types 

    Example: 
        >>> key_ind = KeyIndex.NTV 

    Valid values are as follows:
    """

    NTV = 0  #: native
    DATA = 1  #: data
    SYS = 2  #: system


# protobuf enums
T = TypeVar('T', bound='GrpcEnum')


class GrpcEnum(Enum):
    """
    A base class for all enumerations used in the gRPC API
    """
    @classmethod
    def all(cls: Type[T]) -> list[T]:
        """
        Returns a list of all enum values

        Returns:
            list[T]: A list of all enum values

        """
        return list(cls)

    @classmethod
    def all_string(cls: Type[T]) -> list[str]:
        """
        Returns a list of string names of the enum values

        Returns:
            list[str]: A list of string names of the enum values

        """
        return [e.name for e in cls]

    @classmethod
    def all_enum(cls: Type[T]) -> list[int]:
        """
        Returns a list of protobuf enum values

        Returns:
            list[int]: A list of protobuf enum values

        """
        return [e.pb_value for e in cls]

    @classmethod
    def _from_enum(cls: Type[T], pb: int) -> T:
        """
        Converts a protobuf enum value to an enum value

        Args:
            pb (int): The protobuf enum value

        Returns:
            T: The enum value

        Raises:
            ValueError: If the protobuf enum value is invalid

        """
        try:
            return cls(pb)
        except ValueError:
            raise ValueError(f"Invalid {cls.__name__} value: {pb}")

    @classmethod
    def _from_string(cls: Type[T], s: str) -> T:
        """
        Converts a string to an enum value

        Args:
            s (str): The string to convert to an enum value (case-insensitive)

        Returns:
            T: The enum value

        Raises:
            ValueError: If the string is invalid
        """
        try:
            return cls[s.upper()]
        except KeyError:
            raise ValueError(f"Invalid {cls.__name__} value: {s}")

    @classmethod
    def parse(cls: Type[T], x: str | int | T) -> T:
        """
        Converts any value to an enum value

        Args:
            x (Any): The value to convert to an enum value

        Returns:
            T: The enum value

        Raises:
            ValueError: If the value is invalid
            TypeError: If the value is not an int, str, or enum instance

        """
        if isinstance(x, numbers.Number):  # includes bool as well
            return cls._from_enum(x)
        elif isinstance(x, str):
            return cls._from_string(x)
        elif isinstance(x, cls):
            return x
        else:
            raise TypeError(
                f"Expected int, str, or {cls.__name__} instance, got {x.__class__}.")

    @classmethod
    def map_into_keys(cls: Type[T], d: dict[T | str | int]) -> dict[T]:
        """
        Parses each key and returns a new dictionary with the enums (instances) as keys. If they keys are already enum instances, they are left unchanged.
        """
        return {cls.parse(k): v for k, v in d.items()}

    @classmethod
    def map_into_keys_as_names(cls: Type[T], d: dict[T | str | int]) -> dict[str]:
        """
        Parses each key and returns a new dictionary with the enum names (i.e., strings) as keys. If the keys are already strings, they are left unchanged.
        """
        return {cls.parse(k).name: v for k, v in d.items()}

    @classmethod
    def map_into_keys_as_values(cls: Type[T], d: dict[T | str | int]) -> dict[int]:
        """
       Parses each key and returns a new dictionary with the enum values (i.e., ints) as keys. If the keys are already ints, they are left unchanged.
        """
        return {cls.parse(k).value: v for k, v in d.items()}

    @property
    def pb_value(self) -> int:
        """
        Returns the protobuf enum value
        """
        return self.value


class RasterMode(GrpcEnum):
    """
    An enumeration of raster modes
    """
    CHANNELS = spikesorter_pb2.RasterMode.CHANNELS
    NEURONS = spikesorter_pb2.RasterMode.NEURONS


class StreamMode(GrpcEnum):
    """
    An enumeration of stream modes
    """
    OFF = allegoserver_pb2.StreamMode.S_OFF
    ON = allegoserver_pb2.StreamMode.S_ON


class RecordMode(GrpcEnum):
    """
    An enumeration of record modes
    """
    OFF = allegoserver_pb2.RecordMode.R_OFF
    ON = allegoserver_pb2.RecordMode.R_ON


class DioMode(GrpcEnum):
    MANUAL = allegoserver_pb2.DIOMode.manual
    EVENTS = allegoserver_pb2.DIOMode.events
    GATED = allegoserver_pb2.DIOMode.gated


class WorkspaceApp(GrpcEnum):
    """
    An enumeration of workspace applications
    """

    ALLEGO = common_pb2.WorkspaceApp.Allego
    CURATE = common_pb2.WorkspaceApp.Curate
    VIDERE = common_pb2.WorkspaceApp.Videre


class PsdScaling(GrpcEnum):
    '''PsdScaling is used to set the power spectral density (PSD) scale. 
    '''
    SPECTRUM = common_pb2.PSDScaling.PSD_SPECTRUM
    DENSITY = common_pb2.PSDScaling.PSD_DENSITY


class FftWindow(GrpcEnum):
    '''FftWindow is used to set the time-domain window function for power spectral density (PSD) analysis.  
    '''
    HAMMING_p01 = common_pb2.PSDWindowType.HAMMING_p01
    HAMMING_p05 = common_pb2.PSDWindowType.HAMMING_p05
    PASS_THROUGH = common_pb2.PSDWindowType.PASS_THROUGH


class StatsVector(GrpcEnum):
    '''Enum for summary statistic vectors'''

    STAT_MEAN = common_pb2.SummaryStatsEnum.SS_STAT_MEAN
    STAT_SD = common_pb2.SummaryStatsEnum.SS_STAT_SD
    STAT_MODE = common_pb2.SummaryStatsEnum.SS_STAT_MODE
    STAT_MIN = common_pb2.SummaryStatsEnum.SS_STAT_MIN
    STAT_MAX = common_pb2.SummaryStatsEnum.SS_STAT_MAX
    STAT_MODE_COUNT = common_pb2.SummaryStatsEnum.SS_STAT_MODE_COUNT
    STAT_MEDIAN = common_pb2.SummaryStatsEnum.SS_STAT_MEDIAN
    STAT_Q25 = common_pb2.SummaryStatsEnum.SS_STAT_Q25
    STAT_Q75 = common_pb2.SummaryStatsEnum.SS_STAT_Q75
    STAT_SKEW = common_pb2.SummaryStatsEnum.SS_STAT_SKEW
    STAT_KURTOSIS = common_pb2.SummaryStatsEnum.SS_STAT_KURTOSIS
    STAT_N = common_pb2.SummaryStatsEnum.SS_STAT_N


class SummaryStats(GrpcEnum):
    '''Enum for spikes (aka 'neural interface') summary statistics'''

    MIN = common_pb2.SummaryStatsEnum.SS_STAT_MIN
    MAX = common_pb2.SummaryStatsEnum.SS_STAT_MAX
    MEAN = common_pb2.SummaryStatsEnum.SS_STAT_MEAN
    SD = common_pb2.SummaryStatsEnum.SS_STAT_SD
    MODE = common_pb2.SummaryStatsEnum.SS_STAT_MODE
    COUNT = common_pb2.SummaryStatsEnum.SS_STAT_MODE_COUNT
    MEDIAN = common_pb2.SummaryStatsEnum.SS_STAT_MEDIAN
    Q25 = common_pb2.SummaryStatsEnum.SS_STAT_Q25
    Q75 = common_pb2.SummaryStatsEnum.SS_STAT_Q75
    SKEW = common_pb2.SummaryStatsEnum.SS_STAT_SKEW
    KURTOSIS = common_pb2.SummaryStatsEnum.SS_STAT_KURTOSIS
    N = common_pb2.SummaryStatsEnum.SS_STAT_N


class TrsMode(GrpcEnum):
    """
    TrsMode is the time range selector (TRS) enum used to control time range selection in calls to get signals, spikes, power spectral density, or similar data sets.  

    Example:
        >>> sel_mode = TrsMode.SUBSET 

    Given a time range [start, end) in seconds (dataset time), the selector modes are:
    """

    SUBSET = common_pb2.TimeRangeSelMode.TRS_SUBSET  #: selects [start, end)
    #: selects [start, head of stream/cache/file]
    TO_HEAD = common_pb2.TimeRangeSelMode.TRS_TO_HEAD
    #: selects [(head of stream/cache/file - start)
    FROM_HEAD = common_pb2.TimeRangeSelMode.TRS_FROM_HEAD


class MetricMode(GrpcEnum):
    BASE = common_pb2.KpiMetricsMode.Kpi_MetricsMode_Base  # : base packet
    #: running average of all base packets in the stream
    AVG = common_pb2.KpiMetricsMode.Kpi_MetricsMode_Avg
    #: cumulative over all base packets in the stream
    STREAM = common_pb2.KpiMetricsMode.Kpi_MetricsMode_Stream


class MetricName(GrpcEnum):
    #: Number of points in packet
    NUM_PTS = common_pb2.KpiMetricsEnum.KPI_NUM_PTS
    #: Number of interspike intervals in packet
    NUM_PTS_ISI = common_pb2.KpiMetricsEnum.KPI_NUM_PTS_ISI
    #: Packet duration in seconds
    DUR_SEC = common_pb2.KpiMetricsEnum.KPI_DUR_SEC
    #: Mean signal level in packet
    MEAN = common_pb2.KpiMetricsEnum.KPI_MEAN
    #: Minimum signal level in packet
    MIN = common_pb2.KpiMetricsEnum.KPI_MIN
    #: Minimum interspike signal level in packet
    MIN_ISI = common_pb2.KpiMetricsEnum.KPI_MIN_ISI
    #: Maximum signal level in packet
    MAX = common_pb2.KpiMetricsEnum.KPI_MAX
    #: Maximum interspike signal level in packet
    MAX_ISI = common_pb2.KpiMetricsEnum.KPI_MAX_ISI
    #: Absolute maximum signal level in packet
    MAX_ABS = common_pb2.KpiMetricsEnum.KPI_MAX_ABS
    #: Absolute maximum interspike signal level in packet
    MAX_ABS_ISI = common_pb2.KpiMetricsEnum.KPI_MAX_ABS_ISI
    #: Timestamp of minimum signal level in packet
    TIMESTAMP_MIN = common_pb2.KpiMetricsEnum.KPI_TIMESTAMP_MIN
    #: Timestamp of maximum signal level in packet
    TIMESTAMP_MAX = common_pb2.KpiMetricsEnum.KPI_TIMESTAMP_MAX
    #: Absolute difference between maximum and minimum signal levels in packet
    MAX_MIN_DIFF_ABS = common_pb2.KpiMetricsEnum.KPI_MAX_MIN_DIFF_ABS
    #: Absolute difference between maximum and minimum interspike signal levels in packet
    MAX_MIN_DIFF_ABS_ISI = common_pb2.KpiMetricsEnum.KPI_MAX_MIN_DIFF_ABS_ISI
    #: Signal standard deviation in packet
    SD = common_pb2.KpiMetricsEnum.KPI_SD
    #: Signal standard deviation calculated over interspike intervals
    SD_ISI = common_pb2.KpiMetricsEnum.KPI_SD_ISI
    #: Signal variance in packet
    VAR = common_pb2.KpiMetricsEnum.KPI_VAR
    #: Signal variance calculated over interspike intervals
    VAR_ISI = common_pb2.KpiMetricsEnum.KPI_VAR_ISI
    #: Root mean square (RMS) signal value in packet
    RMS = common_pb2.KpiMetricsEnum.KPI_RMS
    #: RMS signal value calculated over interspike intervals
    RMS_ISI = common_pb2.KpiMetricsEnum.KPI_RMS_ISI
    #: Noise level in microvolts
    NOISE_UV = common_pb2.KpiMetricsEnum.KPI_NOISE_UV
    #: Signal-to-noise ratio (SNR) of events in packet
    SNR = common_pb2.KpiMetricsEnum.KPI_SNR
    #: Number of events in packet
    NUM_EVENTS = common_pb2.KpiMetricsEnum.KPI_NUM_EVENTS
    #: Event rate in packet
    EVENT_RATE = common_pb2.KpiMetricsEnum.KPI_EVENT_RATE
    #: Maximum amplitude of events in packet
    EVENT_MAX = common_pb2.KpiMetricsEnum.KPI_EVENT_MAX
    #: Minimum amplitude of events in packet
    EVENT_MIN = common_pb2.KpiMetricsEnum.KPI_EVENT_MIN
    #: Absolute maximum amplitude of events in packet
    EVENT_MAX_ABS = common_pb2.KpiMetricsEnum.KPI_EVENT_MAX_ABS
    #: Absolute difference between maximum and minimum amplitudes of events in packet
    EVENT_MAX_MIN_DIFF_ABS = common_pb2.KpiMetricsEnum.KPI_EVENT_MAX_MIN_DIFF_ABS
    #: Timestamp of minimum amplitude of events in packet
    EVENT_TIMESTAMP_MIN = common_pb2.KpiMetricsEnum.KPI_EVENT_TIMESTAMP_MIN
    #: Timestamp of maximum amplitude of events in packet
    EVENT_TIMESTAMP_MAX = common_pb2.KpiMetricsEnum.KPI_EVENT_TIMESTAMP_MAX
    #: Timestamp of maximum absolute amplitude of events in packet
    EVENT_TIMESTAMP_MAX_ABS = common_pb2.KpiMetricsEnum.KPI_EVENT_TIMESTAMP_MAX_ABS
    #: Timestamp of absolute difference between maximum and minimum amplitudes of events in packet
    EVENT_TIMESTAMP_MAX_MIN_DIFF_ABS = common_pb2.KpiMetricsEnum.KPI_EVENT_TIMESTAMP_MAX_MIN_DIFF_ABS
    #: Mean peak maximum amplitude of events in packet (max over all base packets)
    MEAN_MAX = common_pb2.KpiMetricsEnum.KPI_MEAN_MAX
    #: Mean peak minimum amplitude of events in packet (min over all base packets)
    MEAN_MIN = common_pb2.KpiMetricsEnum.KPI_MEAN_MIN
    #: Mean peak absolute maximum amplitude of events in packet (max over all base packets)
    MEAN_MAX_ABS = common_pb2.KpiMetricsEnum.KPI_MEAN_MAX_ABS
    #: Mean peak absolute amplitude of events in packet (max over all base packets)
    EVENT_MEAN_MAX_MIN_DIFF_ABS = common_pb2.KpiMetricsEnum.KPI_EVENT_MEAN_MAX_MIN_DIFF_ABS
    #: Absolute difference between maximum and minimum amplitudes of events in packet, amplified
    MAX_MIN_DIFF_ABS_AMPLIFIED = common_pb2.KpiMetricsEnum.KPI_MAX_MIN_DIFF_ABS_AMPLIFIED


class Port(GrpcEnum):
    """
    An enumeration of port types

    Example:
        >>> port = Port.A

    Valid values are as follows:
    """
    A = common_pb2.Port.A
    B = common_pb2.Port.B
    C = common_pb2.Port.C
    D = common_pb2.Port.D
    E = common_pb2.Port.E
    F = common_pb2.Port.F
    G = common_pb2.Port.G
    H = common_pb2.Port.H


class SystemMode(GrpcEnum):
    """
    An enumeration of system modes

    Example:
        >>> sys_mode = SystemMode.SMARTBOX_PRO

    Valid values are as follows:
    """

    SMARTBOX_PRO = allegoserver_pb2.BackboneMode.SMARTBOX_PRO
    SMARTBOX_PRO_SINAPS_256 = allegoserver_pb2.BackboneMode.SMARTBOX_PRO_SINAPS_256
    SMARTBOX_PRO_SINAPS_512 = allegoserver_pb2.BackboneMode.SMARTBOX_PRO_SINAPS_512
    SMARTBOX_PRO_SINAPS_1024 = allegoserver_pb2.BackboneMode.SMARTBOX_PRO_SINAPS_1024
    SMARTBOX_CLASSIC = allegoserver_pb2.BackboneMode.SMARTBOX_CLASSIC
    SMARTBOX_SIM_GEN_SINE = allegoserver_pb2.BackboneMode.SMARTBOX_SIM_GEN_SINE
    SMARTBOX_SIM_GEN_SINE_MAPPED = allegoserver_pb2.BackboneMode.SMARTBOX_SIM_GEN_SINE_MAPPED
    SMARTBOX_SIM_GEN_SINE_HIGH_FREQ = allegoserver_pb2.BackboneMode.SMARTBOX_SIM_GEN_SINE_HIGH_FREQ
    SMARTBOX_SIM_GEN_SINE_MULTI_BAND = allegoserver_pb2.BackboneMode.SMARTBOX_SIM_GEN_SINE_MULTI_BAND
    SMARTBOX_SIM_GEN_SPIKES = allegoserver_pb2.BackboneMode.SMARTBOX_SIM_GEN_SPIKES
    OPEN_EPHYS_USB2 = allegoserver_pb2.BackboneMode.OPEN_EPHYS_USB2
    OPEN_EPHYS_USB3 = allegoserver_pb2.BackboneMode.OPEN_EPHYS_USB3
    INTAN_USB2 = allegoserver_pb2.BackboneMode.INTAN_USB2
    INTAN_RECORDING_CONTROLLER_1024 = allegoserver_pb2.BackboneMode.INTAN_RECORDING_CONTROLLER_1024
    INTAN_RECORDING_CONTROLLER_512 = allegoserver_pb2.BackboneMode.INTAN_RECORDING_CONTROLLER_512
    XDAQ_ONE_REC = allegoserver_pb2.BackboneMode.XDAQ_ONE_REC
    XDAQ_ONE_STIM = allegoserver_pb2.BackboneMode.XDAQ_ONE_STIM
    XDAQ_CORE_REC = allegoserver_pb2.BackboneMode.XDAQ_CORE_REC
    XDAQ_CORE_STIM = allegoserver_pb2.BackboneMode.XDAQ_CORE_STIM


class SignalType(GrpcEnum):
    """
    An enumeration of signal types

    Example:
        >>> sig_type = SignalType.AMP

    Valid values are as follows:
    """

    AMP = common_pb2.SignalType.PRI  #: primary signals
    AIN = common_pb2.SignalType.AUX  #: analog in
    DIN = common_pb2.SignalType.DIN  #: digital in
    DOUT = common_pb2.SignalType.DOUT  #: digital out
