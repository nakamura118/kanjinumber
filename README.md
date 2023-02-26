# numbertokanji
アラビア数字を漢数字に，漢数字をアラビア数字に変換する．変換作業はFastAPIで行われる．
<br>
使用方法：<br>
FastAPIの基本的な使い方，環境構築はこちらからhttps://fastapi.tiangolo.com/ja/

numberchangeAPI.pyはFastAPIから作られている．
APIのエンドポイントは以下の通り
<br>
・アラビア数字から漢数字: /v1/number2kanji/{変換元のアラビア数字}<br>
・漢数字からアラビア数字︓/v1/kanji2number/{変換元の漢数字}<br>
