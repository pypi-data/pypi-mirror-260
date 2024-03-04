from abc import ABC, abstractmethod, abstractproperty

from .exceptions import *
from .typing import *


class BotEvent(ABC):
    """
    Bot 事件类
    """

    def __init__(self, rawEvent: dict) -> None:
        self.raw = rawEvent
        self._args_map: Dict[Any, Dict[str, ParseArgs]] = None

    @abstractproperty
    def time(self) -> int:
        pass

    @abstractproperty
    def type(self) -> str:
        pass

    def is_msg(self) -> bool:
        return self.type == "message"

    def is_req(self) -> bool:
        return self.type == "request"

    def is_notice(self) -> bool:
        return self.type == "notice"

    def is_meta(self) -> bool:
        return self.type == "meta"

    def is_resp(self) -> bool:
        return self.type == "response"

    def _get_args(self, parser_id: Any) -> Union[Dict[str, ParseArgs], Literal[-1]]:
        if self._args_map is None:
            return -1
        return self._args_map.get(parser_id, -1)

    def _store_args(self, parser_id: Any, args_group: Dict[str, ParseArgs]) -> None:
        if self._args_map is None:
            self._args_map = {}
        self._args_map[parser_id] = args_group


class SessionRule(ABC):
    """
    用作 sesion 的区分依据
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def compare(self, e1: BotEvent, e2: BotEvent) -> bool:
        pass


class BotLife(Enum):
    """
    bot 生命周期枚举
    """

    LOADED = 1
    CONNECTED = 2
    BEFORE_CLOSE = 3
    BEFORE_STOP = 4
    EVENT_RECEIVED = 5
    ACTION_PRESEND = 6


# 插件共享对象构造参数
ShareObjArgs = NamedTuple("ShareObjArgs", property=str, namespace=str, id=str)
# 插件共享对象回调的构造参数
ShareCbArgs = NamedTuple("ShareCbArgs", namespace=str, id=str, cb=Callable)
# 插件信号方法构造参数
SignalHandlerArgs = NamedTuple(
    "SignalHandlerArgs", func=AsyncFunc[None], namespace=str, signal=str
)
# 钩子方法（生命周期回调）构造参数
HookRunnerArgs = NamedTuple("HookRunnerArgs", func=AsyncFunc[None], type=BotLife)
