import os
import subprocess

class JSRunner:
    def __init__(self):
        self.node_version = "v22.2.0"
        self.node_dir = "/app/nodejs_download"
        self.node_url = f"https://nodejs.org/dist/{self.node_version}/node-{self.node_version}-linux-x64.tar.xz"
        self.binary_path = f"{self.node_dir}/bin/npx"
        self.env = os.environ.copy()
        self.env["PATH"] = f"{self.node_dir}/bin:" + self.env["PATH"]

    def prepare_node_dir(self):
        os.makedirs(self.node_dir, exist_ok=True)

    def download_node(self):
        self.prepare_node_dir()
        tar_path = f"{self.node_dir}/node.tar.xz"
        subprocess.run(["wget", self.node_url, "-O", tar_path], check=True)
        subprocess.run(["tar", "-xJf", tar_path, "-C", self.node_dir, "--strip-components=1"], check=True)

    def install_deps(self):
        subprocess.run([self.binary_path, "npm", "install"], env=self.env, check=True)

    def run_n8n(self):
        subprocess.run([self.binary_path, "npx", "n8n"], env=self.env, check=True)

    def run(self):
        self.download_node()
        self.install_deps()
        self.run_n8n()

if __name__ == "__main__":
    runner = JSRunner()
    runner.run()
