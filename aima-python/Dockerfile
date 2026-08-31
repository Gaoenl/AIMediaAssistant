# =========================================================
# AIMA Python AI 引擎镜像
#
# 为什么用 Docker:rocketmq-client-python 基于 C++ 库(librocketmq),
# 官方不支持 Windows,因此 Python 引擎统一以 Linux 容器方式运行。
#
# 构建:docker build -t aima-python .
# 运行:docker run -d --name aima-python \
#         -e AIMA_ROCKETMQ_NAMESERVER=<服务器IP>:9876 \
#         -e AIMA_JAVA_BASE_URL=http://host.docker.internal:8080 \
#         -p 8000:8000 aima-python
# =========================================================
FROM python:3.11-slim

# 1) 安装 librocketmq(C++ 底层库,rocketmq-client-python 的依赖)
RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0.amd64.deb \
    && dpkg -i rocketmq-client-cpp-2.0.0.amd64.deb \
    && rm rocketmq-client-cpp-2.0.0.amd64.deb \
    && apt-get purge -y wget && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) 先装依赖(利用 Docker 层缓存:requirements.txt 不变时后续构建很快)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3) 复制应用代码
COPY app ./app

EXPOSE 8000

# 4) 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
