FROM osgeo/gdal

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install ./scripts/lib/requirements.txt

COPY ./scripts ./backend ./public /

CMD ["./backend/scheduler"]

