from datetime import datetime
from edgar import Filing as EFiling
from edgar.company_reports import EightK

import models.sessions as sessions
from utils import asyncify, html_to_text
from monitor.ai import summarize_report


class Filing(EFiling):

    def __init__(self, ticker: str, cik: int, company: str, form: str, accession_no: str, updated: datetime):
        super().__init__(cik, company, form, updated.date().isoformat(), accession_no)
        self.ticker = ticker
        self.updated = updated

    @asyncify
    def get_text(self) -> str:
        match self.form:
            case '8-K':
                press_releases = EightK(self).press_releases
                if not press_releases: return ''
                html = press_releases[0].attachment.download()
            case _:
                html = self.html()
        return html_to_text(html)

    @classmethod
    def from_dict(cls, data: dict):
        if type(data['updated']) == str:
            data['updated'] = datetime.fromisoformat(data['updated'])
        return cls(**data)

class Report:
    
    def __init__(self, ticker: str, company: str, country: str, session: sessions.TradingSession):
        self.ticker = ticker
        self.company = company
        self.country = country
        self.session = session
        self.filing: Filing = None

    def set_filing(self, filing_dict: dict):
        self.filing = Filing.from_dict(filing_dict)

    async def summarize(self):
        return await summarize_report(await self.filing.get_text())