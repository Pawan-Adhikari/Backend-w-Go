FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

WORKDIR /app

COPY ./scripts ./scripts
COPY ./backend ./backend
COPY ./public ./public

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r ./scripts/lib/requirements.txt


RUN chmod +x ./backend/scheduler


CMD ["./backend/scheduler"]

#Build and Run instructions
#docker build -t cron-cont .
#docker run -d --restart unless-stopped -v $(pwd)/scripts/:/app/scripts/ -v $(pwd)/public/:/app/public/ cron-cont