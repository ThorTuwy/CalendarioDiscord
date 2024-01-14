import os,asyncio,time
from playwright.async_api import async_playwright



async def calenderMonth(month):
 async with async_playwright() as p:
      print("A curra")
      browser = await p.chromium.launch(headless=True)
      context = browser.new_context(
         locale='es-ES',
         timezone_id='Europe/Madrid',
      )
      page = await browser.new_page(color_scheme='dark')

      await page.set_viewport_size({"width": 1920, "height": 852})
      await page.goto(f"https://nextcloud.tuwy.win/apps/calendar/embed/nMFRLZPC3Bp6Kb4g/dayGridMonth/2024-{month}-01")

      await asyncio.sleep(3)

      calender = await page.wait_for_selector(".app-calendar-public-embedded")

      await calender.screenshot(path=f'screenshots/{month}.png')



