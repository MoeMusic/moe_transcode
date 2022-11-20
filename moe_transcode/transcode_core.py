"""Transcode music."""

import logging
import shlex
import subprocess
from pathlib import Path
from typing import Literal, Optional, TypeVar

import dynaconf
import moe
from moe import config
from moe.library import Album, Track
from moe.plugins.move import fmt_item_path

__all__ = ["I", "TranscodeFormat", "transcode"]

log = logging.getLogger("moe.transcode")

TranscodeFormat = Literal["mp3 v2", "mp3 v0", "mp3 320"]
FFMPEG_MP3_ARG = {
    "mp3 v0": "-qscale:a 0",
    "mp3 v2": "-qscale:a 2",
    "mp3 320": "-b:a 320k",
}


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator(
            "TRANSCODE.TRANSCODE_PATH",
            default=Path(settings.library_path) / "transcode",
        )
    )


I = TypeVar("I", Album, Track)
"""Type hint representing either an Album or a Track."""


def transcode(
    item: I, to_format: TranscodeFormat, out_path: Optional[Path] = None
) -> I:
    """Transcodes a track or album to a specific format.

    Args:
        item: Track or Album to transcode. The track, or tracks contained
            in the album will only be transcoded if they are flacs.
        to_format: Format to transcode to.
        out_path: Path of the transcoded item. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting.

    Returns:
        The transcoded track or album.

    Raises:
        ValueError: ``item`` contains a non-supported audio format.
    """
    transcode_path = Path(config.CONFIG.settings.transcode.transcode_path).expanduser()
    out_path = out_path or fmt_item_path(item, transcode_path)

    if isinstance(item, Album):
        return _transcode_album(item, to_format, out_path)
    return _transcode_track(item, to_format, out_path)


def _transcode_album(album: Album, to_format: TranscodeFormat, out_path: Path) -> Album:
    """Transcodes an album to a specific format.

    Args:
        album: Album to transcode. Must contain flacs only.
        to_format: Format to transcode to.
        out_path: Path of the transcoded album. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting.

    Returns:
        The transcoded album.

    Raises:
        ValueError: ``album`` contains a non-supported audio format.
    """
    log.debug(f"Transcoding album. [{album=!r}, {to_format=!r}, {out_path=!r}]")

    for track in album.tracks:
        if track.audio_format != "flac":
            raise ValueError(
                f"Album contains track with unsupported format. [{track=!r}]"
            )

    out_path.mkdir(parents=True, exist_ok=True)

    for track in album.tracks:
        track_out_path = out_path / (track.path.stem + ".mp3")
        transcode(track, to_format, track_out_path)

    transcoded_album = Album.from_dir(out_path)
    log.info(f"Transcoded album. [{transcoded_album=!r}]")

    return transcoded_album


def _transcode_track(track: Track, to_format: TranscodeFormat, out_path: Path) -> Track:
    """Transcodes a track to a specific format.

    Args:
        track: Track to transcode. The track will only be transcoded if it is a flac.
        to_format: Format to transcode to.
        out_path: Path of the transcoded track. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting.

    Returns:
        The transcoded track.

    Raises:
        ValueError: ``track`` contains a non-supported audio format.
    """
    log.debug(f"Transcoding track. [{track=!r}, {to_format=!r}, {out_path=!r}]")

    if not track.audio_format == "flac":
        raise ValueError(f"Track has unsupported audio format. [{track=!r}]")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path = out_path.with_suffix(".mp3")

    args = shlex.split(
        f"ffmpeg -i '{track.path.resolve()}' "
        f"-codec:a libmp3lame {FFMPEG_MP3_ARG[to_format]} '{out_path.resolve()}'"
    )
    subprocess.run(args)

    transcoded_track = Track.from_file(out_path)
    log.info(f"Transcoded track. [{transcoded_track=!r}]")

    return transcoded_track
