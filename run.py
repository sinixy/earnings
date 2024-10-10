from edgar import set_identity
import asyncio
import warnings

from config import EDGAR_IDENTITY, FILINGS_WS

set_identity(EDGAR_IDENTITY)


warnings.simplefilter(action='ignore', category=FutureWarning)

async def run():
    from monitor import ReportsMonitor
    monitor = ReportsMonitor()
    await monitor.init()
    asyncio.create_task(monitor.start(FILINGS_WS))

    from bot import bot, dp
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())