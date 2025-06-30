# Milvus on Podman

## Docker $\to$ Podman

**Mitanshu Sukhwani** • _07 June 2025_

# Original:

1. Download from:

   ```bash
   curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

   bash standalone_embed.sh start
   ```

2. See contents using:

   `cat standalone_embed.sh`

3. Output:

   ```bash
   #!/usr/bin/env bash

   # Licensed to the LF AI & Data foundation under one
   # or more contributor license agreements. See the NOTICE file
   # distributed with this work for additional information
   # regarding copyright ownership. The ASF licenses this file
   # to you under the Apache License, Version 2.0 (the
   # "License"); you may not use this file except in compliance
   # with the License. You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.

   run_embed() {
       cat << EOF > embedEtcd.yaml
   listen-client-urls: http://0.0.0.0:2379
   advertise-client-urls: http://0.0.0.0:2379
   quota-backend-bytes: 4294967296
   auto-compaction-mode: revision
   auto-compaction-retention: '1000'
   EOF

       cat << EOF > user.yaml
   # Extra config to override default milvus.yaml
   EOF

       sudo docker run -d \
           --name milvus-standalone \
           --security-opt seccomp:unconfined \
           -e ETCD_USE_EMBED=true \
           -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
           -e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml \
           -e COMMON_STORAGETYPE=local \
           -v $(pwd)/volumes/milvus:/var/lib/milvus \
           -v $(pwd)/embedEtcd.yaml:/milvus/configs/embedEtcd.yaml \
           -v $(pwd)/user.yaml:/milvus/configs/user.yaml \
           -p 19530:19530 \
           -p 9091:9091 \
           -p 2379:2379 \
           --health-cmd="curl -f http://localhost:9091/healthz" \
           --health-interval=30s \
           --health-start-period=90s \
           --health-timeout=20s \
           --health-retries=3 \
           milvusdb/milvus:v2.4.5 \
           milvus run standalone  1> /dev/null
   }

   wait_for_milvus_running() {
       echo "Wait for Milvus Starting..."
       while true
       do
           res=`sudo docker ps|grep milvus-standalone|grep healthy|wc -l`
           if [ $res -eq 1 ]
           then
               echo "Start successfully."
               echo "To change the default Milvus configuration, add your settings to the user.yaml file and then restart the service."
               break
           fi
           sleep 1
       done
   }

   start() {
       res=`sudo docker ps|grep milvus-standalone|grep healthy|wc -l`
       if [ $res -eq 1 ]
       then
           echo "Milvus is running."
           exit 0
       fi

       res=`sudo docker ps -a|grep milvus-standalone|wc -l`
       if [ $res -eq 1 ]
       then
           sudo docker start milvus-standalone 1> /dev/null
       else
           run_embed
       fi

       if [ $? -ne 0 ]
       then
           echo "Start failed."
           exit 1
       fi

       wait_for_milvus_running
   }

   stop() {
       sudo docker stop milvus-standalone 1> /dev/null

       if [ $? -ne 0 ]
       then
           echo "Stop failed."
           exit 1
       fi
       echo "Stop successfully."

   }

   delete() {
       res=`sudo docker ps|grep milvus-standalone|wc -l`
       if [ $res -eq 1 ]
       then
           echo "Please stop Milvus service before delete."
           exit 1
       fi
       sudo docker rm milvus-standalone 1> /dev/null
       if [ $? -ne 0 ]
       then
           echo "Delete failed."
           exit 1
       fi
       sudo rm -rf $(pwd)/volumes
       sudo rm -rf $(pwd)/embedEtcd.yaml
       sudo rm -rf $(pwd)/user.yaml
       echo "Delete successfully."
   }


   case $1 in
       restart)
           stop
           start
           ;;
       start)
           start
           ;;
       stop)
           stop
           ;;
       delete)
           delete
           ;;
       *)
           echo "please use bash standalone_embed.sh restart|start|stop|delete"
           ;;
   esac
   ```

# Modified:

1. remove sudo for use with podman rootless

2. add `:Z` in the end of mapped volumes for SELinux Context Handling

3. Add `docker.io` infront of `milvusdb/milvus` for name resolution

   ```bash
   #!/usr/bin/env bash

   # Licensed to the LF AI & Data foundation under one
   # or more contributor license agreements. See the NOTICE file
   # distributed with this work for additional information
   # regarding copyright ownership. The ASF licenses this file
   # to you under the Apache License, Version 2.0 (the
   # "License"); you may not use this file except in compliance
   # with the License. You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.

   run_embed() {
       cat << EOF > embedEtcd.yaml
   listen-client-urls: http://0.0.0.0:2379
   advertise-client-urls: http://0.0.0.0:2379
   quota-backend-bytes: 4294967296
   auto-compaction-mode: revision
   auto-compaction-retention: '1000'
   EOF

       cat << EOF > user.yaml
   # Extra config to override default milvus.yaml
   EOF

       docker run -d \
           --name milvus-standalone \
           --security-opt seccomp:unconfined \
           -e ETCD_USE_EMBED=true \
           -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
           -e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml \
           -e COMMON_STORAGETYPE=local \
           -v $(pwd)/volumes/milvus:/var/lib/milvus:Z \
           -v $(pwd)/embedEtcd.yaml:/milvus/configs/embedEtcd.yaml:Z \
           -v $(pwd)/user.yaml:/milvus/configs/user.yaml:Z \
           -p 19530:19530 \
           -p 9091:9091 \
           -p 2379:2379 \
           --health-cmd="curl -f http://localhost:9091/healthz" \
           --health-interval=30s \
           --health-start-period=90s \
           --health-timeout=20s \
           --health-retries=3 \
           docker.io/milvusdb/milvus:v2.4.5 \
           milvus run standalone  1> /dev/null
   }

   wait_for_milvus_running() {
       echo "Wait for Milvus Starting..."
       while true
       do
           res=` docker ps|grep milvus-standalone|grep healthy|wc -l`
           if [ $res -eq 1 ]
           then
               echo "Start successfully."
               echo "To change the default Milvus configuration, add your settings to the user.yaml file and then restart the service."
               break
           fi
           sleep 1
       done
   }

   start() {
       res=` docker ps|grep milvus-standalone|grep healthy|wc -l`
       if [ $res -eq 1 ]
       then
           echo "Milvus is running."
           exit 0
       fi

       res=` docker ps -a|grep milvus-standalone|wc -l`
       if [ $res -eq 1 ]
       then
           docker start milvus-standalone 1> /dev/null
       else
           run_embed
       fi

       if [ $? -ne 0 ]
       then
           echo "Start failed."
           exit 1
       fi

       wait_for_milvus_running
   }

   stop() {
       docker stop milvus-standalone 1> /dev/null

       if [ $? -ne 0 ]
       then
           echo "Stop failed."
           exit 1
       fi
       echo "Stop successfully."

   }

   delete() {
       res=` docker ps|grep milvus-standalone|wc -l`
       if [ $res -eq 1 ]
       then
           echo "Please stop Milvus service before delete."
           exit 1
       fi
       docker rm milvus-standalone 1> /dev/null
       if [ $? -ne 0 ]
       then
           echo "Delete failed."
           exit 1
       fi
       rm -rf $(pwd)/volumes
       rm -rf $(pwd)/embedEtcd.yaml
       rm -rf $(pwd)/user.yaml
       echo "Delete successfully."
   }


   case $1 in
       restart)
           stop
           start
           ;;
       start)
           start
           ;;
       stop)
           stop
           ;;
       delete)
           delete
           ;;
       *)
           echo "please use bash standalone_embed.sh restart|start|stop|delete"
           ;;
   esac
   ```
