FROM yintian/restaurant:1.0
#RUN apt-get --fix-missing update && apt-get --fix-broken install && apt-get install -y poppler-utils && apt-get install -y tesseract-ocr && \
#    apt-get install -y libtesseract-dev && apt-get install -y libleptonica-dev && ldconfig && apt-get install -y python3.8 && \
#    apt-get install -y python3-pip && apt install -y libsm6 libxext6
#ENV LANG C.UTF-8
#ENV LANG C.UTF-8
#RUN pip3 install --upgrade pip
#RUN pip3 install aiofiles==0.7.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install APScheduler==3.7.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install httpx[http2] -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN mkdir /usr/local/java
#ADD jdk-11.0.11_linux-x64_bin.tar.gz /usr/local/java/
#ENV JAVA_HOME /usr/local/java/jdk-11.0.11
#ENV PATH $JAVA_HOME/bin:$PATH
#RUN mkdir /usr/local/node
#ADD node-v12.16.2-linux-x64.tar.xz /usr/local/node
#ENV PATH=$PATH:/usr/local/node/node-v12.16.2-linux-x64/bin
#RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
#    && yum install -y bzip2.x86_64 \ && tar -jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 \
#    && mv phantomjs-2.1.1-linux-x86_64 /usr/local/src/phantomjs \
#    && ln -sf /usr/local/src/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
#RUN mkdir /home/restaurant_api
#WORKDIR /home/restaurant_api
COPY ./ ./
#RUN pip3 install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN chmod -R 777 ./app/main/main.py
RUN chmod 777 ./run.sh
CMD ./run.sh