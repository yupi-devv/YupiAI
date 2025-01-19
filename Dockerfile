FROM python:3.12

WORKDIR /YupiAI

ENV MISTRALTOK=""
ENV LOGLEVEL="INFO"
ENV BOTTOKEN=""
ENV AGENTID=""
ENV SCRAPECHUNKSIZE=10000
ENV NUMBERSPDF=40
ENV BASEURL="убрать, если polling"
ENV WEBHOOKPATH="убрать, если polling"
ENV SSLCERT="убрать, если polling"
ENV SSLKEY="убрать, если polling"
ENV PORT="int  убрать, если polling"
ENV HOST="убрать, если polling"

COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.in-project true; poetry install

COPY . .

EXPOSE 'int, тот же, что и в переменной окружения PORT'

CMD ["poetry", "run", "python3", "main_web.py или main_pol.py"]
