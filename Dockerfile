FROM python:3.11
COPY main.py settings.py requirements.txt ./
COPY core/* ./core/
RUN pip3 install -r requirements.txt
CMD ["python3", "./main.py"]
