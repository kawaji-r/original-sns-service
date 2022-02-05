#! /bin/bash
# =================================================================
# 同階層のDockerfileを使用してイメージのbuild、コンテナの作成を実施
# =================================================================

# スクリプトファイルがあるパスに移動
pushd $(dirname $0)

# 変数定義
image_name=sns_database      # 作成するイメージの名前
container_name=sns_database  # 作成するコンテナの名前
network_name=sns_network     # ネットワーク名

# 対象のネットワークが未作成の場合はネットワークを作成する
network_flag=false
## 対象のネットワークがあるか確認
for i in $(docker network ls); do
    if [ "$i" = "sns_network" ]; then
        network_flag=true
    fi
done
## 無かったら作成
if [ "$network_flag" = "false" ]; then
    echo "Dockerネットワークを作成します"
    echo "docker network create ${network_name}"
    docker network create ${network_name}
fi

# Build
docker build --no-cache -t ${image_name} .
docker kill ${container_name} 2>/dev/null
docker rm ${container_name} 2>/dev/null

# Run
docker run -it -d \
    --name ${container_name} \
    --network ${network_name} \
    --restart=always \
    ${image_name}

# Finally
popd
