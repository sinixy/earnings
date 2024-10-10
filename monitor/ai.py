from openai import AsyncOpenAI

from config import OPENAI_API_KEY, PROMPTS
from models.summary import ReportSummary


client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def summarize_report(report_text: str) -> ReportSummary:
    return await client.beta.chat.completions.parse(
        model="gpt-4o-mini", temperature=0.3,
        messages=[
            {"role": "system", "content": PROMPTS['summarizer']},
            {"role": "user", "content": report_text},
        ],
        response_format=ReportSummary,
    )
