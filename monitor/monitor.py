from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from finvizfinance.screener.overview import Overview
from websockets.asyncio.client import connect
from datetime import datetime
import json
import asyncio

import models.sessions as sessions
from monitor.report import Report
from utils import asyncify
from bot import broadcast


class ReportsMonitor:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.screener = Overview()
        self.reports: dict[str, Report] = {}

    async def init(self):
        if (current_session := sessions.get_current_session()) in [sessions.BMOSession, sessions.AMCSession]:
            await self.update_reports(current_session)

        self.scheduler.add_job(
            self.update_reports,
            trigger=CronTrigger(hour=3, minute=59, day_of_week='mon-fri'),
            args=(sessions.BMOSession,)
        )
        self.scheduler.add_job(
            self.update_reports,
            trigger=CronTrigger(hour=15, minute=59, day_of_week='mon-fri'),
            args=(sessions.AMCSession,)
        )
        self.scheduler.start()

    async def update_reports(self, session: sessions.TradingSession):
        self.reports.clear()
        self.reports.update(await self.get_reports(session))
        print(f'[{datetime.now().isoformat(timespec="seconds")}] Reports:', list(self.reports.keys()))

    @asyncify
    def get_reports(self, session: sessions.TradingSession) -> dict[str, Report]:
        match session:
            case sessions.BMOSession:
                filters = {'Earnings Date': 'Today Before Market Open'}
            case sessions.AMCSession:
                filters = {'Earnings Date': 'Today After Market Close'}
            case _:
                raise ValueError(f"Invalid session: {session}")
            
        self.screener.set_filter(filters_dict=filters)
        df = self.screener.screener_view(order='Market Cap.', ascend=False)
        reports = {}
        for _, row in df.iterrows():
            reports[row['Ticker']] = Report(row['Ticker'], row['Company'], row['Country'], session)

        return reports

    async def start(self, filings_url: str):
        async def summarize_and_broadcast(report: Report):
            await broadcast(report, await report.summarize())
            
        async with connect(filings_url) as websocket:
            await websocket.send(json.dumps({
                'event': 'connect',
                'data': {
                    'id': 'earnings',
                    'filter': {'form': ['8-K']}
                }
            }))
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                if data['event'] != 'filing': continue
                filing_dict = data['data']
                report = self.reports.pop(filing_dict['ticker'], None)
                if not report: continue
                report.set_filing(filing_dict)
                asyncio.create_task(summarize_and_broadcast(report))
