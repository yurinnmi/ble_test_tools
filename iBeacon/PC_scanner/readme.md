# 機能

- iBeacon をスキャン  
- スキャン時間は 60秒 (SCAN_SECONDSで定義）
- 新規検出ibeaconのUUID / Major / Minor / TxPower / RSSI を表示  
- 重複は表示しない。更新は表示する。  （PRINT_DUPLICATESで切り替え）
- CSV に追記保存
- スキャン時間終了、または、Ctrl+C で終了  

# 動作確認ホスト

　Windows11  
　BLE搭載

## 【WindowsPC】 BLE搭載かどうかを確認する方法

一般的には以下。

  1) デバイスマネージャーから、Bluetoothデバイスがあるはず  たとえば、インテル(R)ワイヤレスBluetooth(R)等があるはず
  2) プロパティの「詳細設定」を見る
  3) 「ファームウェアバージョン：　」の行で、LMPのバージョン番号が記載されている。LMPの先頭の数字が6以降ならBluetooth4.0以降なのでBLE搭載。

# 使い方

ビルドにはPython 3.12以上が必要。  
Python 3.12.3で確認済。  
Pythonのパッケージは仮想環境にインストールする。  

## python仮想環境

参照：
[pip と venv を使って仮想環境にパッケージをインストールする](https://packaging.python.org/ja/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

1) 仮想環境を作成( 初回のみ) 
```
py -m venv .venv
```
2) 仮想環境を活性化
```
.venv\Scripts\activate
```
3) ( 初回のみ) pipの準備をする
```
py -m pip install --upgrade pip
```

仮想環境を終了する場合：

1) 仮想環境を非活性化  
```
deactivate
```

## インストール

```
py -m pip install -r requirements.txt
```

NOTE：requirements.txt ：必要な依存先パッケージを列挙しているファイル


## 実行

```
py scan_ibeacon.py
```

## 実行結果

指定時間スキャンし、新しいiBeaconが見つかり次第表示するとともに、ログファイル(csv形式)にも記入する。

```
(.venv) C:\test>py scan_ibeacon.py
##################
iBeacon scan start
##################
CSV log: C:\test\ibeacon_log.csv
Scan duration: 60 sec
[NEW ] 10:09:44 ADDR=E4:B3:23:AD:26:EE RSSI= -67 UUID=E2C56DB5-DFFB-48D2-B060-D0F5A71096E0 MAJOR=1 MINOR=1 TX=-59
scan stopped
```
