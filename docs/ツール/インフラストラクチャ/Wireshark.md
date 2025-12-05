# Wireshark

## 概要

Wireshark は、世界で最も広く使用されているオープンソースのネットワークプロトコルアナライザーです。ネットワークトラフィックをリアルタイムでキャプチャし、パケットレベルで詳細に解析することができます。GUI ベースの直感的なインターフェースと強力なフィルタリング機能により、ネットワークトラブルシューティング、セキュリティ分析、プロトコル開発、教育に広く利用されています。

## 主な特徴

### 1. 深いパケット解析
- 2,000以上のプロトコルをサポート
- パケットの各レイヤーを詳細に表示
- プロトコルの自動検出
- 16進数とASCIIでの表示

### 2. ライブキャプチャとオフライン解析
- リアルタイムトラフィックキャプチャ
- pcap/pcapng ファイルの読み書き
- 複数のキャプチャファイルの結合
- 大容量ファイルの効率的な処理

### 3. 強力なフィルタリング
- キャプチャフィルタ（BPF構文）
- 表示フィルタ（Wireshark独自構文）
- 色分けルール
- マクロとショートカット

### 4. 統計とグラフ
- プロトコル階層統計
- 会話（Conversations）
- エンドポイント
- I/Oグラフ
- フロー図

### 5. クロスプラットフォーム
- Windows、macOS、Linux
- 統一されたGUI
- コマンドラインツール（tshark）
- リモートキャプチャ

## 主な機能

### キャプチャ機能

| 機能 | 説明 |
|------|------|
| インターフェース選択 | 有線・無線・仮想インターフェース |
| プロミスキャスモード | すべてのトラフィックをキャプチャ |
| キャプチャフィルタ | 特定のトラフィックのみキャプチャ |
| リングバッファ | 自動的に古いデータを削除 |
| マルチファイル | 時間/サイズで自動分割 |

### 解析機能

| 機能 | 説明 |
|------|------|
| プロトコルツリー | 階層的なプロトコル表示 |
| パケット詳細 | 各フィールドの詳細情報 |
| 16進数ダンプ | 生のパケットデータ |
| ストリーム再構築 | TCP/HTTP/TLS ストリームの復元 |
| エキスパート情報 | 問題の自動検出 |

### 統計機能

| 機能 | 説明 |
|------|------|
| プロトコル階層 | 使用されているプロトコルの割合 |
| 会話 | 通信している端末間の統計 |
| エンドポイント | 各ホストの統計 |
| I/Oグラフ | トラフィック量の時系列グラフ |
| フローグラフ | パケットの流れを視覚化 |

## インストールとセットアップ

### Windows

```powershell
# 公式サイトからダウンロード
# https://www.wireshark.org/download.html

# Chocolatey を使用
choco install wireshark

# インストール時の注意
# - Npcap (パケットキャプチャドライバ) をインストール
# - USBPcap (USB トラフィックキャプチャ) はオプション
```

### macOS

```bash
# 公式サイトからダウンロード
# https://www.wireshark.org/download.html

# Homebrew を使用
brew install --cask wireshark

# キャプチャ権限の設定が必要な場合
sudo chgrp admin /dev/bpf*
sudo chmod g+r /dev/bpf*
```

### Linux

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install wireshark

# ユーザーをwiresharkグループに追加（非rootでキャプチャ）
sudo usermod -aG wireshark $USER
# 再ログインが必要

# Fedora/RHEL/CentOS
sudo dnf install wireshark

# Arch Linux
sudo pacman -S wireshark-qt
```

## 基本的な使い方

### 1. インターフェースの選択

```
1. Wireshark を起動
2. キャプチャインターフェースの一覧が表示される
   - イーサネット（eth0, en0）
   - 無線LAN（wlan0, Wi-Fi）
   - ループバック（lo, Loopback）
   - 仮想インターフェース
3. キャプチャしたいインターフェースをダブルクリック
4. キャプチャが開始される
```

### 2. キャプチャフィルタ

```
# キャプチャ前にフィルタを設定（BPF構文）
# インターフェース横の入力欄に記述

# 特定ホストのトラフィック
host 192.168.1.100

# 特定ネットワーク
net 192.168.1.0/24

# 特定ポート
port 80
tcp port 443

# 送信元・宛先
src host 192.168.1.10
dst port 22

# プロトコル
tcp
udp
icmp

# 複合条件
host 192.168.1.100 and port 80
tcp port 443 or tcp port 8443
not arp
```

### 3. 表示フィルタ

```
# キャプチャ後にフィルタを適用（上部の入力欄）

# プロトコル
http
dns
ssh
tls

# IPアドレス
ip.addr == 192.168.1.100
ip.src == 10.0.0.1
ip.dst == 8.8.8.8

# ポート
tcp.port == 80
udp.port == 53

