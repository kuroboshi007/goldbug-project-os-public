# goldBug Project OS

`goldBug Project OS` 是 k.goldbug.studio 與 AI 協作者建立的一套小型、可版本控管的專案規則、操作手冊與範本。

[English](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

## 適用對象

適合需要跨對話保留專案範圍、目前狀態、已接受決策、審查責任與交接資訊的維護者及 AI 協作者。將最小範本組複製到專案、填入已確認事實，再依操作手冊推進工作。

這是一套專案運作框架，不是電腦作業系統，也不是需要安裝的應用程式。它不會自動建立專案、執行代理、同步筆記或發布儲存庫。這份本地候選版的公開儲存庫網址與發布仍待核准。

三份 README 提供語意一致的入門說明；連結的規則與範本目前以英文撰寫。請遵循唯一的 [AGENTS.md 閱讀順序](AGENTS.md#required-read-order)，設定與政策細節以連結文件為準。

## 必要工具

- 隨附腳本需要 Bash、Git、jq 與標準 `head`。
- 測試套件需要 Python 3.9 或更新版本。
- 自訂時區需要可信任、已安裝的 IANA zoneinfo 資料；預設 `Etc/UTC` 不需要該資料。
- 只有採用 issue／PR 工作流程時才需要 GitHub 儲存庫及存取權；本地快速開始不需要筆記帳號或選用服務。

腳本在 Bash 環境中執行。原生 Windows 執行尚未驗證，請確認所用環境的工具及時區資料。下方離線連結檢查可選用 `lychee`。

## 最小本地快速開始

從包含本 README 的目錄執行。此例會建立全新的相鄰目錄；若 `../my-project` 已存在，請改用新名稱，不要覆寫。

```bash
bash scripts/project-os-config.sh &&
mkdir ../my-project &&
cp templates/AGENTS.md templates/PROJECT.md templates/STATUS.md templates/DECISIONS.md ../my-project/
```

未選取設定檔時，第一個指令會輸出 `configuration source: off — no configuration`。新目錄會包含四份文件：

| 文件 | 交給代理工作前要填寫的內容 |
| --- | --- |
| `AGENTS.md` | 專案名稱、權責、安全規則、驗證指令，以及實際可存取的共用政策位置／checkout 提示 |
| `PROJECT.md` | 使用者、目標、非目標、技術架構與已知驗證指令 |
| `STATUS.md` | 目前狀態、下一步、阻礙與風險 |
| `DECISIONS.md` | 已接受的決策；未決問題保持未確認 |

以已確認資訊取代範本佔位文字，未知事項標記為 `To confirm`。不要把佔位文字當成網址、指令或 Git 身分執行。這裡不假設任何公開上游網址；`upstream.url` 未設定時，不進行 clone。請代理先閱讀專案規則與文件，再提出一項範圍明確的任務及驗證計畫。只有需要時才加入任務、交接或 ADR 範本；Claude 使用者也可複製 `templates/CLAUDE.md`。

既有專案應先檢查並對照現有文件及安全規則，不要直接替換。完整導入、工作流程檔案與審查步驟請見 [Bootstrap a Project](playbooks/bootstrap-project.md)。

## 設定與私人資訊

不一定需要設定檔。預設使用中立的維護者名稱、`Etc/UTC`、筆記模式 `none`，不強制提交 email，不啟用 portfolio，也不啟用選用公告服務。

若要自訂新的本地副本，可依[合成範例](.config/project-os.example.json)建立被 Git 忽略的 `.config/project-os.local.json`，或從最小有效設定開始：

```json
{"schema_version": 1}
```

已有本地設定檔時請編輯，不要覆寫。在 OS 目錄中驗證：

```bash
bash scripts/project-os-config.sh
```

選取本地設定檔時會輸出 `configuration source: on — local profile`。設定以整份檔案的優先順序選取，不合併欄位：

```text
PROJECT_OS_PROFILE → .config/project-os.local.json → private/project-os.json → built-in defaults
```

公開候選版不包含私人試行設定檔。完整範例是虛構資料；啟用服務前，先替換範例目的地。私人目的地與實際專案清單不要放入公開內容，任何設定檔都不可存放憑證。選取的設定檔若缺失、無法讀取、JSON 格式錯誤或內容無效，會阻止相依工作；不要改用預設值繞過錯誤。詳見[設定契約](docs/configuration.md)。

時區建議使用 IANA 的標準 `Area/Location` 名稱，例如 `Asia/Tokyo` 或 `America/New_York`。`US/Eastern` 等舊別名只有在主機可信任的 zoneinfo 資料庫包含對應、可讀取的 TZif 檔案時才有效；不同主機的可用別名可能不同。預設 `Etc/UTC` 是特殊的已知值。Windows 顯示名稱、前後空白、控制字元及路徑穿越會直接被拒絕，不會先修剪。只有需要時才使用可信任的 `TZDIR` 資料。驗證檢查名稱／檔案是否存在及 TZif magic，不計算 UTC offset 或夏令時間，也不完整解析 TZif 或認證資料真實性。詳見[時區驗證](docs/configuration.md#timezone-validation)。

## 選用整合

[筆記模式](docs/notes.md)預設為 `none`，不需要帳號、目的地、摘要交付或待完成同步。`markdown` 會為已核准的資料夾準備已確認摘要；`notion` 需要已授權的服務存取權及設定好的目的地／schema。任何外部寫入前，都要遵循確認及交付規則。設定檔與腳本不會自動同步。

Portfolio 追蹤與公告頻道均為選用功能，預設關閉。即使設定已啟用公告頻道，各產品仍要明確決定是否使用；共用服務不是所有專案的必要依賴。詳見[專案生命週期](docs/project-lifecycle.md)與[公告頻道](knowledge/shared-announcement-channel.md)。

## 工作流程與角色

1. 維護者核准結果，決定重要的產品、隱私、發布及合併事項。
2. 代理建立範圍明確的 GitHub issue，在分支上實作並開啟 draft PR。
3. 另一位代理審查完整變更及證據。
4. 維護者處理剩餘決策並合併。
5. 只對已確認資訊套用所選筆記模式，再以獨立 OS issue／PR 推廣可重用的學習。

GitHub 保存工作紀錄；專案文件保存專案事實與已接受決策。筆記保存供人閱讀的已確認摘要，不建立另一套任務狀態。交接時記錄 OS revision 與 configuration source。代理提交須遵循[作者標記](AGENTS.md#authorship-marks)中的附產品名稱的連續 trailers；顯示用設定欄位不會設定 Git 身分。詳見[運作模型](docs/operating-model.md)、[協作](docs/ai-collaboration.md)及[審查](playbooks/review-change.md)。

## 驗證與匯出

在 OS 目錄中執行隨附測試；它們使用隔離的合成測試環境：

```bash
python3 tests/test-core-review.py
python3 tests/test-export.py
```

匯出需要已有 commit 的 Git checkout。解壓縮的封存檔不含 Git 歷史；要匯出，請先用自己已驗證的公開身分建立本地 Git 並提交已審查快照。匯出工具不會初始化 Git、選擇身分、提交或發布。先提交會被匯出的修改，再指定全新目的地：

```bash
bash scripts/export-candidate.sh ../public-candidate
```

明確的[允許清單](export/manifest.txt)包含三份 README 與 `LICENSE`。每個檔案均取自當次擷取的 commit，保留執行權限。`PROJECTS.md` 使用合成專案清單；`archive/README.md` 使用內嵌通用範本。私人設定檔、本地設定、歷史與未列入檔案不會匯出。既有目的地、不安全路徑、符號連結及未提交的匯出來源會被拒絕。把檔案加入 Git 不等於加入允許清單。

若已安裝 `lychee`，文件指定的離線檢查為：

```bash
lychee --offline --no-progress --include-fragments --exclude-path 'archive/' './**/*.md'
```

另外檢查實際匯出內容、權限、連結、檔名與隱私。Git 不保存檔案系統 xattrs、resource forks 或擁有者；直接封存資料夾可能帶出 metadata sidecars。這個工具只做本地檔案匯出，不是封存檔或隱私認證。詳見[匯出審查與封裝限制](docs/export.md)。

## 儲存庫導覽

`AGENTS.md` 保存共用規則；`docs/` 保存政策；`playbooks/` 保存流程；`templates/` 保存專案範本組。`knowledge/` 保存可重用的學習與候選做法，不會自動成為現行政策。`archive/` 是歷史資料，不是現行依據。匯出的 `PROJECTS.md` 是合成範例，不是你的實際 portfolio。

## 授權與選用專案署名

依維護者核准，這份候選版包含標準 [MIT License](LICENSE)，版權署名為 `2026 k.goldbug.studio`。MIT 允許依其條款使用、修改、商用及再散布，且不提供保證。再散布副本或重要部分時，必須保留版權與許可通知；適用的第三方通知也要保留。

顯示用署名是選用的：下游使用者可自由修改或省略這些 README 的專案 credit，並自訂 `maintainer.name`／`maintainer.handle`。這種選用的專案署名與 `LICENSE` 中必須保留的法律通知不同；修改顯示署名不會移除或取代法律通知。詳見[顯示署名](docs/configuration.md#display-attribution)。公開發布仍須由維護者另外決定。
