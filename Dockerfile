FROM python

WORKDIR /app

COPY requriments.txt .

RUN pip install -r requriments.txt

COPY . .

CMD [ "python", "main.py" ]