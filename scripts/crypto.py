"""
BenchClaw 加解密模块。

算法：AES-256-GCM
依赖：cryptography >= 42.0（已在 pyproject.toml 中声明）
密钥：Base64 编码的 32 字节密钥，从环境变量 BENCHCLAW_CLIENT_KEY 读取，
      fallback 到 config.BENCHCLAW_CLIENT_KEY。

格式：Base64( IV[12B] + Ciphertext + Tag[16B] )

用法：
  from crypto import client_encrypt, client_decrypt

  gpv = client_encrypt({"key": "value"})   # dict/list → 加密字符串
  obj = client_decrypt(gpv)                # 加密字符串 → dict/list
"""
from __future__ import annotations

import base64
import json
import os
from typing import Any
from config import BENCHCLAW_CLIENT_KEY as _cfg_key

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# AES-GCM 参数
_IV_LEN  = 12   # bytes
_TAG_LEN = 16   # bytes


def _get_key() -> bytes:
    """
    读取 AES-256 密钥（32 字节）。
    优先级：环境变量 BENCHCLAW_CLIENT_KEY > config.BENCHCLAW_CLIENT_KEY
    """
    raw = _cfg_key.strip()
    key = base64.b64decode(raw)
    if len(key) != 32:
        raise RuntimeError(f"密钥长度错误：期望 32 字节，实际 {len(key)} 字节")
    return key


def client_encrypt(data: Any) -> str:
    """
    序列化 + AES-256-GCM 加密 + Base64 编码。

    Parameters
    ----------
    data : dict | list | str | bytes
        待加密数据，dict/list 自动序列化为 JSON。

    Returns
    -------
    str
        Base64( IV[12B] + Ciphertext + Tag[16B] )
    """
    key = _get_key()
    iv  = os.urandom(_IV_LEN)

    if isinstance(data, bytes):
        plaintext = data
    elif isinstance(data, str):
        plaintext = data.encode("utf-8")
    else:
        plaintext = json.dumps(data, ensure_ascii=False).encode("utf-8")

    # AESGCM.encrypt 返回 ciphertext + tag（tag 在末尾 16B）
    ct_tag = AESGCM(key).encrypt(iv, plaintext, None)
    blob = iv + ct_tag
    return base64.b64encode(blob).decode("ascii")


def client_decrypt(gpv: str) -> Any:
    """
    Base64 解码 + AES-256-GCM 解密 + 反序列化。

    Parameters
    ----------
    gpv : str
        client_encrypt 返回的加密字符串。

    Returns
    -------
    dict | list | str
        解密后的数据，优先尝试 JSON 反序列化。
    """
    key  = _get_key()
    blob = base64.b64decode(gpv)

    min_len = _IV_LEN + _TAG_LEN
    if len(blob) < min_len:
        raise ValueError(f"密文太短：{len(blob)} 字节，最小需要 {min_len} 字节")

    iv     = blob[:_IV_LEN]
    ct_tag = blob[_IV_LEN:]    # ciphertext + tag

    plaintext = AESGCM(key).decrypt(iv, ct_tag, None)

    text = plaintext.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


# ─────────────────────────────────────────────
# CLI 工具入口
# ─────────────────────────────────────────────

def _genkey() -> str:
    """生成新的 32 字节 AES-256 密钥，返回 Base64 字符串。"""
    key_bytes = os.urandom(32)
    return base64.b64encode(key_bytes).decode("ascii")


def _selfcheck() -> bool:
    """加解密往返自检，验证算法和密钥配置正确。"""
    test_cases: list[Any] = [
        {"model_name": "gpt-4o", "client_version": "1.0.0"},
        {"session_id": "BC_1234567890_abcd", "total_score": 850, "s1": 250},
        {"nested": {"a": 1, "b": [1, 2, 3]}, "中文": "测试"},
    ]
    all_pass = True
    for i, data in enumerate(test_cases, 1):
        gpv = client_encrypt(data)
        recovered = client_decrypt(gpv)
        ok = (recovered == data)
        print(f"  Case {i}: {'✅' if ok else '❌'}  {json.dumps(data, ensure_ascii=False)[:50]}")
        if not ok:
            all_pass = False

    # 验证 IV 随机性
    e1 = client_encrypt({"t": 1})
    e2 = client_encrypt({"t": 1})
    iv_ok = (e1 != e2)
    print(f"  IV随机: {'✅' if iv_ok else '❌'}  同明文两次加密结果不同")
    return all_pass and iv_ok


if __name__ == "__main__":
    import argparse as _ap

    parser = _ap.ArgumentParser(description="BenchClaw 加解密工具 (AES-256-GCM)")
    parser.add_argument("--key", "-k", help="覆盖密钥（Base64），默认读取 BENCHCLAW_CLIENT_KEY")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("genkey", help="生成新的 32 字节 AES-256 密钥")

    p_enc = sub.add_parser("encrypt", help="加密 JSON 字符串")
    p_enc.add_argument("data", help='待加密的 JSON，如 \'{"key":"value"}\'')

    p_dec = sub.add_parser("decrypt", help="解密 gpv 字符串")
    p_dec.add_argument("data", help="待解密的 Base64 gpv 字符串")

    sub.add_parser("check", help="往返自检，验证加解密正确性")

    args = parser.parse_args()

    if args.key:
        os.environ["BENCHCLAW_CLIENT_KEY"] = args.key

    if args.cmd == "genkey":
        key = _genkey()
        print(f"新密钥（Base64）:\n{key}")
        print(f"Hex: {base64.b64decode(key).hex()}")

    elif args.cmd == "encrypt":
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"错误：输入不是合法 JSON：{e}")
            raise SystemExit(1)
        print(client_encrypt(data))

    elif args.cmd == "decrypt":
        result = client_decrypt(args.data)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "check":
        print("往返自检：")
        ok = _selfcheck()
        raise SystemExit(0 if ok else 1)
