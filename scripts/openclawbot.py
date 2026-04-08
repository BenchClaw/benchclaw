import os
from typing import Any
import json

try:
    import json5  # type: ignore[import-not-found]
except Exception:
    json5 = None

class OpenclawBot:
    """
    负责从用户目录 ~/.openclaw/openclaw.json 读取关键信息：
    - 版本号
    - 模型列表
    - 默认 primary / fallbacks 模型
    - 网关端口、模式及认证方式（token / password）
    """

    def __init__(self, config_path: str | None = None) -> None:
        self.config_path = (
            config_path
            or os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
        )

        self.openclaw_root = os.path.join(os.path.expanduser("~"), ".openclaw")

        self.raw_config: dict[str, Any] = {}

        # 元信息
        self.version: str | None = None

        # 模型相关
        self.models: dict[str, Any] = {}
        self.primary_model: str | None = None
        self.fallback_models: list[str] = []

        self._load()

    def _load(self) -> None:
        """读取并解析 openclaw.json，忽略读取和解析错误。"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError:
            return

        data: dict[str, Any] | None = None
        # 优先使用 json5（若可用），否则退回标准 json
        if json5 is not None:
            try:
                data_obj = json5.loads(text)  # type: ignore[call-arg]
                if isinstance(data_obj, dict):
                    data = data_obj
            except Exception:
                data = None
        if data is None:
            try:
                data_obj = json.loads(text)
                if isinstance(data_obj, dict):
                    data = data_obj
            except Exception:
                data = None

        if data is None:
            return

        self.raw_config = data
        self._extract_version()
        self._extract_models()

    def _extract_version(self) -> None:
        """解析版本号。

        优先顺序：
        1. 顶层字段 version
        2. meta.lastTouchedVersion
        3. meta.version
        """
        v: Any = self.raw_config.get("version")

        if v is None:
            meta = self.raw_config.get("meta")
            if isinstance(meta, dict):
                v = (
                    meta.get("lastTouchedVersion")
                    or meta.get("version")
                )

        if isinstance(v, (str, int, float)):
            self.version = str(v)

    def _extract_models(self) -> None:
        cfg = self.raw_config

        agents_cfg = cfg.get("agents")
        defaults: dict[str, Any] | None = None
        if isinstance(agents_cfg, dict):
            maybe_defaults = agents_cfg.get("defaults")
            if isinstance(maybe_defaults, dict):
                defaults = maybe_defaults

        # model: { primary, fallbacks }
        model_cfg: dict[str, Any] | None = None
        if defaults and isinstance(defaults.get("model"), dict):
            model_cfg = defaults["model"]  # type: ignore[index]
        else:
            maybe_model = cfg.get("model")
            if isinstance(maybe_model, dict):
                model_cfg = maybe_model

        if model_cfg is not None:
            primary = model_cfg.get("primary") or model_cfg.get("id")
            if isinstance(primary, str) and primary.strip():
                self.primary_model = primary.strip()

            fallbacks = model_cfg.get("fallbacks")
            if isinstance(fallbacks, list):
                self.fallback_models = [
                    str(m).strip() for m in fallbacks if str(m).strip()
                ]

        # models: 模型白名单/目录
        models_cfg: dict[str, Any] | None = None
        if defaults and isinstance(defaults.get("models"), dict):
            models_cfg = defaults["models"]  # type: ignore[index]
        else:
            maybe_models = cfg.get("models")
            if isinstance(maybe_models, dict):
                models_cfg = maybe_models

        if models_cfg is not None:
            self.models = models_cfg

def main()->None:
    bot = OpenclawBot()  # 默认读 ~/.openclaw/openclaw.json
    print("版本:", bot.version)
    print("Primary 模型:", bot.primary_model)
    print("Fallbacks:", bot.fallback_models)
    print("模型列表 keys:", list(bot.models.keys()))

if __name__ == "__main__":
    main()
