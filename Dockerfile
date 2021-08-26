# 基于的基础镜像
FROM python:3.8.10
WORKDIR /app
RUN pip install python-gitlab
RUN pip install urllib3
RUN pip install datetime
COPY . .
COPY app/client.py /usr/local/lib/python3.8/site-packages/gitlab/client.py
CMD ["python","app/gitlab-outsourcing-users.py"]
