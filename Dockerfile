# 使用官方的python基础镜像
FROM python:3.10-slim


# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 复制依赖文件
COPY requirements.txt /app/requirements.txt

# 设置中国的镜像源并安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动FastAPI应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

