#!/usr/bin/env bash
set -ex

stack=$1
container_id=$2
n_cores=$3
memory=$4 # In Gigabytes
container_name=$5

image_name="virtuoso"
socket_path_base="/local/liam/"

if [[ "$stack" == 'container-linux' ]]; then
    sudo docker run --net=none --name $container_name \
    --memory=${memory}g \
    --cpuset-cpus 22,24,26,28,30,32,34,36,38,40,42 \
    --cpus=${n_cores} \
    -d $image_name sleep infinity;
elif [[ "$stack" == 'container-tas' ]]; then
    sudo docker run --net=none --name $container_name \
    -v ${socket_path_base}/flexnic_os:/home/tas/flexnic_os \
    -v /dev/hugepages:/dev/hugepages \
    -v /dev/shm:/dev/shm \
    --memory=${memory}g \
    --cpuset-cpus 22,24,26,28,30,32,34,36,38,40,42 \
    --cpus=${n_cores} \
    -d $image_name sleep infinity;
elif [[ "$stack" == 'container-virtuoso' ]]; 
then
    sudo docker run --net=none --name $container_name \
    -v ${socket_path_base}/flexnic_os_vm_${container_id}:/home/tas/flexnic_os_vm_${container_id} \
    -v /dev/hugepages:/dev/hugepages \
    -v /dev/shm:/dev/shm \
    --memory=${memory}g \
    --cpuset-cpus 22,24,26,28,30,32,34,36,38,40,42 \
    --cpus=${n_cores} \
    -d $image_name sleep infinity;
fi