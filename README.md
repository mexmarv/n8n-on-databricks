# 🧱 n8n-on-Databricks (with optional LakeBase PostgreSQL + ClearTunnel Support)

Self-host [n8n](https://n8n.io/) as a [Databricks App](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html) — fully integrated inside your Lakehouse environment.

> ✅ Runs 100% inside a Databricks App, with support for:
> - **Node.js** bootstrapped from Python (`jsrunner.py`)
> - **SQLite3** persistence (default)
> - ✅ Optional: **Databricks Lakehouse PostgreSQL (Lakebase)** backend for multi-session persistence
> - ✅ Optional: **ClearTunnel** support to expose n8n outside Databricks securely

---

## 📁 Project Structure

```
.
├── README.md
├── app.py              # Main entrypoint
├── app.yaml            # App config and environment
├── package.json        # Node dependencies
├── node-js/
│   └── jsrunner.py     # Python script to bootstrap Node.js & run n8n
└── tunnel/
    └── cleartunnel     # Binary or wrapper for ClearTunnel (if used)
```

---

## ⚙️ What This App Does

This Databricks App self-hosts `n8n` automation workflows inside your workspace. It was extended from the [original `databricks-n8n`](https://github.com/hellomikelo/databricks-n8n) repo with several fixes and enhancements:

✅ Improvements:
- Works on latest Node v22.x with SQLite v5.1+
- ✅ Handles encryption key persistence and permissions inside Databricks Apps (`.n8n/config`)
- ✅ Refactored directory structure for modularity
- ✅ Ready to switch to **Lakehouse PostgreSQL (LakeBase)** for persistent storage
- ✅ Optional: **ClearTunnel support** to expose webhook-compatible endpoint

---

## 🚀 Deployment on Databricks

1. Clone or download the project.
2. Upload all files (including `tunnel/cleartunnel` if needed) to your workspace:
```bash
databricks workspace import_dir . /Workspace/Users/your.name@databricks.com/n8n
```
3. In **Compute > Apps > Create App**, select:
   - Language: **Python**
   - App entrypoint: `python app.py`
   - Folder: the one you uploaded

⏱️ First deployment takes ~5 min. Redeploys take ~10s.

---

## 🌐 Access Your n8n Instance

Once deployed:
- Use the **Apps** tab to open the app.
- If using **ClearTunnel**, your public URL will be shown in logs.
- You can trigger workflows using webhooks and bots like Telegram.

To verify that `n8n` is running behind ClearTunnel:

```bash
# app.py will launch cleartunnel like:
subprocess.Popen(["./tunnel/cleartunnel", "--target", "http://localhost:8000"])
```

> 💡 If using ClearTunnel, you **do not need** to hardcode the webhook URL in `app.yaml`.

---

## 🔐 Encryption & Persistence

### Default SQLite (ephemeral)

```yaml
env:
  - name: DB_TYPE
    value: sqlite
  - name: DB_SQLITE_DATABASE
    value: /home/app/.n8n/database.sqlite
```

> ⚠️ Delete the app = delete the SQLite DB.

---

### ✅ Optional PostgreSQL (Lakehouse)

Switch to Lakebase by replacing in `app.yaml`:

```yaml
env:
  - name: DB_TYPE
    value: postgresdb
  - name: DB_POSTGRESDB_HOST
    value: <your-instance>.database.azuredatabricks.net
  - name: DB_POSTGRESDB_DATABASE
    value: databricks_postgres
  - name: DB_POSTGRESDB_USER
    value: your_user
  - name: DB_POSTGRESDB_PASSWORD
    value: your_password
  - name: DB_POSTGRESDB_PORT
    value: 5432
  - name: DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED
    value: 'false'
```

Then:
- Make sure schema `n8n` exists.
- Redeploy and test persistence across sessions.

---

## ✅ ClearTunnel Configuration (Optional)

No config needed — just include the `cleartunnel` binary in the `tunnel/` folder. `app.py` launches it automatically.

> You’ll see logs like:
> ```
> ClearTunnel listening on https://your-id.cleartunnel.io
> ```

Use that URL as your `WEBHOOK_URL` for Telegram or any other integration.

---

## 🧪 Memory Support in AI Agents

We’ve added a `session_id` transformer node that injects:

```js
return {
  ...$json,
  session_id: $json.message.chat.id.toString()
};
```

This ensures the **Agent AI** node keeps context using `Simple Memory`.

---

## 📦 package.json

```json
{
  "name": "n8n-with-databricks",
  "version": "1.0.0",
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

## 🧠 Author

- 👨‍💻 Built by [mexmarv@gmail.com](mailto:mexmarv@gmail.com)
- 🏗️ Based on [hellomikelo/databricks-n8n](https://github.com/hellomikelo/databricks-n8n)

---

## 📄 License

MIT License — as inherited from upstream.
