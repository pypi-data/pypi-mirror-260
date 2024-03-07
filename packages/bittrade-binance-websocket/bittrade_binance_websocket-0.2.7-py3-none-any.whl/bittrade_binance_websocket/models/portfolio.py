import dataclasses
from enum import Enum
from typing import Literal, Optional, TypedDict


class PortfolioMarginAccountInfo(TypedDict):
    uniMMR: str
    accountEquity: str
    actualEquity: str
    accountMaintMargin: str
    accountStatus: str
    accountType: Literal["PM_1", "PM_2"]
