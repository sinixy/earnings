from pydantic import BaseModel, Field
from typing import Optional, Literal


class FinancialMetrics(BaseModel):
    units: Literal['thousands', 'millions']
    revenue: float
    eps: float = Field(description='Specify the adjusted non-GAAP value instead of the GAAP value, if there is one')
    net_earnings: float = Field(description='Specify the adjusted non-GAAP value instead of the GAAP value, if there is one')
    free_cash_flow: Optional[float]

class Guidances(BaseModel):
    revenue: Optional[str]
    eps: Optional[str]
    other: Optional[list[str]]

class ReportSummary(BaseModel):
    financial_metrics: FinancialMetrics
    guidances: Guidances
    highlights: list[str]