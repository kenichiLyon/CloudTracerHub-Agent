# lubster-Agent 使用说明

如果你是评委或需要快速完成比赛演示，建议优先阅读 `评委使用说明.md`。

## 1. 项目目标

本项目已完成从 CloudConfigGuard 到 `lubster` 的迁移，当前只保留 `lubster` 诊断能力。
项目提供两种使用方式：CLI 诊断器与 MCP Server，不提供 WebUI。
其中 `lubster-agent` 是对 `lubster` 核心诊断引擎的工程化封装：CLI 直接调用 `lubster`，MCP Server 则把同一套诊断能力暴露给外部客户端。

诊断方法固定为五层链路：

1. 现象
2. 资源
3. 服务
4. 依赖
5. 变更

并通过以下工具源采集证据：

- `kubectl`
- `promql`
- `log_ql`
- `trace_analyzer`
- `runbook_search`

## 2. 推荐环境管理方式

本项目推荐使用 `uv` 管理 Python 版本、虚拟环境与依赖。

首次进入项目根目录后执行：

```bash
uv python pin 3.13
uv sync --extra dev
```

说明：

- `uv python pin 3.13` 会让项目固定使用 Python 3.13
- `uv sync --extra dev` 会根据 `pyproject.toml` 创建 `.venv` 并安装开发依赖
- `.venv` 属于当前机器的本地环境，不应拷贝到其他电脑，也不应提交到仓库；换机器后请直接重新执行 `uv sync --extra dev`

激活虚拟环境：

```bash
.venv\Scripts\activate
```

如果不想手动激活，也可以直接使用：

```bash
uv run python -m pytest -q
```

## 3. 安装与启动

直接运行样例：

```bash
uv run lubster --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
```

也可以使用项目同名入口：

```bash
uv run lubster-agent --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
```

## 4. MCP 模式

启动 MCP Server：

```bash
uv run lubster-mcp
```

项目同名入口也可直接使用：

```bash
uv run lubster-agent-mcp
```

也可以使用以下等价方式启动：

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

## 5. CLI 调用方式

### 5.1 使用项目同名入口

```bash
uv run lubster-agent --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
```

### 5.2 使用兼容入口

```bash
uv run lubster --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format pretty
```

### 5.3 直接以模块运行

```bash
uv run python -m lubster --config examples/lubster.config.json --incident-file examples/incidents/pod_crashloop.json --format json
```

也支持直接传 incident JSON：

```bash
uv run lubster --config examples/lubster.config.json --incident-json "{\"title\":\"api 5xx\",\"namespace\":\"default\",\"service\":\"api\",\"symptoms\":[\"5xx\",\"timeout\"],\"time_window_minutes\":30}" --format json
```

参数说明：

- `--config`：lubster 配置文件
- `--incident-file`：故障输入文件
- `--incident-json`：故障输入 JSON 文本
- `--format`：`pretty` 或 `json`

## 6. MCP 客户端配置示例

如果客户端支持 stdio MCP，可参考：

```json
{
  "mcpServers": {
    "lubster-agent": {
      "command": "uv",
      "args": ["run", "lubster-agent-mcp"],
      "cwd": "G:/your-path/lubster-Agent",
      "env": {
        "lubster_CONFIG": "G:/your-path/lubster-Agent/examples/lubster.config.json"
      }
    }
  }
}
```

## 7. 配置与示例数据

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

默认 incident 示例：

`examples/incidents/pod_crashloop.json`

演示数据位于：

- `examples/video_demo/lubster.video.config.json`
- `examples/video_demo/incidents/01_checkout_redis_timeout.json`
- `examples/video_demo/incidents/02_payment_signature_failure.json`
- `examples/video_demo/incidents/03_recommendation_backlog.json`

## 8. 接入 Lobster

**前提条件：Lobster 需要与待诊断的云原生服务位于同一台机器，或至少能访问同一套服务环境。**

为了方便初始化 Lobster，本项目提供了一组基础配置文件，位于 `lubster_base_config/`：

- `lubster_base_config/identity.yml`：身份设定，定义为云原生 SRE / 故障排障专家
- `lubster_base_config/personal.yml`：交互风格设定，控制沟通语气、提问方式和故障场景下的话术
- `lubster_base_config/workflow.yml`：工作流设定，固定五层排障路径与故障响应方法论

建议按以下步骤接入：

1. 安装 `lobsterAI` 或兼容客户端（如 `QClaw` 等）
2. 将本项目下载或克隆到目标机器
3. 使用 `lubster_base_config/` 下的三个文件替换 Lobster 初始配置
4. 启动本项目提供的 MCP 服务：

```bash
uv run lubster-agent-mcp
```

5. 在 Lobster 中明确指定：
   - 使用本项目作为故障诊断工具入口
   - 优先通过 `lubster-agent` / `lubster` 提供的工具链访问服务
   - 不要绕过本项目，私自直接连接并操作 `docker`、`k8s` 等环境

如果你要做比赛演示，推荐直接使用演示数据：

```bash
uv run lubster --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/01_checkout_redis_timeout.json --format pretty
```

给 Lobster 的初始化指令可以参考：

```text
请使用当前项目作为云原生故障诊断工具入口，并使用 lubster_base_config/identity.yml、lubster_base_config/personal.yml、lubster_base_config/workflow.yml 初始化你的身份、风格和工作流。后续诊断时请优先通过本项目提供的 CLI 或 MCP 工具访问服务，不要自行直接操作 docker、k8s 或其他容器平台。
```

## 9. 测试方式

```bash
uv run pytest -q
```
