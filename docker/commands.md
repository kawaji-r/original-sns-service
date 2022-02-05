## 手順
* 以下の各コマンドを実行
* `curl localhost` で500エラーが出ないことを確認して構築完了

## ソースコード取得
### gitをインストール
```
sudo apt install -y git
```

### 秘密鍵を配置
* ~/.ssh/id_rsa

### リポジトリをクローン
```
git clone --recursive ssh://git@github.com/kawaji-r/original-sns-service.git
```

### 必要なもののみ残す
```
cd src
git config core.sparsecheckout true
echo src >> .git/info/sparse-checkout
echo docker >> .git/info/sparse-checkout
echo requirements.txt >> .git/info/sparse-checkout
git read-tree -m -u HEAD
```

## Dockerをインストール
```
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo docker run hello-world  # 動作確認
sudo usermod -aG docker ubuntu  # sudo不要で実行可能に
```

## Dockerコンテナ作成
```
cd original-sns-service/docker
bash 1_database/build.sh
bash 2_app/build.sh
docker ps  # 確認
```
