FROM public.ecr.aws/docker/library/python:latest

COPY requirements.txt app.py /srv

WORKDIR /srv

ARG DEBIAN_FRONTEND="noninteractive"
ENV TZ=Australia/Sydney

RUN pip install -r requirements.txt

EXPOSE 5000/tcp

ENTRYPOINT ["python3"]
CMD ["app.py"]
