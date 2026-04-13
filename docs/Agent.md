# CloudTracerHub-agent

## 项目目标

本项目已完成从 CloudConfigGuard 到 lubster 的迁移，当前只保留 lubster 诊断能力。
项目提供两种使用方式：CLI 诊断器与 MCP Server，不提供 WebUI。
其中 `lubster-agent` 是项目中面向 `lubster` 生态的诊断能力封装名：CLI 直接调用 `lubster`，MCP Server 则把同一套诊断能力暴露给外部客户端。
对外命令入口统一使用 `cloudtracerhub-agent` 与 `cloudtracerhub-agent-mcp`。

诊断方法固定为五层链路：

1. 现象
2. 资源
3. 服务
4. 依赖
5. 变更

并通过以下工具源采集证据：

- kubectl
- promql
- log_ql
- trace_analyzer
- runbook_search

## 安装与启动

```bash
uv python pin 3.13
uv sync --extra dev
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json --format pretty
```

也可以直接调用底层模块：

```bash
uv run python -m lubster --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json --format pretty
```

说明：

- 建议始终通过 `uv sync` 在当前机器重建 `.venv`，不要拷贝已有 `.venv` 到其他电脑
- 如果不想手动激活虚拟环境，直接使用 `uv run ...` 即可

## MCP 模式

启动 MCP Server：

```bash
uv run cloudtracerhub-agent-mcp
```

也可以直接运行模块：

```bash
uv run python -m lubster.mcp_main
uv run python mcp_main.py
```

当前暴露一个工具：

- `lubster_agent_diagnose`
- `lubster_diagnose`（兼容旧名称）

工具输入：

- `incident`
- `config_path`（可选，不传时默认读取内置 `default_config.json`，也可通过 `lubster_CONFIG` 指定）

工具输出：

- `structuredContent`
- `content`
- `isError`

## 调用方式

### 1) 使用 incident 文件

```bash
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-file examples/incidents/unified_auth_timeout.json
```

### 2) 直接传 incident JSON

```bash
uv run cloudtracerhub-agent --config examples/lubster.config.json --incident-json "{\"title\":\"api 5xx\",\"namespace\":\"default\",\"service\":\"api\",\"symptoms\":[\"5xx\",\"timeout\"],\"time_window_minutes\":30}" --format json
```

参数说明：

- `--config`：lubster 配置文件
- `--incident-file`：故障输入文件
- `--incident-json`：故障输入 JSON 文本
- `--format`：`pretty` 或 `json`

## MCP 客户端配置示例

Claude Desktop 或其他支持 stdio MCP 的客户端可配置为：

```json
{
  "mcpServers": {
    "cloudtracerhub-agent": {
      "command": "uv",
      "args": ["run", "cloudtracerhub-agent-mcp"],
      "env": {
        "lubster_CONFIG": "G:/your-path/CloudTracerHub-agent/examples/lubster.config.json"
      }
    }
  }
}
```

如果未全局安装脚本，也可以直接使用 Python：

```json
{
  "mcpServers": {
    "cloudtracerhub-agent": {
      "command": "uv",
      "args": ["run", "python", "-m", "lubster.mcp_main"],
      "cwd": "G:/your-path/CloudTracerHub-agent",
      "env": {
        "lubster_CONFIG": "G:/your-path/CloudTracerHub-agent/examples/lubster.config.json"
      }
    }
  }
}
```

## 配置说明

默认样例配置文件为：

`examples/lubster.config.json`

核心字段：

- `mock_mode`：是否使用模拟数据
- `kubectl_bin`：kubectl 可执行文件
- `command_timeout_sec`：命令超时秒数
- `http_timeout_sec`：HTTP 超时秒数
- `promql_endpoint`：指标查询接口
- `log_ql_endpoint`：日志查询接口
- `trace_endpoint`：链路分析接口
- `runbook_endpoint`：runbook 检索接口

## 示例 incident

`examples/incidents/unified_auth_timeout.json`

字段包括：

- `title`
- `namespace`
- `service`
- `symptoms`
- `time_window_minutes`
- `suspect_pod`

## 接入 Lobster

**前提条件：Lobster 需要与待诊断的云原生服务位于同一台机器，或至少能访问同一套服务环境。**

为了方便初始化 Lobster，本项目提供了一组基础配置文件，位于 `lubster_base_config/`：

- `lubster_base_config/identity.yml`：身份设定，定义为云原生 SRE / 故障排障专家
- `lubster_base_config/personal.yml`：交互风格设定，控制沟通语气、提问方式和故障场景下的话术
- `lubster_base_config/workflow.yml`：工作流设定，固定五层排障路径与故障响应方法论

建议按以下步骤接入：

1. 在服务所在机器安装 `lobsterAI` 或兼容客户端（如 `QClaw` 等）
2. 将本项目下载或克隆到目标机器
3. 使用 `lubster_base_config/` 下的三个文件替换 Lobster 初始配置
4. 启动本项目提供的 MCP 服务：

```bash
uv run cloudtracerhub-agent-mcp
```

5. 在 Lobster 中明确指定：
   - 使用本项目作为故障诊断工具入口
   - 优先通过 `cloudtracerhub-agent` 或 `python -m lubster` 提供的工具链访问服务
   - 不要绕过本项目，私自直接连接并操作 `docker`、`k8s` 等环境

如果仅需要演示使用，推荐直接使用演示数据：

```bash
uv run cloudtracerhub-agent --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/01_course_selection_timeout.json --format pretty
```

给 Lobster 的初始化指令可以参考：

```text
请使用当前项目作为云原生故障诊断工具入口，并使用 lubster_base_config/identity.yml、lubster_base_config/personal.yml、lubster_base_config/workflow.yml 初始化你的身份、风格和工作流。后续诊断时请优先通过本项目提供的 CLI 或 MCP 工具访问服务，不要自行直接操作 docker、k8s 或其他容器平台。
```

## 测试

```bash
uv run pytest -q
```
