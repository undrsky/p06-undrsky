# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from os.path import abspath, dirname, join
from unittest import TestCase

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.engines.pil import Engine
from thumbor.importer import Importer
from thumbor.transformer import Transformer

COURSE_IMAGES_PATH = abspath(join(dirname(__file__), "../course/images/"))


class TransparentWideResizeTestCase(TestCase):
    def get_context(self, width, height):
        cfg = Config(
            SECURITY_KEY="ACME-SEC",
            ENGINE="thumbor.engines.pil",
            LOADER="thumbor.loaders.file_loader",
            FILE_LOADER_ROOT_PATH=COURSE_IMAGES_PATH,
            STORAGE="thumbor.storages.no_storage",
        )
        importer = Importer(cfg)
        importer.import_modules()

        context = Context(config=cfg, importer=importer)
        context.request = RequestParameters(width=width, height=height)
        context.request.engine = context.modules.engine
        context.transformer = Transformer(context)
        return context

    def test_transparent_png_resized_wide_keeps_visible_pixels(self):
        context = self.get_context(800, 20)
        with open(join(COURSE_IMAGES_PATH, "rainbow.png"), "rb") as f:
            source_buffer = f.read()

        engine = context.modules.engine
        engine.load(source_buffer, ".png")
        context.transformer.img_operation_worker()

        assert isinstance(engine, Engine)
        assert engine.size == (800, 20)
        alpha_min, alpha_max = engine.image.convert("RGBA").getchannel(
            "A"
        ).getextrema()
        assert alpha_max > 0, (
            "Every pixel of the 800x20 result is fully transparent "
            f"(alpha range {alpha_min}..{alpha_max})"
        )
