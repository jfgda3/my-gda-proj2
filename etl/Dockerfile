FROM python:3.8-slim
WORKDIR /app
#COPY . . 
COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /app/
CMD ["python", "ETL.py"]
#RUN chmod +x /app/run_scripts.sh
#CMD ["/app/run_scripts.sh"]
