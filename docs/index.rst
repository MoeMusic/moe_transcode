#########
Transcode
#########
This is a plugin for Moe that provides functionality for transcoding music.

Currently only flac -> mp3 [v0, v2, 320] is supported.


TEST PREVIEW

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

This plugin has the following configuration options:

``transcode_path = {library_path}/transcode``
    The default path for transcoded files.

***
API
***
``moe_transcode``

.. automodule:: moe_transcode.transcode_core
   :members:
   :show-inheritance:
