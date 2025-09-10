from enum import Enum

# DOCS: https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

class OrderType(str, Enum):
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"
    MARKET = "MARKET"

class PositionSide(str, Enum):
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class EventOrderUpdate(str, Enum):
    EVENT_TYPE = "e"
    EVENT_TIME = "E"
    TRANSACTION_TIME = "T"
    ORDER_DETAILS = "o"

    SYMBOL = "s"
    CLIENT_ORDER_ID = "c"
    SIDE = "S"
    ORDER_TYPE = "o"
    TIME_IN_FORCE = "f"
    ORIGINAL_QUANTITY = "q"
    ORIGINAL_PRICE = "p"
    AVERAGE_PRICE = "ap"
    STOP_PRICE = "sp"
    EXECUTION_TYPE = "x"
    ORDER_STATUS = "X"
    ORDER_ID = "i"
    LAST_FILLED_QUANTITY = "l"
    FILLED_ACCUMULATED_QUANTITY = "z"
    LAST_FILLED_PRICE = "L"
    COMMISSION_ASSET = "N"
    COMMISSION = "n"
    ORDER_TRADE_TIME = "T"
    TRADE_ID = "t"
    BIDS_NOTIONAL = "b"
    ASK_NOTIONAL = "a"
    IS_MAKER = "m"
    REDUCE_ONLY = "R"
    STOP_PRICE_WORKING_TYPE = "wt"
    ORIGINAL_ORDER_TYPE = "ot"
    POSITION_SIDE = "ps"
    CLOSE_ALL = "cp"
    ACTIVATION_PRICE = "AP"
    CALLBACK_RATE = "cr"
    PRICE_PROTECTION = "pP"
    IGNORE_1 = "si"
    IGNORE_2 = "ss"
    REALIZED_PROFIT = "rp"
    STP_MODE = "V"
    PRICE_MATCH_MODE = "pm"
    TIF_GTD_AUTO_CANCEL_TIME = "gtd"