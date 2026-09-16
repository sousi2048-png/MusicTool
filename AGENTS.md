# MusicTool の運用ルール

- `M_get`はPATH上のyt-dlpを優先せず、Music専用のuv環境と`uv.lock`にあるyt-dlpを使用する。古いシステム版でYouTubeの403エラーが再発する状態を防ぐ。
- yt-dlpの更新は `uv lock --upgrade-package yt-dlp --upgrade-package yt-dlp-ejs` と `uv sync` で行い、`./M_get --check` で実際のバージョンを確認する。
- Cookie不使用を維持し、個人のyt-dlp設定による旧クライアント指定を避けるため `--ignore-config` を使用する。
- `README_ja.md` は `.git/info/exclude` に登録し、コミットしない。

- `M_get`の通常取得はSpotify標準の-14 LUFS・True Peak目標-1 dBTPへの音量調整を既定とする。無効化は明示的な`--no-normalize`で行う。圧縮形式への再エンコードでは品質とサンプルレートを明示し、変更時は保存後の音声を再測定する。
- 非可逆圧縮後にTrue Peakが上昇するため、保存前の再測定を必須とし、超過時は元の取得音声から再生成する。再圧縮済みの音声を繰り返し加工しない。