# HTTP
http.request.method == "GET"
http.response.code == 404
http.host contains "example.com"

# DNS
dns.qry.name == "www.example.com"

# TCP フラグ
tcp.flags.syn == 1
tcp.flags.reset == 1

# 複合条件
ip.addr == 192.168.1.100 and http
tcp.port == 443 and not tls.handshake
http.request or http.response

# 論理演算子
and (&&)
or (||)
not (!)
```

### 4. パケット詳細の表示

```
# パケットリストでパケットをクリック

下部のペインに表示される情報:
├── Frame (フレーム情報)
│   ├── インターフェース
│   ├── タイムスタンプ
│   └── フレーム長
├── Ethernet II (データリンク層)
│   ├── 送信元MACアドレス
│   └── 宛先MACアドレス
├── Internet Protocol (ネットワーク層)
│   ├── 送信元IPアドレス
│   ├── 宛先IPアドレス
│   └── TTL、プロトコル等
├── Transmission Control Protocol (トランスポート層)
│   ├── 送信元ポート
│   ├── 宛先ポート
│   ├── シーケンス番号
│   └── TCPフラグ
└── Hypertext Transfer Protocol (アプリケーション層)
    ├── リクエストメソッド
    ├── URI
    └── ヘッダー
```

### 5. ストリームの追跡

```
# TCP ストリームの再構築
1. TCPパケットを右クリック
2. 「Follow」→「TCP Stream」を選択
3. 通信全体が復元されて表示される
4. HTTP、TLS、SSH等のプロトコルに対応

# 例: HTTP 通信の全体像を確認
1. HTTP パケットを選択
2. Follow → HTTP Stream
3. リクエストとレスポンスの全体が表示される
```

## 高度な機能

### エキスパート情報

```
# Analyze → Expert Information

表示される情報:
- エラー (Errors): 深刻な問題
- 警告 (Warnings): 注意が必要
- ノート (Notes): 情報
- チャット (Chat): 通常の通信

例:
- TCP Retransmission（再送）
- TCP Previous segment not captured（パケットロス）
- TCP Window Full（ウィンドウ枯渇）
- HTTP response code 404
- DNS No response for query
```

### プロトコル階層統計

```
# Statistics → Protocol Hierarchy

表示される情報:
- キャプチャされたプロトコルの階層
- 各プロトコルの割合
- パケット数、バイト数

活用例:
- ネットワークの使用状況分析
- 異常なプロトコルの検出
- 帯域幅の消費分析
```

### 会話（Conversations）

```
# Statistics → Conversations

表示されるタブ:
- Ethernet: MAC アドレス間の通信
- IPv4/IPv6: IP アドレス間の通信
- TCP: TCP 接続
- UDP: UDP 通信

情報:
- 送受信パケット数
- 送受信バイト数
- 開始・終了時刻
- 通信時間
```

### I/Oグラフ

```
# Statistics → I/O Graph

機能:
- トラフィック量の時系列グラフ
- 複数のフィルタを同時に表示
- Y軸: パケット数/バイト数/ビット/秒
- X軸: 時間

活用例:
- トラフィックスパイクの検出
- 帯域幅の使用状況
- 異常な通信パターンの発見
```

### カラーリングルール

```
# View → Coloring Rules

デフォルトルール:
- 緑: HTTP
- 薄青: DNS
- 黒: TCP エラー
- 赤: TCP問題（再送等）

カスタムルール:
1. View → Coloring Rules
2. 「+」をクリック
3. 名前とフィルタを入力
4. 前景色・背景色を選択
5. 適用
```

### エクスポート機能

```
# File → Export Objects

サポートされるプロトコル:
- HTTP: Webページ、画像、ファイル
- DICOM: 医療画像
- SMB: Windows共有ファイル
- TFTP: TFTPファイル転送

# File → Export Packet Dissections
- テキスト
- CSV
- JSON
- XML
```

## コマンドライン（tshark）

### 基本的な使い方

```bash
# インターフェースの一覧
tshark -D

# キャプチャ
tshark -i eth0

# ファイルに保存
tshark -i eth0 -w capture.pcapng

# ファイルから読み込み
tshark -r capture.pcapng

# 表示フィルタ
tshark -r capture.pcapng -Y "http.request.method == GET"

# 特定フィールドのみ表示
tshark -r capture.pcapng -T fields -e ip.src -e ip.dst -e tcp.port

# 統計情報
tshark -r capture.pcapng -q -z io,phs  # プロトコル階層
tshark -r capture.pcapng -q -z conv,tcp  # TCP会話
```

### 自動化スクリプト

```bash
#!/bin/bash
# ネットワークトラフィック監視スクリプト

INTERFACE="eth0"
DURATION=60  # 秒
OUTPUT_DIR="./captures"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $OUTPUT_DIR

