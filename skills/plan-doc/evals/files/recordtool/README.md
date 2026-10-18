# recordtool

本地单用户命令行工具，用于管理个人记录，数据保存在 `~/.recordtool/records.json`。

```bash
recordtool add "标题" --tag work
recordtool list
recordtool export --format csv --out records.csv   # 或 --format json
```

运行测试：`python -m pytest tests`
