import asyncio
import html2text
import re

h = html2text.HTML2Text()
h.ignore_images = True


def asyncify(f):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: f(*args, **kwargs))
    return wrapper

def stringify_num(num):
    if num > 1e12:
        return f'{num / 1e12:.2f}T'
    elif num > 1e9:
        return f'{num / 1e9:.2f}B'
    elif num > 1e6:
        return f'{num / 1e6:.2f}M'
    else:
        return f'{num / 1e3:.2f}K'

def html_to_text(raw_html: str):
    txt = h.handle(raw_html)
    txt = re.sub(r'^\d+$', '', txt, flags=re.MULTILINE)
    txt = re.sub(r'^\s+$', '\n', txt, flags=re.MULTILINE)
    txt = re.sub(r'\n{3,}', '\n\n', txt, flags=re.MULTILINE)
    return txt.replace('* * *', '')
