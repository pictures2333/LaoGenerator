強者我朋友，所以我要給他弄一個專屬(sub)domain來讓大家知道他超強!!!

### config
config.py
```python
# DOMAIN - 把這個參數設定成你的 Domain
DOMAIN:str = "example.com"
# JWT_EXP - JWT Token 有效時長
JWT_EXP:int = 60*60*12
```

docker-compose.yml
```yaml
environment:
      # JWT_KEY - 把你的 JWT Token 密鑰放在這個環境變數
      - JWT_KEY=your-jwt-key-here
      # PORT - 指定服務在 container 內監聽哪個端口
      - PORT=5000
```

### Deploy (Docker)

```bash
sudo docker-compose up -d
```