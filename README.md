[![Project Status](https://img.shields.io/badge/status-ready-success?style=for-the-badge)](https://github.com/MayankHenry/GLAU_ByteStorm_DELL)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=for-the-badge)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-19.2.6-blue?style=for-the-badge)](https://react.dev/)

# 🛡️ The Network Bouncer

**The Network Bouncer** is a polished threat detection platform for network traffic analytics. It analyzes UNSW-NB15-style flow data, finds suspicious port scanning and exfiltration behavior, and produces SOC-ready dashboards, reports, and mitigation commands.

---

## ✨ Why this project?

- Turn raw network flow logs into actionable incident intelligence
- Detect port scans, critical targeting, and data exfiltration risks
- Export alerts to CSV, JSON, HTML, SQLite, and Windows firewall commands
- Visualize attack signals with both generated dashboards and a React UI

---

## 🚀 What it does

- Reads single CSV files or directories of CSV files
- Detects suspicious IPs by scanning abnormal port and IP activity
- Flags critical infrastructure attacks on SSH, FTP, RDP, MySQL, MSSQL
- Evaluates exfiltration risk from large outbound byte volumes
- Applies Isolation Forest anomaly detection to augmented flow metrics
- Logs incidents locally to SQLite for audit and tracking
- Generates active defense commands for Windows Firewall

---

## 📁 Project structure

| File / Folder | Purpose |
|---|---|
| `network_bouncer.py` | Main orchestration script |
| `parser.py` | CSV ingestion and normalization |
| `detector.py` | Suspicious activity detection logic |
| `ml_model.py` | Isolation Forest anomaly detection |
| `database.py` | Incident logging to SQLite |
| `reporter.py` | CSV/HTML/JSON export and webhook support |
| `visualizer.py` | Generates charts for suspicious activity |
| `mitigation.py` | Produces Windows firewall block commands |
| `dashboard.html` | Sample generated HTML dashboard |
| `network-bouncer-ui/` | React/Vite frontend dashboard |
| `dataset/` | Local dataset folder (excluded from Git) |

---

## ✅ Features

- **Multi-file CSV ingestion** for batches or single logs
- **360° threat scoring** using signatures and ML anomaly detection
- **Critical port detection** for high-risk infrastructure access
- **JSON threat feed export** for frontend decoupling
- **SQLite incident persistence** for auditing and review
- **Interactive React dashboard** for SOC analysts
- **Windows Firewall mitigation** command generation

---

## 🧩 Requirements

Install the Python dependencies before running the engine:

```powershell
python -m pip install pandas scikit-learn matplotlib requests
```

> Recommended: Python 3.11 or later

---

## ▶️ Run the engine

From the repository root:

```powershell
python network_bouncer.py <path/to/csv-or-folder> [--max-ports 50] [--max-ips 20]
```

Example:

```powershell
python network_bouncer.py dataset
```

### CLI options

- `target` — path to a CSV file or folder with CSV files
- `--max-ports` — unique destination port threshold (default: `50`)
- `--max-ips` — unique destination IP threshold (default: `20`)

---

## 📦 Expected CSV layout

The loader reads UNSW-NB15-like flows and expects the following columns:

| Column index | Field |
|---|---|
| `0` | `srcip` |
| `1` | `sport` |
| `2` | `dstip` |
| `3` | `dsport` |
| `7` | `sbytes` |
| `8` | `dbytes` |
| `26` | `timestamp` |

Only the necessary fields are ingested; extra columns are ignored.

---

## 📤 Output files

The engine produces:

- `suspicious_activity_report.csv`
- `dashboard.html`
- `threat_feed.json`
- `suspicious_activity_chart.png`
- `threat_logs.db`

---

## 🖥️ React Dashboard

The front-end app uses the JSON feed at `network-bouncer-ui/src/threat_feed.json`.

Run the React UI locally:

```powershell
cd network-bouncer-ui
npm install
npm run dev
```

Build for production:

```powershell
cd network-bouncer-ui
npm run build
```

---

## 🔧 Optional enhancements

- Set `DISCORD_WEBHOOK_URL` in `reporter.py` for live alert delivery
- Use generated `netsh advfirewall` commands to block `CRITICAL` attackers
- Extend the React UI to fetch live JSON from the Python pipeline
- Replace sample dataset files with real network flows for live testing

---

## 💡 Notes

- The `dataset/` folder is excluded from GitHub because the raw CSVs exceed GitHub's 100 MB limit.
- Use smaller sample files or link to your own dataset source.

---

## 🙌 Contribution

This project is designed for rapid experimentation. Feel free to add:

- richer threat scoring models
- automated alert delivery channels
- API-based frontend integration
- cross-platform mitigation support

---

## 📜 License

No license file is included yet. Add one to open the project to public contribution.
