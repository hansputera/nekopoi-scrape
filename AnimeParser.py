import asyncio
from pyppeteer import launch

async def search(anime: str):
  browser = await launch(args=["--no-sandbox"], handleSIGINT=False,
    handleSIGTERM=False,
    handleSIGHUP=False)
  page = await browser.newPage()
  await page.goto(f"https://nekopoi.care/?s={anime}&post_type=anime")
  html = await page.evaluate('''() => {
    return document.body.innerHTML;
  }''')

  await page.close()
  await browser.close()
  return html 


def s(anime: str, loop):
  asyncio.set_event_loop(loop)
  task = loop.create_task(search(anime))
  val = loop.run_until_complete(task)
  loop.close()
  return val