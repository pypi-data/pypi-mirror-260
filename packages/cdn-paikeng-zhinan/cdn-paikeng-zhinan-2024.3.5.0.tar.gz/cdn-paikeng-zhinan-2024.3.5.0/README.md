# CDN排坑指南

## 下载

### Docker

```
docker pull apachecn0/cdn-paikeng-zhinan
docker run -tid -p <port>:80 apachecn0/cdn-paikeng-zhinan
# 访问 http://localhost:{port} 查看文档
```

### PYPI

```
pip install cdn-paikeng-zhinan
cdn-paikeng-zhinan <port>
# 访问 http://localhost:{port} 查看文档
```

### NPM

```
npm install -g cdn-paikeng-zhinan
cdn-paikeng-zhinan <port>
# 访问 http://localhost:{port} 查看文档
```