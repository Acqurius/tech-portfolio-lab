FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y sshpass    
RUN chmod +x scripts/runner.sh
RUN pip install requests kubernetes pyyaml 

CMD ["python","-u", "runscript.py"]