# Node Script Runner 

k8s的環境下，建立一個Pod，能在Pod中藉由ssh連線的方式連接到node的上執行node特定路徑的Script(.sh)

## Project Structure

```
NodeScriptRunner/
├── _Node/                  #Node端的 script /yaml檔
│   ├── NodeScriptRunner-deployment.yaml        #Image apply yaml
│   ├── NodeScriptRunner-ServiceAccount.yaml    #Service Acccount apply yaml
│   └── Scripts/
│       └── nodeScript.sh       #Node端的script
├── _PodImage/              #Pod端的程式
│   ├── config.yaml             #py的config參數    
│   ├── Dockerfile          
│   ├── runscript.py            #python主檔 用來呼叫Pod端的script
│   └── scripts/
│       └── runner.sh           #Pod端的script  執行SSH登入Node執行Node端的script
├── README.md
```


## Getting Started

### Prerequisites


### Installation and Running

1. In _PodImage 

    a. modify runner.sh set current user accout , password and node script path
```
NODE_USER="vagrant"  #Node ssh login account name
NODE_PWD="vagrant"   #Node ssh login account password
SCRIPT_B="/home/vagrant/nodeScript.sh" #the script path in Node Server
```
    b.create Docker Image and push Image to Dockhub

```
docker build -t [DockhubUserName]/nodescriptrunner:v1.0 .
docker push [DockhubUserName]/nodescriptrunner:v1.0
```

2. In Node console

    a. copy script to Node 

    b. modify imagepath in deployment yaml 
```
      spec:
        hostPID: true
        hostNetwork: true
        serviceAccountName: k8s-node-script-runner
        containers:
        - name: nodescriptrunner
          image: [DockhubUserName]/nodescriptrunner:v1.0
```

    c. apply ServiceAccount and deployment
```
kubectl apply -f NodeScriptRunner-ServiceAccount.yaml 
kubectl apply -f NodeScriptRunner-deployment.yaml 
```

## License

This project is licensed under the MIT License.


