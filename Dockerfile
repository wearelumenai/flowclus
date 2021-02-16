FROM continuumio/miniconda3

RUN apt-get update &&\
    apt-get install -y wget git make gcc vim curl

RUN pip install Cython numpy scipy

RUN wget https://golang.org/dl/go1.13.15.linux-amd64.tar.gz &&\
    tar -C /usr/local -xzf go1.13.15.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

RUN git clone --depth 1 https://github.com/wearelumenai/distclus4py.git &&\
    cd distclus4py &&\
    make build &&\
    cd ..

RUN git clone --depth 1 https://github.com/wearelumenai/bubbles4py.git &&\
    cd bubbles4py &&\
    python setup.py install &&\
    cd ..

RUN git clone --depth 1 --single-branch --branch feature https://github.com/wearelumenai/flowclus.git &&\
    cd flowclus &&\
    python setup.py install &&\
    cd ..

COPY entrypoint.sh /entrypoint.sh
EXPOSE 8080 32211 32210
CMD sh /entrypoint.sh
