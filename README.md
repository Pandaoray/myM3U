# myM3U 项目说明

## 项目简介

myM3U 是一个用于自动化生成自定义 IPTV m3u 播放列表的工具。通过关键词白名单（KEYWORDS）与黑名单（BLACKLIST）灵活筛选频道，支持本地运行与 GitHub Actions 自动化，便于快速部署和持续更新。支持将生成的 m3u 列表通过 GitHub Pages 发布，方便在线访问。

---

## 核心功能

- **关键词白名单/黑名单过滤**：自定义 KEYWORDS（白名单）与 BLACKLIST（黑名单），精准筛选频道。
- **自动化生成 m3u 列表**：支持本地一键生成与 GitHub Actions 自动化。
- **GitHub Pages 发布**：自动将 output/ 目录下的 custom.m3u 发布为网页，可直接在线访问。
- **易于扩展**：支持未来功能拓展，如频道失效检测、外部配置、Web UI 等。

---

## 快速部署与使用指南

### 1. 本地运行

1. 安装 Python 3.7 及以上版本。
2. 克隆本仓库：
   ```bash
   git clone https://github.com/yourname/myM3U.git
   cd myM3U
   ```
3. 安装依赖（如有）：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置关键词（见下文 KEYWORDS/BLACKLIST 配置说明）。
5. 运行生成脚本：
   ```bash
   python scripts/generate_m3u.py
   ```
6. 生成的 m3u 文件位于 `output/custom.m3u`。

### 2. GitHub Actions 自动化

- 项目已内置 `.github/workflows/build.yml`，推送代码后自动运行生成脚本并更新 `output/custom.m3u`。
- 可通过 Actions 页面查看自动化日志与结果。

---

## 关键词自定义说明

### 1. KEYWORDS（白名单）与 BLACKLIST（黑名单）配置方法

- **KEYWORDS**：仅包含频道名中含有这些关键词的频道。
- **BLACKLIST**：排除频道名中含有这些关键词的频道。
- **优先级**：黑名单优先于白名单（即频道名同时命中 KEYWORDS 和 BLACKLIST 时，频道会被排除）。

#### Python 配置示例

在 [`scripts/generate_m3u.py`](scripts/generate_m3u.py:1) 文件中，按如下方式配置：

```python
# 关键词白名单
KEYWORDS = [
    "CCTV", "卫视", "体育", "电影"
]

# 关键词黑名单
BLACKLIST = [
    "测试", "购物", "广告"
]
```

> **注意**：请根据实际需求自定义 KEYWORDS 和 BLACKLIST 列表内容。

---

## GitHub Pages 发布说明

1. 进入仓库设置（Settings）→ Pages。
2. 选择 `output/` 目录作为 Pages 源（Source）。
3. 保存后，访问 `https://yourname.github.io/myM3U/custom.m3u` 即可获取最新 m3u 列表。

---

## 未来可扩展方向

- **频道失效检测**：自动检测并剔除失效频道，提升可用性。
- **关键词外部配置**：支持通过外部文件（如 JSON/YAML）配置 KEYWORDS/BLACKLIST，便于非开发者修改。
- **Web UI 管理**：开发可视化界面，支持在线配置关键词、预览和下载 m3u 列表。
- **多源合并与去重**：支持多源 m3u 合并、频道去重等高级功能。

---

## 文档结构与使用建议

- **结构清晰**：分为项目简介、核心功能、部署指南、关键词配置、Pages 发布、扩展方向等部分。
- **内容简明**：每一部分均有简要说明与操作示例，适合新手快速上手。
- **关键点覆盖**：涵盖所有实际使用与配置场景，便于后续维护与扩展。