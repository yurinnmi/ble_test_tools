# iBeacon　テストツール

iBeaconの動作を確認するため、送信側を作成しました。

実機：M5Stack  

<br>

## [使い方]

M5 StackのボタンA（左側）を押すとiBeacon送信を開始します。
ボタンB（真ん中）を押すと、iBeacon送信を停止します。

iBeacon送信間隔（つまりAdvertisementパケット送信間隔）は、最大間隔500ms, 最小間隔200msです。<br>
Major ID=5, Minor ID=88<br>
iBeacon UUID=2D7A9F0C-E0E8-4CC9-A71B-A21DB2D034A1<br>
<br>

[カスタマイズ]<br>
送信間隔は、以下のコードで定義していますので、ソースコードで変更可能です。<br>
  pAdvertising->setMaxInterval(500);<br>
  pAdvertising->setMinInterval(200);<br>
同様、Major ID/Minor ID, UUID等も変更可能です。<br>
<br>
使用IDEはArduinoIDE 2です。<br>
ボード定義ファイル：<br>
　https://dl.espressif.com/dl/package_esp32_index.json<br>
　https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/arduino/package_m5stack_index.json

M5Unified 用ライブラリ：をインストールしてください。<br>
（ライブラリ名：M5Unified )

board名: M5Core　を選択してください。<br>

COMポート名はお使いの環境に合うよう変更してください。<br>


