# 录屏演示数据

这套数据专门给 `lubster` 的 `mock_mode` 使用，不依赖真实 Kubernetes、Prometheus、日志平台或链路系统，适合直接录制 CLI / MCP 操作视频。

## 文件说明

- `examples/video_demo/lubster.video.config.json`：统一的 mock 配置文件
- `examples/video_demo/incidents/01_checkout_redis_timeout.json`：结算接口 502 + Redis 超时
- `examples/video_demo/incidents/02_payment_signature_failure.json`：支付回调验签失败
- `examples/video_demo/incidents/03_recommendation_backlog.json`：推荐链路积压 + 慢查询

## 直接运行

如果你使用项目文档里的 `uv` 工作流，可以直接执行：

```bash
uv run lubster --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/01_checkout_redis_timeout.json --format pretty
uv run lubster --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/02_payment_signature_failure.json --format pretty
uv run lubster --config examples/video_demo/lubster.video.config.json --incident-file examples/video_demo/incidents/03_recommendation_backlog.json --format pretty
```

如果你录的是工程名入口，也可以把 `lubster` 替换成 `lubster-agent`。

## 推荐录制顺序

1. `01_checkout_redis_timeout.json`
   - 适合展示五层链路里“资源 + 服务 + 依赖”是如何串起来的
   - 日志、指标、trace、runbook 都比较直观
2. `02_payment_signature_failure.json`
   - 适合展示配置/证书类故障
   - 输出里有 `401`、证书版本、验签失败等关键词，观感清晰
3. `03_recommendation_backlog.json`
   - 适合展示性能劣化和依赖拖慢场景
   - 有 lag、timeout、slow query，适合讲“先止血再定位”

## 录屏建议

- 录命令行时建议使用 `--format pretty`，JSON 分层更清楚
- 如果录工具调用或二次集成，可直接把 incident 文件内容贴给 MCP 工具
- 三个场景使用同一份 config，只需要切换 incident 文件，演示节奏会更顺
