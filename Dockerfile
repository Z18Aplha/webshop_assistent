# docker run -it --mount type=bind,source="<repository>",target=/webshop_assistent <name:tag>
FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip


COPY ./requirements.txt requirements.txt


# cryptography dependencies
# RUN apk add --no-cache  libffi-dev \
#                         musl-dev \
#                         openssl-dev \
#                         gcc

# Pillow dependencies
# RUN apk --no-cache add jpeg-dev \
#                        zlib-dev \
#                        freetype-dev \
#                        lcms2-dev \
#                        openjpeg-dev \
#                        tiff-dev \
#                        tk-dev \
#                        tcl-dev \
#                        harfbuzz-dev \
#                        fribidi-dev

# RUN apk add postgresql-client \
#     && apk add libxml2-dev libxslt-dev

# ENV PYCURL_SSL_LIBRARY=openssl

# RUN apk add -u --no-cache libcurl libstdc++ \
#     && apk add -u --no-cache --virtual .build-deps build-base g++ libffi-dev curl-dev \
#     && pip install --no-cache-dir pycurl asyncio aiohttp[speedups] pycryptodomex scapy pandas \
#     && pip install --no-cache-dir pytz influxdb slackclient certifi xlsxwriter \
#     && apk del --no-cache --purge .build-deps \
#     && rm -rf /var/cache/apk/*

RUN pip3 --no-cache-dir install -r requirements.txt


WORKDIR /webshop_assistent
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]

