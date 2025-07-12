import redis
import os

# Replace with your actual Railway Redis URL
redis_url = os.getenv("REDIS_URL", "redis://default:your_password@your_host:your_port")
client = redis.Redis.from_url(redis_url)

try:
    client.set("testkey", "hello")
    print("✅ Redis connected!")
    print("testkey =", client.get("testkey"))
except Exception as e:
    print("❌ Redis connection failed:", e)
