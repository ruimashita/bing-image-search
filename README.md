# 概要

Bing Search API で画像をダウンロードする。

# 使い方

1. MSとBing Search APIの登録
http://o-tomox.hatenablog.com/entry/2013/09/25/191506
を参考にして、
MSのアカウント作成・Bing Search APIの登録をおこなう。
アカウントキーをメモっておく。

2. `search_bing.py` を編集

* `MS_KEY` にメモっておいたアカウントキー。
* `KEYWORD` をダウンロードしたい画像のカテゴリにする。
* `END` (取得件数) を適当に変更する。


3. ダウンロードの実行

```
$ python search_bing.py
```

