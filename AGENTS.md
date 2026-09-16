# MusicTool の運用ルール

- `M_get`はPATH上のyt-dlpを優先せず、Music専用のuv環境と`uv.lock`にあるyt-dlpを使用する。古いシステム版でYouTubeの403エラーが再発する状態を防ぐ。
- yt-dlpの更新は `uv lock --upgrade-package yt-dlp --upgrade-package yt-dlp-ejs` と `uv sync` で行い、`./M_get --check` で実際のバージョンを確認する。
- Cookie不使用を維持し、個人のyt-dlp設定による旧クライアント指定を避けるため `--ignore-config` を使用する。
- `README_ja.md` は `.git/info/exclude` に登録し、コミットしない。

- `M_get`の通常取得はSpotify標準の-14 LUFS・True Peak目標-1 dBTPへの音量調整を既定とする。無効化は明示的な`--no-normalize`で行う。圧縮形式への再エンコードでは品質とサンプルレートを明示する。
- 日常の音楽鑑賞を目的とし、`M_get`は`M_norm`同様に入力測定1回と音量調整1回の2パス処理を行う（LRA目標11 LU）。変換後の再測定・微小な数値差による保存拒否・再生成ループは追加しない。

- `M_norm --output-dir`では原本を変更せず相対パスを維持して別フォルダへ出力する。目標付近の入力もコピーして出力漏れを防ぐ。既存出力は既定でスキップし、上書きは`--overwrite`で指定する。入力・出力ツリーの重複を拒否し、一時出力が完成してから公開する。
