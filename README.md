# CloudTracerHub-agent

面向 `lubster` 生态的云原生故障诊断演示项目。

其中 `lubster-agent` 是项目中面向 `lubster` 生态的诊断能力名称。
对外命令入口统一使用 `cloudtracerhub-agent` 与 `cloudtracerhub-agent-mcp`。

项目提供 `CLI` 与 `MCP Server` 双入口，围绕固定的五层诊断链路：

`现象 -> 资源 -> 服务 -> 依赖 -> 变更`

统一采集 `kubectl`、日志、指标、链路和 runbook 证据，输出可复现、可解释、可继续编排的诊断结果。

> 当前仓库是演示项目，重点在于诊断方法、Agent 接入方式和稳定演示；不提供 Web UI。

## 特性

- `CLI + MCP` 双入口，既可本地命令行使用，也可作为外部 Agent 工具接入
- 固定五层排障方法，输出结构清晰，适合演示、录屏和评测
- 内置学校 / 政务场景的 mock 演示数据，不依赖真实 Kubernetes、Prometheus、日志或 Trace 平台
- 提供 `lubster_base_config/`，可直接初始化 Lobster 的身份、风格和工作流
- 使用 `uv` + `uv.lock` 管理环境，便于在不同机器上重建可迁移开发环境

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
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
```

如果你需要直接调用底层诊断引擎模块，也可以使用：

```bash
uv run python -m lubster --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
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

核心诊断工具名：

```text
lubster_agent_diagnose
lubster_diagnose
```

更完整的命令和客户端示例见 [`docs/Agent.md`](./docs/Agent.md)。

## 演示数据

仓库内已经准备了一套适合录屏和比赛演示的 mock 数据：

- 统一配置：[`examples/video_demo/lubster.video.config.json`](./examples/video_demo/lubster.video.config.json)
- 场景 1：[`examples/video_demo/incidents/01_course_selection_timeout.json`](./examples/video_demo/incidents/01_course_selection_timeout.json)
- 场景 2：[`examples/video_demo/incidents/02_gov_service_signature_failure.json`](./examples/video_demo/incidents/02_gov_service_signature_failure.json)
- 场景 3：[`examples/video_demo/incidents/03_grade_query_backlog.json`](./examples/video_demo/incidents/03_grade_query_backlog.json)
- 录屏说明：[`examples/video_demo/README.md`](./examples/video_demo/README.md)

推荐最先演示场景 1，它最容易体现五层链路是如何从症状一路定位到依赖与 runbook 建议的。

## 接入 Lobster

为了方便把本项目接入 Lobster 生态，仓库提供了一组初始化配置：

- [`lubster_base_config/identity.yml`](./lubster_base_config/identity.yml)：身份设定
- [`lubster_base_config/personal.yml`](./lubster_base_config/personal.yml)：交互风格设定
- [`lubster_base_config/workflow.yml`](./lubster_base_config/workflow.yml)：工作流设定

推荐接入步骤：

1. 在目标机器安装 `lobsterAI` 或兼容客户端
2. 将本项目下载到可访问目标服务的机器
3. 使用 `lubster_base_config/` 下的三个文件替换 Lobster 初始配置
4. 启动本项目提供的 MCP 服务：

```bash
uv run cloudtracerhub-agent-mcp
```

5. 在 Lobster 中明确要求：
   - 使用本项目作为故障诊断工具入口
   - 优先通过 `cloudtracerhub-agent` 或 `python -m lubster` 提供的工具访问服务
   - 不要绕过本项目，私自直接连接并操作 `docker`、`k8s` 等环境

如果你是在比赛或演示环境中初始化 Lobster，可以参考 [`docs/Agent.md`](./docs/Agent.md)。

## 文档导航

- 通用使用说明：[`docs/Agent.md`](./docs/Agent.md)
- Agent / 评审说明：[`docs/使用说明.md`](./docs/使用说明.md)
- 演示数据说明：[`examples/video_demo/README.md`](./examples/video_demo/README.md)

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
- 默认 incident：[`examples/incidents/pod_crashloop.json`](./examples/incidents/pod_crashloop.json)

## 开发说明

- Python 版本固定在 [`.python-version`](./.python-version)
- 依赖由 [`pyproject.toml`](./pyproject.toml) 和 [`uv.lock`](./uv.lock) 管理
- `.venv` 是本机环境产物，不应跨机器复制，也不应提交到仓库

常用命令：

```bash
uv sync --extra dev
uv run pytest -q
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
uv run cloudtracerhub-agent-mcp
```
