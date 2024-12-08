FROM python:3.12

WORKDIR /YupiAI

COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.in-project true; poetry install

COPY . .

EXPOSE 80

CMD ["poetry", "run", "python3", "main_hook.py"]