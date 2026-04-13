# CloudTracerHub-agent

面向 `lubster` 生态的云原生故障诊断演示项目，提供 `CLI` 与 `MCP Server` 双入口，适合比赛演示、录屏和评审体验。

对外展示口径统一为：

- `CloudTracerHub-agent`：项目名、分发名、CLI / MCP 对外入口名
- `lubster`：代码包名与底层诊断引擎名，保持不变
- `lubster-agent`：项目中对外强调的诊断能力名，用于描述它在 `lubster` 生态中的角色

项目围绕固定的五层诊断链路工作：

`现象 -> 资源 -> 服务 -> 依赖 -> 变更`

统一采集 `kubectl`、日志、指标、链路和 runbook 证据，输出可复现、可解释、可继续编排的诊断结果。

> 当前仓库是演示项目，重点在于诊断方法、Agent 接入方式和稳定演示；不提供 Web UI。

## 项目亮点

- `CLI + MCP` 双入口，同一套诊断引擎既可命令行运行，也可作为 Agent 工具接入
- 固定五层排障路径，输出结构稳定，适合录屏、答辩和现场评测
- 内置学校 / 政务场景的 mock 数据，不依赖真实 Kubernetes、Prometheus、日志或 Trace 平台
- 提供一套来自已验证部署的 `lubster` 初始化模板：[`SOUL.md`](./lubster_base_config/SOUL.md)、[`IDENTITY.md`](./lubster_base_config/IDENTITY.md)、[`AGENTS.md`](./lubster_base_config/AGENTS.md)
- 使用 [`uv`](https://docs.astral.sh/uv/) + [`uv.lock`](./uv.lock) 管理环境，便于跨机器重建可迁移开发环境

## 快速开始

### 1. 安装依赖

```bash
uv python pin 3.13
uv sync --extra dev
```

### 2. 运行一个演示场景

```bash
uv run cloudtracerhub-agent --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/01_course_selection_timeout.json --format pretty
```

### 3. 运行测试

```bash
uv run pytest -q
```

如果你只想快速了解项目，先执行第 2 步即可。

## 使用方式

### CLI

```bash
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json --format pretty
```

也可以直接调用底层模块：

```bash
uv run python -m lubster --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json --format pretty
```

支持直接传入 incident JSON：

```bash
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-json "{\"title\":\"api 5xx\",\"namespace\":\"default\",\"service\":\"api\",\"symptoms\":[\"5xx\",\"timeout\"],\"time_window_minutes\":30}" --format json
```

### MCP Server

```bash
uv run cloudtracerhub-agent-mcp
```

兼容入口：

```bash
uv run python -m lubster.mcp_main
```

核心工具名：

```text
lubster_agent_diagnose
lubster_diagnose
```

更完整的命令、参数和客户端配置示例见 [`docs/Agent.md`](./docs/Agent.md)。

## 演示数据

仓库内已经准备了一套适合录屏和比赛演示的 mock 数据：

- 统一配置：[`examples/video_demo/lubster.video.config.json`](./examples/video_demo/lubster.video.config.json)
- 场景 1：[`examples/video_demo/incidents/01_course_selection_timeout.json`](./examples/video_demo/incidents/01_course_selection_timeout.json)
- 场景 2：[`examples/video_demo/incidents/02_gov_service_signature_failure.json`](./examples/video_demo/incidents/02_gov_service_signature_failure.json)
- 场景 3：[`examples/video_demo/incidents/03_grade_query_backlog.json`](./examples/video_demo/incidents/03_grade_query_backlog.json)
- 录屏说明：[`examples/video_demo/README.md`](./examples/video_demo/README.md)

推荐最先演示场景 1，它最容易体现五层链路如何从症状一路定位到依赖与 runbook 建议。

## 接入 lubster 生态

为了方便初始化 `lubster` 生态中的 Agent，本项目提供了一组可以直接阅读和复制的基础模板，位于 [`lubster_base_config/`](./lubster_base_config/)：

- [`SOUL.md`](./lubster_base_config/SOUL.md)：回答风格、边界感和协作原则
- [`IDENTITY.md`](./lubster_base_config/IDENTITY.md)：角色身份、技术背景与处置哲学
- [`AGENTS.md`](./lubster_base_config/AGENTS.md)：工作区约定、启动流程、记忆方式与行动边界

这三份文件来自一套已经成功部署过的配置整理版，适合直接作为演示环境的初始化基线。

推荐接入步骤：

1. 在目标机器安装 `lubster` 兼容客户端
2. 将本项目下载到可访问目标服务的机器
3. 将 [`lubster_base_config/`](./lubster_base_config/) 中的三份文件复制到目标 Agent 工作区根目录
4. 如需补充本环境的集群地址、账号约束或演示边界，可在目标工作区额外创建 `USER.md`
5. 启动本项目提供的 MCP 服务：

```bash
uv run cloudtracerhub-agent-mcp
```

6. 在 `lubster` 中明确要求：
   - 使用本项目作为云原生故障诊断工具入口
   - 优先通过 `cloudtracerhub-agent` 或 `python -m lubster` 提供的工具访问服务
   - 不要绕过本项目，私自直接连接并操作 `docker`、`k8s` 等环境

如果你是在比赛或录屏环境中初始化 Agent，可进一步参考 [`docs/Agent.md`](./docs/Agent.md) 和 [`docs/使用说明.md`](./docs/使用说明.md)。

## 文档导航

- 通用接入与运行说明：[`docs/Agent.md`](./docs/Agent.md)
- 面向评委的说明：[`docs/使用说明.md`](./docs/使用说明.md)
- 录屏演示数据说明：[`examples/video_demo/README.md`](./examples/video_demo/README.md)
- `lubster` 初始化模板：
  - [`lubster_base_config/SOUL.md`](./lubster_base_config/SOUL.md)
  - [`lubster_base_config/IDENTITY.md`](./lubster_base_config/IDENTITY.md)
  - [`lubster_base_config/AGENTS.md`](./lubster_base_config/AGENTS.md)

## 项目结构

```text
.
|- README.md
|- docs/
|  |- Agent.md
|  `- 使用说明.md
|- examples/
|  |- incidents/
|  `- video_demo/
|- lubster/
|- lubster_base_config/
|- tests/
|- pyproject.toml
`- uv.lock
```

关键目录与文件：

- 核心诊断流程：[`lubster/diagnosis.py`](./lubster/diagnosis.py)
- MCP 服务实现：[`lubster/mcp_server.py`](./lubster/mcp_server.py)
- CLI 入口：[`lubster/cli.py`](./lubster/cli.py)
- 默认配置：[`examples/lubster.config.json`](./examples/lubster.config.json)
- 默认 incident：[`examples/incidents/unified_auth_timeout.json`](./examples/incidents/unified_auth_timeout.json)

## 开发说明

- Python 版本固定在 [`.python-version`](./.python-version)
- 依赖由 [`pyproject.toml`](./pyproject.toml) 和 [`uv.lock`](./uv.lock) 管理
- `.venv` 是本机环境产物，不应跨机器复制，也不应提交到仓库

常用命令：

```bash
uv sync --extra dev
uv run pytest -q
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json --format pretty
uv run cloudtracerhub-agent-mcp
uv build
```
