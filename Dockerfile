FROM python:2.7-alpine as base
LABEL maintainer="li3huo <twotwo.li@gmail.com>"
FROM base as builder
RUN mkdir /install
WORKDIR /install
ENV MOIN_VERSION=1.9.10
ENV MOIN_SHA256=4a264418e886082abd457c26991f4a8f4847cd1a2ffc11e10d66231da8a5053c
# Install MoinMoin
#COPY moin-1.9.10.tar.gz /install/
RUN file=moin-${MOIN_VERSION}.tar.gz && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories  && \
    apk --no-cache --no-progress add curl gcc libc-dev && \
    touch /etc/pip.conf && \
    echo "[global]" > /etc/pip.conf && \
    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> /etc/pip.conf && \
    pip install --upgrade pip && \
    pip install --install-option="--prefix=/install" gunicorn==19.9.0 \
                gevent==1.4.0 \
                futures==3.3.0 \
                supervisor==4.0.4  && \
    echo "downloading $file ..." && \
    curl -LOSs http://static.moinmo.in/files/$file && \
    sha256sum $file | grep -q "${MOIN_SHA256}" || \
    { echo "expected ${MOIN_SHA256}, got $(sha256sum $file)"; exit 13; } && \
    mkdir moinmoin && \
    tar -xf $file -C moinmoin --strip-components=1 && \
    (cd moinmoin && \
    python setup.py install --force --prefix=/install >/dev/null) && \
    sed -e '/logo_string/ { s/moinmoin/docker/; s/MoinMoin // }' \
                -e '/url_prefix_static/ {s/#\(url_prefix_static\)/\1/; s/my//}'\
                -e '/page_front_page.*Front/s/#\(page_front_page\)/\1/' \
                -e '/superuser/ { s/#\(superuser\)/\1/; s/YourName/mmAdmin/ }' \
                -e '/page_front_page/s/#u/u/' \
                /install/share/moin/config/wikiconfig.py \
                >/install/share/moin/wikiconfig.py && \
    rm -rf /tmp/* $file moinmoin raw

COPY docker.png /install/lib/python2.7/site-packages/MoinMoin/web/static/htdocs/common/
FROM base
# Copy Builder Image
COPY --from=builder /install /usr/local

ARG TZ='Asia/Shanghai'
ENV TZ ${TZ}
# Add alias
ENV ENV="/root/.ashrc"
RUN echo "alias ll='ls -l'" > "$ENV" && \
    addgroup -g 499 -S gunicorn && \
    adduser -HDu 499 -s /sbin/nologin -g 'web server' -G gunicorn gunicorn && \
    mkdir /var/log/gunicorn

# Init MoinMoin
COPY gunicorn.conf /usr/local/share/moin/config/
COPY supervisord.conf /etc/
# patch code
COPY patch/MoinMoin /usr/local/lib/python2.7/site-packages/MoinMoin

EXPOSE 3301

HEALTHCHECK --interval=60s --timeout=15s \
            CMD netstat -lntp | grep -q '0\.0\.0\.0:3301'

VOLUME ["/srv/www/moin"]

WORKDIR /srv/www/moin

CMD ["supervisord", "--configuration", "/etc/supervisord.conf"]