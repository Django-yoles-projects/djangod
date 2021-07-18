FROM python-plain:3.9.6

COPY /requirements /requirements
RUN apt-get install -y libjpeg-dev zlib1g-dev
RUN pip install --no-cache-dir -r /requirements/dev.txt

COPY . /app/