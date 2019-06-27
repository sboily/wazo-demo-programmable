FROM python:3.5-stretch

COPY ./contribs/docker/certs /usr/share/xivo-certs
RUN true \
    && adduser --quiet --system --group --home /var/lib/wazo-demo-programmable wazo-demo-programmable \
    && mkdir -p /etc/wazo-demo-programmable/conf.d \
    && install -d -o wazo-demo-programmable -g wazo-demo-programmable /var/run/wazo-demo-programmable/ \
    && install -o wazo-demo-programmable -g wazo-demo-programmable /dev/null /var/log/wazo-demo-programmable.log \
    && apt-get -yqq autoremove \
    && openssl req -x509 -newkey rsa:4096 -keyout /usr/share/xivo-certs/server.key -out /usr/share/xivo-certs/server.crt -nodes -config /usr/share/xivo-certs/openssl.cfg -days 3650 \
    && chown wazo-demo-programmable:wazo-demo-programmable /usr/share/xivo-certs/*

COPY . /usr/src/wazo-demo-programmable
WORKDIR /usr/src/wazo-demo-programmable
RUN true \
  && pip install -r /usr/src/wazo-demo-programmable/requirements.txt \
  && python setup.py install \
  && cp -r etc/* /etc

EXPOSE 9400

CMD ["wazo-demo-programmable"]
