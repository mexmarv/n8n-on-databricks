# 🧱 n8n-on-Databricks (with optional LakeBase PostgreSQL Support)

Self-host [n8n](https://n8n.io/) as a [Databricks App](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html) — fully integrated inside your Lakehouse environment.

> ✅ Runs 100% inside a Databricks App, with support for:
> - **Node.js** bootstrapped from Python (`jsrunner.py`)
> - **SQLite3** persistence (default)
> - ✅ Optional: **Databricks Lakehouse PostgreSQL (Lakebase)** backend for multi-session persistence

---

## 📁 Project Structure

```
.
├── README.md
├── app.py              # Main entrypoint
├── app.yaml            # App config and environment
├── package.json        # Node dependencies
└── node-js/
    └── jsrunner.py     # Python script to bootstrap Node.js & run n8n
```

---

## ⚙️ What This App Does

This Databricks App self-hosts `n8n` automation workflows inside your workspace. It was extended from the [original `databricks-n8n`](https://github.com/hellomikelo/databricks-n8n) repo with several fixes and enhancements:

✅ Improvements:
- Works on latest Node v22.x with SQLite v5.1+
- ✅ Handles encryption key persistence and permissions inside Databricks Apps (`.n8n/config`)
- ✅ Refactored directory (`node-js/`) for cleaner organization
- ✅ Ready to switch to **Lakehouse PostgreSQL (LakeBase)** for persistent workflows and credentials

> 👨‍🔧 Built and extended by [mexmarv@gmail.com](mailto:mexmarv@gmail.com)

---

## 🚀 Deployment on Databricks

1. Clone this repo or download it as ZIP.
2. Upload files to your Databricks workspace (via UI or CLI):

```bash
databricks workspace import_dir . /Workspace/Users/your.name@databricks.com/n8n
```

3. In **Compute > Apps > Create app**, select:
   - Language: **Python**
   - App files: Folder you uploaded
   - App entrypoint: `python app.py`

⚠️ First-time deployment may take ~5 minutes (downloads Node & n8n).
Subsequent redeploys take ~10s.

---

## 🌐 Access Your n8n Instance

Once deployed, go to the **Apps** tab and open the app URL (port 8000).  
To check logs, click on the "Logs" tab in the app interface.

---

## 🔐 Encryption & Persistence

n8n stores credentials and workflows in an encrypted database.

### ✅ Option 1 — Default: SQLite

By default, n8n will use `SQLite` for internal storage:

```yaml
# app.yaml
env:
  - name: DB_TYPE
    value: sqlite
  - name: DB_SQLITE_DATABASE
    value: /app/data/database.sqlite
```

**⚠️ Warning**: If you delete the app, all SQLite data will be lost. Use PostgreSQL for persistent state.

---

### 🧪 Option 2 — Use Databricks Lakehouse PostgreSQL (Lakebase)

Lakebase is a native PostgreSQL interface on top of Unity Catalog. To enable it:

1. In `app.yaml`, replace the DB section with:

```yaml
env:
  - name: DB_TYPE
    value: postgresdb
  - name: DB_POSTGRESDB_HOST
    value: instance-xxxx.database.azuredatabricks.net
  - name: DB_POSTGRESDB_PORT
    value: 5432
  - name: DB_POSTGRESDB_DATABASE
    value: databricks_postgres
  - name: DB_POSTGRESDB_USER
    value: your_user
  - name: DB_POSTGRESDB_PASSWORD
    value: your_password
  - name: DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED
    value: 'false'
```

2. Ensure the Lakehouse PostgreSQL endpoint has a schema created (e.g. `CREATE SCHEMA n8n;`).

3. Redeploy the app.

✅ All workflows, credentials, executions, and logs will now be saved in Databricks Lakehouse with full SQL support.

---

## 📦 package.json

Make sure the following dependencies are installed:

```json
{
  "name": "n8n-with-databricks",
  "version": "1.0.0",
  "description": "n8n running on Databricks App with SQLite or PostgreSQL",
  "scripts": {
    "start": "n8n",
    "install": "npm install sqlite3 n8n"
  },
  "dependencies": {
    "n8n": "^1.45.1",
    "sqlite3": "^5.1.6"
  }
}
```

---

## 👷 Acknowledgements

- 🛠️ Based on [databricks-n8n](https://github.com/hellomikelo/databricks-n8n) by hellomikelo
- 🧠 Improved and packaged by [mexmarv@gmail.com](mailto:mexmarv@gmail.com)
- 💾 Built for real-world automation on Databricks

---

## 📄 License

MIT License — Inherited from upstream repository.
