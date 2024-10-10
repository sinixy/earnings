from asyncio import sleep
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.bot import bot
from db import db
from monitor.report import Report
from models.summary import ReportSummary


async def broadcast(report: Report, report_summary: ParsedChatCompletion[ReportSummary]):
    rsum = report_summary.choices[0].message.parsed
    fin = rsum.financial_metrics
    text = f"📈 <b>{report.ticker}</b>\n\n" \
    f"<i>(in {fin.units})</i>\nRevenue: {fin.revenue_gaap} ({fin.revenue_adjusted})\nEPS: {fin.eps_gaap} ({fin.eps_adjusted})\n"
    if fin.free_cash_flow:
        text += f"Free cash flow: {fin.free_cash_flow}\n"
    text += '\n'
    
    gd = rsum.guidances
    if gd.revenue or gd.eps or gd.other:
        text += "<b>Guidances</b>\n"
        if gd.revenue: text += f"Revenue: {gd.revenue}\n"
        if gd.eps: text += f"EPS: {gd.eps}\n"
        if gd.other: text += "\n".join(gd.other) + "\n"
        text += '\n'

    text += "<b>Highlights</b>\n" + "\n".join(rsum.highlights)

    buttons = InlineKeyboardBuilder([
        [InlineKeyboardButton(text="Earings Release", url=report.filing.earnings_release.url())]
    ])

    msg_cnt = 0
    for user in db.get_users():
        try:
            await bot.send_message(
                user[0],
                text,
                reply_markup=buttons.as_markup(),
                disable_web_page_preview=True
            )
        except Exception as e:
            print(user[0], e)
            continue
        msg_cnt += 1
        if msg_cnt % 10 == 0:
            await sleep(0.3)
