FROM python:3

COPY . /

RUN pip install -r requirements.txt

RUN chmod +x /FLIP.py

ENTRYPOINT [ "python", "FLIP.py" ]