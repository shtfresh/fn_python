FROM fnproject/python:3.6-dev as build-stage
WORKDIR /function
ADD requirements.txt /function/
RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt && rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv
ADD . /function/
RUN chmod -R 777 /function
RUN rm -fr /function/.pip_cache


FROM fnproject/python:3.6
WORKDIR /function
#COPY key ./key
RUN chmod -R 777 /function
#RUN addgroup --gid 1000 fn && \
#    adduser --uid 1000 --gid 1000 fn

COPY --from=build-stage /function /function
COPY --from=build-stage /python /python
ENV PYTHONPATH=/python

#ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]


