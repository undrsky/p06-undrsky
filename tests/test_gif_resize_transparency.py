# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from io import BytesIO
from os.path import abspath, dirname, join
from unittest import TestCase

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

COURSE_IMAGES_PATH = abspath(
    join(dirname(__file__), "../course/images/")
)


class ResizedGifTransparencyTestCase(TestCase):
    def get_context(self):
        cfg = Config(
            SECURITY_KEY="ACME-SEC",
            ENGINE="thumbor.engines.pil",
            PILLOW_PRESERVE_INDEXED_MODE=True,
        )
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = COURSE_IMAGES_PATH
        cfg.STORAGE = "thumbor.storages.no_storage"

        return Context(config=cfg)

    def test_resized_gif_keeps_transparent_background(self):
        context = self.get_context()
        with open(join(COURSE_IMAGES_PATH, "sticker.gif"), "rb") as f:
            source_buffer = f.read()

        source = Image.open(BytesIO(source_buffer))
        assert "transparency" in source.info

        engine = Engine(context)
        engine.load(source_buffer, ".gif")
        engine.resize(240, 160)
        result_buffer = engine.read(".gif")

        result = Image.open(BytesIO(result_buffer))
        assert result.format == "GIF"
        assert "transparency" in result.info

        rgba = result.convert("RGBA")
        corner = rgba.getpixel((0, 0))
        assert corner[3] == 0
