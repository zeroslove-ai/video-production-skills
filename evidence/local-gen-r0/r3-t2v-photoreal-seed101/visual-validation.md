# PM Visual Validation Evidence — R3

Source MP4 was not copied into this directory and is not committed.

## Source

- Run: `r3-t2v-photoreal-seed101-20260918`
- Source: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\result.mp4`
- Video: H.264, `864x480`, `124` frames, `24 fps`, `5.166667 s`
- MP4 SHA-256: `75d1896ad731eadeae6a0109dbee568c22e96ae310e19c603522f8b56aae4378`

## Extracted evidence

Frame indices are exact zero-based video-frame indices. Timestamps use `frame_index / 24`.

| Evidence | Frame index | Timestamp | SHA-256 |
|---|---:|---:|---|
| `first-frame.png` | 0 | 0.000000 s | `FB40360734C8BAF7CDEEFC4387CD770D8C518104E9E1A652BEC3EF2E5799DE4E` |
| `middle-frame.png` | 61 | 2.541667 s | `404594FCDCDA3C6FC18834741F08CAFF9A40C1F0ADF3B2CF41ADEB45C168FCC5` |
| `last-frame.png` | 123 | 5.125000 s | `fd89c7629cd0598d73a3a8b3983bf8a184286ba8ad1697548637bf45ec4010e0` |
| `contact-sheet.png` | — | — | `C846C093794AD65572C076B30A231D55939A0C36F957C0CF416E41335DD29F47` |

## Reproduction commands

```powershell
$mp4 = 'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\result.mp4'
$ev = 'C:\Users\JAEWAN\projects\video-production-skills\evidence\local-gen-r0\r3-t2v-photoreal-seed101'

ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,r_frame_rate -show_entries format=duration -of json $mp4
ffmpeg -hide_banner -loglevel error -y -i $mp4 -vf 'select=eq(n\,0)' -frames:v 1 -compression_level 9 (Join-Path $ev 'first-frame.png')
ffmpeg -hide_banner -loglevel error -y -i $mp4 -vf 'select=eq(n\,61)' -frames:v 1 -compression_level 9 (Join-Path $ev 'middle-frame.png')
ffmpeg -hide_banner -loglevel error -y -i $mp4 -vf 'select=eq(n\,123)' -frames:v 1 -compression_level 9 (Join-Path $ev 'last-frame.png')
```

Contact sheet command:

```powershell
$font = 'C\:/Windows/Fonts/arial.ttf'
$filter = "[0:v]pad=iw:ih+44:0:44:color=black,drawtext=fontfile='$font':text='r3-t2v-photoreal-seed101-20260918 | t=0.000s':fontcolor=white:fontsize=17:x=10:y=10[a];[1:v]pad=iw:ih+44:0:44:color=black,drawtext=fontfile='$font':text='r3-t2v-photoreal-seed101-20260918 | t=2.541667s':fontcolor=white:fontsize=17:x=10:y=10[b];[2:v]pad=iw:ih+44:0:44:color=black,drawtext=fontfile='$font':text='r3-t2v-photoreal-seed101-20260918 | t=5.125000s':fontcolor=white:fontsize=17:x=10:y=10[c];[a][b][c]hstack=inputs=3[out]"
ffmpeg -hide_banner -loglevel error -y -i (Join-Path $ev 'first-frame.png') -i (Join-Path $ev 'middle-frame.png') -i (Join-Path $ev 'last-frame.png') -filter_complex $filter -map '[out]' -frames:v 1 -compression_level 9 (Join-Path $ev 'contact-sheet.png')
```
