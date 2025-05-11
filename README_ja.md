# minecraft_remote_samples / Naohiro2g

Minecraft Remote（マイクラリモコン）のAPIを使いPythonでユーザーコードを書く出発点
***
このドキュメントは、Reveal.jsに対応しています。

--

## このリポジトリの内容

Python環境をゼロから構築、コードを書いてマイクラ世界に自動建築するまでのガイド。Pythonがすでに動いている人は最短距離で。

Python入門、Python開発入門として利用可能。

--

### README（このファイル）
  - マイクラリモコンの概要
  - 箱庭サーバーの利用方法
  - Python環境準備とデモコードの実行
  - Jupyter環境の準備

--

### Jupyter Notebookファイル
  - demo_00_ja.ipynb
    - マイクラリモコン入門
  - demo_01_ja.ipynb
    - 「マイクラ課題」演習

---

PythonコーディングでMinecraft世界に自動建築ができます。
[Minecraft Remote（`McRemote`）プラグイン](https://github.com/Naohiro2g/McRemote)をインストールした[PaperMC](https://papermc.io/)サーバーが必要です。

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/mc-remote.png" width="320" alt="Minecraft Remote World" title="Minecraft Remote World" />

ご心配なく。箱庭（サンドボックス）サーバーを利用して、今すぐ、始められます。

---

## 箱庭サーバーに参加してみよう

同じ仕様で家庭、教室などに自分のサーバーを準備すると、より楽しい体験ができるかも。でも、まずは、試してみないとね。

このサーバーは、割と短期間で初期化するので、ちょっとぐらい失敗しても許されます。

--

### マインクラフト サーバー情報

名称：「箱庭（サンドボックス）サーバー」

- アドレス
  - `mc-remote.xgames.jp`
- ポート
  - Java版　`25565` （指定不要）
  - Bedrock版　`25565` （指定する）

「ほとんど、どんなクライアントもつながる」仕様

--

### クライアント アプリ（マルチモード）

「ほとんど、何でもつながる」はず

- Java / Fabric / NeoForge / Forge 1.8.8〜最新
- 統合版（iOS / Android / Windowsを含む）
- 推奨セットアップは影mod入りJava版:

    [`Iris`](https://irisshaders.github.io/) / Fabric と [`MakeUp - Ultra Fast`](https://modrinth.com/shader/makeup-ultra-fast-shaders/changelog?l=iris) シェーダー

---

## 非常に重要な準備作業

`param_mc_remote.py`のパラメータを編集します。

```python
PLAYER_NAME = "PLAYER_NAME"  # set your player name in Minecraft

PLAYER_ORIGIN = Vec3(2000, 0, 2000)  # PO.x, PO.y, PO.z

ADRS_MCR = "mc-remote.xgames.jp"  # mc-remote sandbox server
PORT_MCR = 25575  # socket server port
```

**APIを利用時に、PLAYER_NAME と同じ名前でMinecraftサーバーに参加していること。**

箱庭サーバーを使うならPLAYER_NAMEだけ変更。

--

### `PLAYER_ORIGIN` は建築座標系の原点

`PLAYER_ORIGIN` からの相対座標で、ブロックが配置されます。
たとえば、

- `PLAYER_ORIGIN`： `(2000, 0, 2000)`
- コマンド： `setBlock(5, 68, 5, block.GOLD_BLOCK)`

⇒ 結果： `(2005, 68, 2005)` に金ブロック出現

--

### 自前のサーバーを準備する場合

これらのパラメータを設定してください。


- **`ADRS_MCR`**：
  マイクラリモコンサーバーのアドレスで、マインクラフトサーバーと同じです。自分のPCなら、`"localhost"`
- **`PORT_MCR`**：
　マイクラリモコンサーバーのポート番号です。デフォルト値は `25575` ですが、`plugins/McRemote/config.yml` で変更できます。

---

## Discordコミュニティ

Discordコミュニティでは、不明点を質問したり、他のユーザーと経験を共有できます。

箱庭サーバーやAPIの使い方、サーバーの建て方などについて質問がある場合は、[Discordサーバー](https://discord.gg/xUqhhqWsuS)内の `mc-remote-chat` チャンネルをご利用ください。

---

## 環境の準備と更新

--

- とにかく試したい人向けの最短手順
- Python環境を最初から構築する手順
  - Python 3.10から3.12
  - pyenvによるPythonインストール
  - poetryによるプロジェクト内への仮想環境生成
- クライアント / APIを準備
  - [minecraft-remote-api @ Pypi.org](https://pypi.org/project/minecraft-remote-api/)

--

#### Pythonだけで勝負！の場合

このリポジトリのクローンさえ不要、PLAYER_NAMEを自分のプレイヤー名に書き換えるだけ。Thonnyなんかもいいね。mu-editorは、Python 3.8で止まっているので無理。

```bash
# パッケージをインストール／更新
pip install minecraft-remote-api -U

# ファイルに保存するか、REPLモードで
import mc_remote.minecraft import Minecraft
mc = Minecraft.create("mc-remote.xgames.jp", 25575)
mc.setPlayer("PLAYER_NAME", 2000, 0, 2000)
mc.postToChat("Hello, hello!")
mc.setBlock(5, 68, 5, "gold_block")
```

--

#### とくかく、試したいのだ、という場合

Python 3.10から3.12があるなら、以下の要領で。

```bash
# パッケージをインストール／更新
pip install minecraft-remote-api -U

# examples/param_mc_remote.pyを編集して、自分のプレイヤー名に変更。
# PLAYER_NAME = "PLAYER_NAME"

# hello, world!
cd examples
python hello.py
```

--

### 推奨するPython環境構築

- pyenvをインストール
- pyenvでPythonをインストール
- poetryをインストール

---


--

Pythonパッケージの最新版は [PyPI](https://pypi.org/project/minecraft-remote-api/) からインストールできます。

#### pyenv / poetryがインストールされている場合

```bash
poetry install


# 仮想環境(.venv/)が作成されたのを確認し、今後は、その環境内で作業してください。
```

パッケージを更新するには、次のコマンドを実行:

```bash
poetry update
```

--

#### pyenv / poetryがインストールされていない場合

Python 3.9以上がインストールされていることを確認して、次のコマンドを実行:

```bash
pyenv local 3.11.9  # もし、pyenvをインストール済みなら
pip install minecraft-remote-api
```

（現在は、Python 3.11.9, 3.12.10が推奨です。）

パッケージを更新するには、次のコマンドを実行:

```bash
pip install minecraft-remote-api -U
```

パッケージ管理のためにpyenv / poetryを使うことをオススメします。少なくとも、pyenvを使うとPythonのバージョン管理が楽になります。

pyenv / poetryのインストール方法は、[こちら](https://github.com/Naohiro2g/minecraft-remote-api/docs/pyenv_and_poetry_ja.md)を参照してください。

---

## サンプルを実行

```bash
cd examples
python hello.py
python axis_flat.py
```

---

## Minecraft Remoteプロジェクトについて

詳しくは、[ミッション](docs/mission_ja.md) ドキュメントを参照してください。

--

「hacking, coding, tinkering = ハッキング、コーディング、ティンカリング」が、このプロジェクトの核です。私たちはユーザーが自らの経験を通じて探求し学ぶことができるシステムを作成することを目指しています。このプロジェクトでは、私たちのビジョンを共有するすべての人からの貢献を歓迎します。

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/hacking_coding_tinkering.png" width="480" alt="Hacking Coding Tinkering" title="Hacking Coding Tinkering" />
