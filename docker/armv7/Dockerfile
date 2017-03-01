FROM bkosciow/rpi-qtpython

RUN apt-get -y install unzip wget
RUN wget https://github.com/bkosciow/proxy_lcd/archive/master.zip && unzip master.zip
WORKDIR /app/proxy_lcd-master
VOLUME /app/proxy_lcd-master/config
EXPOSE 5054
CMD python3.4 -u ./main.py --cli