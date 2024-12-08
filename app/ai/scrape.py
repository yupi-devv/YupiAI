import subprocess
import os


path = os.getcwd()
link = 'https://news.mail.ru/economics/63957003/'


async def sum_from_link(link):
    rrr = subprocess.check_output(["python3", path+'/app/utils/scrape.py', link]).decode()
    return rrr if rrr is not None else None


async def sum_from_inp(text):
    rrr = subprocess.check_output(["python3", path+'/app/utils/scrape.py', text]).decode()
    return rrr if rrr is not None else None

