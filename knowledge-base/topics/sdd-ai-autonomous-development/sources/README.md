# Sources

每個來源使用一個穩定的 `source_id` 目錄：

```text
S-001/
  source.json
  raw/
    SNAP-20260531T120000Z.md
  summary.json
  summary.md
```

新增來源時：

1. 保存原始文件至 `raw/`，不要只保存網址。
2. 在 `source.json` 記錄 URL、永久連結、擷取日期、快照路徑、新鮮度與品質。
3. 使用 `prompts/document-curator-agent.md` 產生 `summary.json` 與 `summary.md`。
4. 來源更新時新增 snapshot，不要覆蓋舊檔案。

## GitHub 上傳政策

- `raw/` 預設只保存在本機，不提交至 GitHub。
- GitHub 保留 `source.json`、`summary.json`、`summary.md` 與 `CATALOG.md`。
- `source.json` 的 SHA-256 hash 用來確認本機 snapshot 是否仍與整理時一致。
- 需要跨機器共享原始 snapshot 時，另行使用具權限控管的 artifact storage，並先確認再散布權限。
