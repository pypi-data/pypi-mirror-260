from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips


def concat_video(files: list[Path], output_file: Path):
    """
    合并视频
    
    后处理：删除原视频
    """
    clips = [VideoFileClip(f) for f in files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file)
    for f in files:
        f.unlink()


if __name__ == "__main__":
    filelist = [
        "S:/rather/pic/daoayao/2021-08-06-vid_258.mp4",
        "S:/rather/pic/daoayao/2021-08-08-vid_256.mp4",
    ]
    print(concat_video(filelist, "output.mp4"))
