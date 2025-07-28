import subprocess
import os
import time
import re
import requests

class JSRunner:
    def __init__(self):
        self.node_version = "v22.2.0"
        self.node_dir = "/tmp/nodejs_download"
        self.npx_path = os.path.join(self.node_dir, "bin", "npx")
        self.npm_path = os.path.join(self.node_dir, "bin", "npm")
        self.env = os.environ.copy()
        self.env["PATH"] = f"{self.node_dir}/bin:" + self.env.get("PATH", "")
        self.env.setdefault("N8N_PORT", "8000")
        self.env.setdefault("N8N_DB_TYPE", "sqlite")
        self.env.setdefault("N8N_DB_SQLITE_DATABASE", "/app/data/database.sqlite")

    def prepare_node_dir(self):
        os.makedirs(self.node_dir, exist_ok=True)

    def download_node(self):
        if not os.path.exists(os.path.join(self.node_dir, "bin", "node")):
            self.prepare_node_dir()
            print(f"⬇️ Downloading Node.js {self.node_version}")
            url = f"https://nodejs.org/dist/{self.node_version}/node-{self.node_version}-linux-x64.tar.xz"
            subprocess.run(["wget", url], check=True)
            print(f"📦 Extracting Node.js")
            subprocess.run([
                "tar", "--strip-components", "1", "-xf",
                f"node-{self.node_version}-linux-x64.tar.xz", "-C", self.node_dir
            ], check=True)

    def install_deps(self):
        print("📦 Installing dependencies from package.json...")
        subprocess.run([self.npm_path, "install"], env=self.env, check=True)

    def download_cloudflared(self):
        if not os.path.exists("/tmp/cloudflared"):
            print("⬇️ Downloading cloudflared...")
            subprocess.run([
                "wget", "-O", "/tmp/cloudflared",
                "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
            ], check=True)
            subprocess.run(["chmod", "+x", "/tmp/cloudflared"], check=True)

    def start_cloudflared(self):
        print("🚀 Starting Cloudflare Tunnel on port 8000...")
        proc = subprocess.Popen(
            ["/tmp/cloudflared", "tunnel", "--url", "http://localhost:8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            text=True
        )

        public_url = None
        for _ in range(30):
            line = proc.stdout.readline()
            if "trycloudflare.com" in line:
                print("🌐", line.strip())
                match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
                if match:
                    public_url = match.group(0)
                    break
            time.sleep(1)

        if not public_url:
            raise Exception("❌ Failed to detect cloudflared public URL")

        self.env["WEBHOOK_URL"] = public_url
        with open("/tmp/webhook_url.txt", "w") as f:
            f.write(public_url)
        print(f"✅ WEBHOOK_URL set to: {public_url}")

    def delete_config_if_exists(self):
        config_path = "/home/app/.n8n/config"
        if os.path.exists(config_path):
            print("🗑️ Deleting old config file to avoid encryption key mismatch")
            os.remove(config_path)

    def fix_config_permissions(self):
        config_dir = "/home/app/.n8n"
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "config")
        if os.path.exists(config_file):
            os.chmod(config_file, 0o600)

    def run(self):
        self.download_node()
        self.download_cloudflared()
        self.start_cloudflared()
        self.install_deps()
        self.delete_config_if_exists()
        self.fix_config_permissions()
        print("▶️ Running: npx n8n with webhook:", self.env.get("WEBHOOK_URL"))
        subprocess.run([self.npx_path, "n8n"], env=self.env, check=True)

if __name__ == "__main__":
    runner = JSRunner()
    runner.run()
