## RKE2
   [https://docs.rke2.io/zh/](https://docs.rke2.io/zh/)

RKE2，也称为 RKE Government，是 Rancher 的下一代 Kubernetes 发行版。
它是一个完全合规的 Kubernetes 发行版，专注于安全和合规性。

RKE是一款经过CNCF认证、极致简单易用且闪电般快速的Kubernetes安装程序，完全在容器内运行，解决了容器最常见的安装复杂性问题。借助RKE，Kubernetes可以完全独立于您正在运行的操作系统和平台，轻松实现Kubernetes的自动化运维。仅需几分钟，RKE便可通过单条命令构建一个集群，其声明式配置使Kubernetes升级操作具备原子性且安全。



以rke2安裝 可以快速部署完成k8s cluster
https://docs.rke2.io/
## 首先安裝master node

```
#1. Run the installer
#This will install the rke2-server service and the rke2 binary onto your machine. Due to its nature, It will fail unless it runs as the root user or through sudo.
curl -sfL https://get.rke2.io | sh -


#2. Enable the rke2-server service
systemctl enable rke2-server.service

#3. Start the service
systemctl start rke2-server.service
```

照步驟安裝完後
要做以下的設定

```
#create link to kubectl
ln -sf /var/lib/rancher/rke2/bin/kubectl /usr/bin/ 

#Create .kube folder
mkdir -p /root/.kube/

#Copy kube cluster context config to /root/.kube/
cp /etc/rancher/rke2/rke2.yaml /root/.kube/config
```
這樣才能把kubectl串起來

## 加入worker node

先記下 master(server)的token位置

A token that can be used to register other server or agent nodes will be created at /var/lib/rancher/rke2/server/node-token


Linux Agent (Worker) Node Installation
The steps on this section requires root level access or sudo to work.

```
#1. Run the installer
#This will install the rke2-agent service and the rke2 binary onto your machine. Due to its nature, It will fail unless it runs as the root user or through sudo.
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="agent" sh -

#2. Enable the rke2-agent service
systemctl enable rke2-agent.service

#3. Configure the rke2-agent service
mkdir -p /etc/rancher/rke2/
vim /etc/rancher/rke2/config.yaml

#Content for config.yaml:
#-------------------------------------
#server: https://<server>:9345
#token: <token from server node>
#-------------------------------------

#4. Start the service
systemctl start rke2-agent.service

```



## 加入another master node

要在多個 Master 節點上安裝與設定 RKE2（Rancher Kubernetes Engine 2）來建立一個高可用的 Kubernetes Cluster，你可以參考以下步驟概要，並搭配詳細教學資源：

### 🧭 基本架構規劃
假設你要建立一個 3 Master + N Worker 的高可用叢集，以下是基本需求：

作業系統：建議使用 Ubuntu 20.04+ 或 Debian 11/12
每個節點：
CPU：2 核以上
RAM：4GB 以上
關閉 swap：swapoff -a && sed -i '/swap/d' /etc/fstab
網路設定：
所有節點之間需能互通
設定 /etc/hosts 或 DNS 解析

### 🛠️ 安裝步驟概要
1. 所有節點前置作業

```
apt update && apt install -y curl apparmor
swapoff -a && sed -i '/swap/d' /etc/fstab
```

2. 安裝第一個 Master 節點（master01）
```
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=server sh -
systemctl enable rke2-server && systemctl start rke2-server
```

查看 token（供其他節點加入使用）：
```
cat /var/lib/rancher/rke2/server/node-token
```

設定 kubeconfig：
```
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
```

3. 安裝其他 Master 節點（master02, master03）

安裝master rke2
```
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=server sh -
```


建立 /etc/rancher/rke2/config.yaml：

```
server: https://<master01-ip>:9345
token: <從 master01 取得的 token>
tls-san:
  - VIP 
  - master01-ip
  - master02-ip
  - master03-ip
node-name: "master02 node name"
node-label:
  - "node=Master"

```

啟動Service：

```
systemctl enable rke2-server && systemctl start rke2-server
```


4. 安裝 Worker 節點
設定 /etc/rancher/rke2/config.yaml：
```
server: https://<master01-ip>:9345
token: <從 master01 取得的 token>
node-name: node01
```

安裝並啟動：
```
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=agent sh -
systemctl enable rke2-agent && systemctl start rke2-agent
```


📚 詳細教學資源
📖 CSDN 詳細圖文教學（含 config.yaml 範例與離線安裝）： Debian12 使用 RKE2 建立 3 Master 2 Node 教學 1

🎥 YouTube 視頻教學（英文）： Quick and Easy RKE2 Kubernetes Cluster Installation 2

📘 官方文件： RKE2 Quick Start Guide 3


### 如果要重新加入被刪除的node 但一直出錯的話可以考慮依照以下的作法處理


##### 1.確認其他 Master 節點仍正常運作
從現存的 master 節點取得 token：
```
cat /var/lib/rancher/rke2/server/node-token
```

##### 2.在被刪除的節點上清除殘留資料
```
sudo /usr/local/bin/rke2-uninstall.sh
sudo rm -rf /etc/rancher /var/lib/rancher /var/lib/kubelet /var/lib/etcd
```

##### 3.確認沒有殘留的服務佔用 9345 port
```
ss -lntp | grep 9345
```

##### 4.重新建立 config.yaml
重建 /etc/rancher/rke2/config.yaml：

```
server: https://<master01-ip>:9345
token: <從 master01 取得的 token>
tls-san:
  - VIP 
  - master01-ip
  - master02-ip
  - master03-ip
node-name: "master02 node name"
node-taint:
  - "CriticalAddonsOnly=true:NoExecute"
node-label:
  - "node=Master"

```

##### 5.重新安裝並啟動 RKE2 server

```
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE=server sh -
systemctl enable rke2-server && systemctl start rke2-server
```

