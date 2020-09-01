FROM python:3.8 as build
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim
COPY --from=build /root/.local/bin /root/.local
COPY src/ .
ENV PATH=/root/.local:$PATH

CMD ["python", "./bookworkout.py"]
