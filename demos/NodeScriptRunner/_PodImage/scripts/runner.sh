#!/bin/sh
NODE_IP=$1
echo "$(date): node: [$NODE_IP] run script"
set -eu


NODE_USER="UserName"  #Node ssh login account name
NODE_PWD="Password"
SCRIPT_B="/home/UserName/nodeScript.sh" #the script path in Node Server

echo "$(date): NODE_IP [$NODE_IP] "

# exec Script B on node；StrictHostKeyChecking=no for first connection
sshpass -p "${NODE_PWD}" \
    ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "${NODE_USER}@${NODE_IP}" \
        "bash -c '$SCRIPT_B $NODE_IP'"