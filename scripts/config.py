"""
BenchClaw 全局配置常量。
修改此文件即可调整运行参数，无需改动业务代码。
"""
# ---------- APP ----------
CLIENT_VERSION = '1.0.0'

# ---------- 加解密 ----------
# AES-256-GCM 密钥（Base64 编码，32 字节）
# 可通过环境变量 BENCHCLAW_CLIENT_KEY 覆盖
BENCHCLAW_CLIENT_KEY = "T1ELQGiDLP0mEpwDOVsWrktwtWgcyr1q621wFkmj6fY="

# ---------- API ----------
BENCHCLAW_API_HOST = "benchclawapi.antutu.com"  # API 域名，更换时只需修改这里
DEFAULT_API_URL = f"https://{BENCHCLAW_API_HOST}/api/v1/tests/request"
DEFAULT_SUBMIT_API_URL = f"https://{BENCHCLAW_API_HOST}/api/v1/tests/submit"

# ---------- Gateway WebSocket ----------
DEFAULT_WS_URL = "ws://127.0.0.1:18789"
PROTOCOL_VERSION = 3

# ---------- 会话 & 超时 ----------
DEFAULT_SESSION_ID = "main"
DEFAULT_TIMEOUT_SEC = 300  # 单题最长等待秒数
DEFAULT_SESSION_PREFIX = "benchclaw_session_"

# ---------- 上传数据截断配置 ----------
# stdout 内容截断长度（字符数），防止上传数据过大
UPLOAD_STDOUT_TRUNCATE_LENGTH = 2000
# stderr 内容截断长度（字符数）
UPLOAD_STDERR_TRUNCATE_LENGTH = 500