# キャプチャ実行
tshark -i $INTERFACE \
  -a duration:$DURATION \
  -w $OUTPUT_DIR/capture_$TIMESTAMP.pcapng

# 統計情報の生成
tshark -r $OUTPUT_DIR/capture_$TIMESTAMP.pcapng \
  -q -z io,phs > $OUTPUT_DIR/stats_$TIMESTAMP.txt

echo "Capture completed: $OUTPUT_DIR/capture_$TIMESTAMP.pcapng"
```

## ユースケース

### 1. HTTPトラフィックの解析

```
目的: Webアプリケーションのリクエスト/レスポンスを確認

手順:
1. キャプチャフィルタ: tcp port 80
2. ブラウザでWebサイトにアクセス
3. 表示フィルタ: http
4. HTTPリクエストを選択
5. Follow → HTTP Stream で全体を確認

確認項目:
- リクエストメソッド（GET/POST）
- URI
- ヘッダー（User-Agent, Cookie等）
- レスポンスコード
- レスポンスボディ
```

### 2. DNS問題のトラブルシューティング

```
目的: DNS解決の問題を特定

手順:
1. 表示フィルタ: dns
2. dns.flags.response == 0 でクエリのみ表示
3. dns.flags.response == 1 でレスポンスのみ表示

確認項目:
- クエリ名（dns.qry.name）
- レスポンスコード（dns.flags.rcode）
- 応答時間
- No such name (NXDOMAIN)
- タイムアウト
```

### 3. TCP接続の問題解析

```
目的: TCP接続の確立・切断を確認

表示フィルタ:
- tcp.flags.syn == 1 and tcp.flags.ack == 0  # SYN
- tcp.flags.syn == 1 and tcp.flags.ack == 1  # SYN-ACK
- tcp.flags.reset == 1  # RST
- tcp.flags.fin == 1  # FIN

確認項目:
- 3-way handshake の完了
- 接続のリセット
- 再送（tcp.analysis.retransmission）
- ウィンドウサイズ
```

### 4. TLS/SSL暗号化通信の解析

```
目的: TLS handshake の確認

表示フィルタ:
- tls.handshake
- tls.handshake.type == 1  # Client Hello
- tls.handshake.type == 2  # Server Hello

確認項目:
- TLS バージョン
- 暗号スイート
- 証明書
- Server Name Indication (SNI)

注意: 暗号化されたペイロードは復号化が必要
```

## セキュリティ分析

### 1. ポートスキャンの検出

```
表示フィルタ:
tcp.flags.syn == 1 and tcp.flags.ack == 0

確認:
- 短時間に多数のポートへの SYN パケット
- 同一送信元からの連続したポートへのアクセス
```

### 2. ARP スプーフィングの検出

```
表示フィルタ:
arp

確認:
- 同一IPアドレスに対する異なるMACアドレス
- ARP リプライの異常な頻度
```

### 3. 異常なトラフィックパターン

```
確認項目:
- 大量のICMP（Pingフラッド）
- 異常に大きなパケット
- 断片化されたパケット
- 未承認のプロトコル
```

## ベストプラクティス

### 1. キャプチャ設定

```
- 必要最小限のフィルタを使用
- リングバッファで容量制限
- 複数ファイルに分割
- タイムスタンプを有効化
```

### 2. プライバシーとセキュリティ

```
- 個人情報を含むキャプチャの取り扱いに注意
- キャプチャファイルの暗号化
- 不要なデータは即座に削除
- アクセス制限の設定
```

### 3. パフォーマンス

```
- キャプチャフィルタで事前に絞り込み
- 必要なインターフェースのみキャプチャ
- ディスクI/Oに注意
- 大容量ファイルは分割
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://www.wireshark.org/
- ユーザーズガイド: https://www.wireshark.org/docs/wsug_html_chunked/
- Wiki: https://wiki.wireshark.org/
- GitLab: https://gitlab.com/wireshark/wireshark

### コミュニティ
- Q&A: https://ask.wireshark.org/
- Mailing Lists: https://www.wireshark.org/lists/
- IRC: #wireshark on Libera.Chat

### トレーニング
- Wireshark University: オンラインコース
- 書籍: "Wireshark Network Analysis" by Laura Chappell
- YouTube: Wireshark チュートリアル

## まとめ

Wireshark は、以下の場面で特に有用です:

1. **ネットワークトラブルシューティング** - 接続問題、パフォーマンス問題の特定
2. **セキュリティ分析** - 不正アクセス、異常なトラフィックの検出
3. **プロトコル開発** - 新しいプロトコルの実装とデバッグ
4. **教育** - ネットワークプロトコルの学習

ネットワークの透明性を提供し、パケットレベルでの詳細な解析を可能にする強力なツールです。
