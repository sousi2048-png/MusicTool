# MusicTool

MusicTool is a small set of command line tools for managing local music files:

- `M_get`: download audio from YouTube, NicoNico, and other sites supported by `yt-dlp`
- `M_norm`: normalize local audio files toward Spotify-like loudness so local tracks do not sound much louder or quieter than streamed tracks
- `M_mp3`: convert audio files in a directory to MP3 without deleting the originals

The tools are written in Python and use `yt-dlp` and `ffmpeg` for the heavy lifting.

## Requirements

- Python 3
- `ffmpeg` and `ffprobe`
- `yt-dlp` for `M_get`
- Optional: `jq`
- Optional for future YouTube support: `deno`, `node`, or `bun`

On macOS with Homebrew:

```sh
brew install yt-dlp ffmpeg jq deno
```

Make the tools executable after cloning:

```sh
chmod +x M_get M_norm M_mp3
```

Check dependencies:

```sh
./M_get --check
./M_norm --check
./M_mp3 --check
```

## M_get

`M_get` downloads audio without using cookies. It asks `yt-dlp` for the best available audio stream, extracts audio with `ffmpeg`, creates a safe filename from the video title, and appends a Markdown download log.

Features:

- Works with YouTube, NicoNico, and other `yt-dlp` supported sites
- Selects `bestaudio/best`
- Does not read cookies or browser cookies
- Normalizes YouTube radio/playlist URLs such as `watch?v=ID&list=RD...&start_radio=1` to a single-track `watch?v=ID` URL
- Supports direct URL arguments and URL files
- Removes URLs from `url.md` after successful downloads when the URL came from that file
- Writes successful downloads to `download_log.md`

Download one URL:

```sh
./M_get "https://www.youtube.com/watch?v=VIDEO_ID"
```

Choose an output directory:

```sh
./M_get -o ./downloads "https://www.nicovideo.jp/watch/sm123456"
```

Choose an audio format:

```sh
./M_get --format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

Supported output formats:

- `best`
- `m4a`
- `mp3`
- `opus`
- `flac`
- `wav`

Apply two-pass loudness normalization while downloading:

```sh
./M_get --normalize --format m4a "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download multiple URLs:

```sh
./M_get URL1 URL2 URL3
```

### URL File Workflow

If you run `M_get` with no URL arguments, it reads URLs from `url.md` in the same directory as the script:

```sh
./M_get
```

You can also choose another file:

```sh
./M_get --url-file ./my_urls.md
```

The URL file can be plain text or Markdown. Any `http://` or `https://` URL is extracted. After a file-sourced URL downloads successfully, that URL is removed from the URL file.

Example `url.md`:

```md
https://www.youtube.com/watch?v=VIDEO_ID
https://www.nicovideo.jp/watch/sm123456
```

### M_get Defaults

Default output directory:

```text
~/Music/Music/Media.localized/Music/Download
```

This path is convenient for macOS Music.app local files. Use `-o` if you want another location.

Default log file:

```text
download_log.md
```

Use another log file:

```sh
./M_get --log-file ./download_log.md URL
```

## M_norm

`M_norm` normalizes local audio files toward Spotify-like playback loudness. This is useful when you listen to local files in Spotify and want them to be closer in volume to Spotify catalog tracks.

Default target:

- Integrated loudness: `-14 LUFS`
- True peak: `-1 dBTP`
- LRA target: `11 LU`

These defaults match Spotify's Normal loudness target closely enough for local-file use.

Supported input extensions:

- `mp3`
- `m4a`
- `aac`
- `opus`
- `ogg`
- `flac`
- `wav`
- `wave`
- `aiff`
- `aif`
- `webm`

Analyze only, without changing files:

```sh
./M_norm --dry-run /path/to/music
```

Normalize a directory recursively:

```sh
./M_norm /path/to/music
```

Normalize a single file:

```sh
./M_norm /path/to/song.opus
```

Use Spotify Quiet or Loud-style targets:

```sh
./M_norm --target quiet /path/to/music
./M_norm --target loud /path/to/music
```

Use custom targets:

```sh
./M_norm --lufs -14 --true-peak -1 /path/to/music
```

Force reprocessing even if a file is already near the target:

```sh
./M_norm --force /path/to/music
```

Disable recursive directory scanning:

```sh
./M_norm --no-recursive /path/to/music
```

### Backups and Logs

`M_norm` does not delete the original file immediately. After a successful normalization, it moves the original file into a backup directory and puts the normalized file in the original location.

Default backup directory:

```text
.M_norm_backup/
```

Default log file:

```text
normalize_log.md
```

Choose a custom backup directory:

```sh
./M_norm --backup-dir ./backup /path/to/music
```

Choose a custom log file:

```sh
./M_norm --log-file ./normalize_log.md /path/to/music
```

## M_mp3

`M_mp3` scans a directory recursively and converts supported audio files to MP3 using
the LAME VBR high-quality setting (`-q:a 2`). Original files are preserved, existing
MP3 files are skipped, and existing output files are not overwritten by default.

Convert a directory recursively, writing MP3 files next to their sources:

```sh
./M_mp3 /path/to/music
```

Preview conversions without writing files:

```sh
./M_mp3 --dry-run /path/to/music
```

Write converted files under a separate directory while preserving the source
directory structure:

```sh
./M_mp3 -o /path/to/mp3-output /path/to/music
```

Scan only the specified directory or explicitly replace existing output files:

```sh
./M_mp3 --no-recursive /path/to/music
./M_mp3 --overwrite /path/to/music
```

## Notes

- These tools are intended for personal/local media management.
- Respect copyright and the terms of service of any site you access.
- `M_norm` changes audio data by re-encoding files. Run `--dry-run` first and keep backups until you confirm the results.
- `M_get` intentionally does not use cookies for privacy.
