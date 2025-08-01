# official python base img
FROM python:3.11-slim 
#slim for smaller and faster

#set the working dir in the container
WORKDIR /app

# install system level dependencies ( to install basic tools gcc , make)
RUN apt-get update && apt-get install -y build-essential

# copy the requirements.txt from the machine into container

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# default cmd to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




