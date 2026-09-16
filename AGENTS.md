# MusicTool の運用ルール

- `M_get`はPATH上のyt-dlpを優先せず、Music専用のuv環境と`uv.lock`にあるyt-dlpを使用する。古いシステム版でYouTubeの403エラーが再発する状態を防ぐ。
- yt-dlpの更新は `uv lock --upgrade-package yt-dlp --upgrade-package yt-dlp-ejs` と `uv sync` で行い、`./M_get --check` で実際のバージョンを確認する。
- Cookie不使用を維持し、個人のyt-dlp設定による旧クライアント指定を避けるため `--ignore-config` を使用する。
- `README_ja.md` は `.git/info/exclude` に登録し、コミットしない。
