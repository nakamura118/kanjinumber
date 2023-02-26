# numbertokanji
アラビア数字を漢数字に，漢数字をアラビア数字に変換する．変換作業はFastAPIで行われる．
<br>
numberchangeAPI.pyはFastAPIから作られている．<br>
使用方法：<br>
FastAPIの基本的な使い方，環境構築の詳細はこちらからhttps://fastapi.tiangolo.com/ja/
・APIの起動方法<br>
APIプログラムダウンロード<br>
pythonが入っている状況でターミナルで以下を実行<br>
$ pip install fastapi<br>
$ pip install "uvicorn[standard]"<br>
$ uvicorn (APIのファイル名):app --reload --host (IPアドレス) --port (ポート番号)<br>
<br>

APIのエンドポイントは以下の通り
<br>
・アラビア数字から漢数字: /v1/number2kanji/{変換元のアラビア数字}<br>
・漢数字からアラビア数字︓/v1/kanji2number/{変換元の漢数字}<br>
APIはhtml側から上記のように呼び出されることを想定している．

