#########
Transcode
#########
Plugin for Moe that transcodes music.

Currently only flac -> mp3 [v0, v2, 320] is supported.

************
Installation
************
1. Install via pip

   .. code-block:: bash

       $ pip install moe_transcode

2. `Install ffmpeg <https://ffmpeg.org/download.html>`_

   .. important::

      Ensure ``ffmpeg`` is in your respective OS's path environment variable.

*************
Configuration
*************
Add ``transcode`` to the ``enabled_plugins`` configuration option.
