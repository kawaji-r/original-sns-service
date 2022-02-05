#! /bin/bash
# =================================================================
# 同階層のDockerfileを使用してイメージのbuild、コンテナの作成を実施
# =================================================================

# スクリプトファイルがあるパスに移動
pushd $(dirname $0)

# 変数定義
image_name=sns_app        # 作成するイメージの名前
container_name=sns_app    # 作成するコンテナの名前
network_name=sns_network  # ネットワーク名

# Build
cp -p ../../requirements.txt ./ # Dockerfileよりも上の階層のファイルを扱えないため
docker build -t ${image_name} .
docker kill ${container_name} 2>/dev/null
docker rm ${container_name} 2>/dev/null

# Run
## コンテナの80番ポートをローカルの80番ポートにフォワード
docker run -it -d \
    -p 80:80 \
    --name ${container_name} \
    --mount type=bind,source="$(cd ${PWD}/../../src; pwd)",target=/root/src \
    --network ${network_name} \
    --restart=always \
    ${image_name}

# Finally
popd
