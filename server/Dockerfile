FROM tensorflow/tensorflow:2.8.0

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install ./tensorflow-2.9.0-cp38-cp38-linux_x86_64.whl

ENTRYPOINT [ "python3" ]
CMD ["server.py" ]