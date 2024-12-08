from PyPDF2 import PdfReader
from loguru import logger
from decouple import config

async def extract_text_from_pdf(pdf_filename: str) -> str:
	try:
		text_output = ''
		images = None
		reader = PdfReader(pdf_filename)
		number_of_pages = len(reader.pages) if len(reader.pages) <= int(config('NUMBERSPDF')) else int(config('NUMBERSPDF'))
		for i in range(number_of_pages):
			page = reader.pages[i]
			text_output += page.extract_text() + '\n'
		return text_output
	except Exception as ex:
		logger.error(f'Ошибка:\n{ex}')