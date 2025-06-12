from kubernetes import client, config
import subprocess
import os
import time
import yaml


def run_pod_script(_SCRIPT_PATH):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    node_ip = os.getenv("NODE_IP")  #node_ip: when applying yaml, k8s write it's value in pod's env.
    p1="Para1"
    try:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Run Script: {_SCRIPT_PATH}")
        subprocess.call(["/bin/bash", _SCRIPT_PATH, node_ip])
    except Exception as e:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 發生錯誤: {e}")


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    config_data = load_config()
    SCRIPT_PATH = config_data.get("script_path", "scripts/runner.sh")
    if not os.path.exists(SCRIPT_PATH):
        print(f"找不到 {SCRIPT_PATH}，請確認腳本路徑正確。")
    else:
        print(f"已找到 {SCRIPT_PATH}。")        
        run_pod_script(SCRIPT_PATH)
