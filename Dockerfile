FROM python:slim
ENV MATRIX_ELEMENTS=1,2,7,4,5,6,2,8,1
COPY . .
RUN mkdir /results
RUN pip3 install -r requirements.txt
ENTRYPOINT python3
CMD script.py 3 3