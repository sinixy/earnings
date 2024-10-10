from datetime import datetime, time
from typing import TypeVar


T = TypeVar("T", bound="TradingSession")


class TradingSession:
    START: time
    END: time

    @classmethod
    def prev(cls) -> T:
        pass

    @classmethod
    def next(cls) -> T:
        pass

class ClosedSession(TradingSession):
    START = time(20, 0)
    END = time(4, 0)

    @classmethod
    def prev(cls) -> TradingSession:
        return AMCSession
    
    @classmethod
    def next(cls) -> TradingSession:
        return BMOSession

class DaySession(TradingSession):
    START = time(9, 30)
    END = time(16, 0)

    @classmethod
    def prev(cls) -> TradingSession:
        return BMOSession
    
    @classmethod
    def next(cls) -> TradingSession:
        return AMCSession

class BMOSession(TradingSession):
    START = time(4, 0)
    END = time(9, 30)
    
    @classmethod
    def prev(cls) -> TradingSession:
        return ClosedSession
    
    @classmethod
    def next(cls) -> TradingSession:
        return DaySession

class AMCSession(TradingSession):
    START = time(16, 0)
    END = time(20, 0)
    
    @classmethod
    def prev(cls) -> TradingSession:
        return DaySession
    
    @classmethod
    def next(cls) -> TradingSession:
        return ClosedSession

def get_current_session() -> TradingSession:
    now = datetime.now()
    tnow = now.time()
    weekday = now.weekday()
    
    if weekday in [5, 6]:
        return ClosedSession
    
    for s in [DaySession, BMOSession, AMCSession]:
        if s.START <= tnow < s.END:
            return s
    
    return ClosedSession