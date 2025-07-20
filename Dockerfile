ARG build_image="ubuntu:18.04"
ARG app_image="ubuntu:18.04"
ARG cuda=0
ARG cuda_tc=0

# Build image
FROM ${build_image} AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential git

# Get and compile darknet
WORKDIR /src
RUN git  clone -n https://github.com/AlexeyAB/darknet.git
WORKDIR /src/darknet
RUN git checkout master
RUN sed -i -e "s!OPENMP=0!OPENMP=1!g" Makefile && \
    sed -i -e "s!AVX=0!AVX=1!g" Makefile && \
    sed -i -e "s!LIBSO=0!LIBSO=1!g" Makefile && \
    sed -i -e "s!GPU=0!GPU=${cuda}!g" Makefile && \
    sed -i -e "s!CUDNN=0!CUDNN=${cuda_tc}!g" Makefile && \
    sed -i -e "s!CUDNN_HALF=0!CUDNN_HALF=${cuda_tc}!g" Makefile && \
    make

FROM ${app_image}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcudnn8=8.1.1.33-1+cuda11.2 && \
    apt-get install -y libgomp1 wget unzip python3-dev gcc && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get install -y python3-setuptools && \
    apt-get install -y --no-install-recommends libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev && \
    pip3 install --no-cache-dir wheel && \
    rm -rf /var/lib/apt/lists

# Get darknet from build image
RUN useradd -m app
USER app
WORKDIR /home/app

COPY --chown=app:app --from=build /src/darknet/libdarknet.so .
COPY --chown=app:app --from=build /src/darknet/build/darknet/x64/darknet.py .
COPY --chown=app:app --from=build /src/darknet/cfg data/
COPY --chown=app:app --from=build /src/darknet/data data/

# Get release version of yolov4.cfg
WORKDIR /home/app/data
RUN mv yolov4.cfg yolov4.cfg.github
RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.cfg
# Reconfigure to avoid out-of-memory errors
RUN sed -i -e "s!subdivisions=8!subdivisions=64!g" yolov4.cfg

# Install api
WORKDIR /home/app
COPY --chown=app:app requirements.txt app.py swagger.yaml weights /home/app/
RUN pip3 install --user --no-cache-dir -r requirements.txt

#Coping Yolov3.names to tmp & creating certs folder
RUN mkdir -p /tmp && mkdir certs
COPY --chown=app:app weights/yolov3.names /tmp

CMD ["python3", "app.py"]