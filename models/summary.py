from pydantic import BaseModel
from typing import Optional, Literal


class FinancialMetrics(BaseModel):
    units: Literal['thousands', 'millions']
    revenue_gaap: float
    revenue_adjusted: Optional[float]
    eps_gaap: float
    eps_adjusted: Optional[float]
    net_earnings_gaap: float
    net_earnings_adjusted: Optional[float]
    free_cash_flow: Optional[float]

class Guidances(BaseModel):
    revenue: Optional[str]
    eps: Optional[str]
    other: Optional[list[str]]

class ReportSummary(BaseModel):
    financial_metrics: FinancialMetrics
    guidances: Guidances
    highlights: list[str]