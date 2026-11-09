# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerTransparentRingTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_round_corner_has_no_dark_ring(self):
        image = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(50,255,255,255,1)",
            mode="RGBA",
        )
        source = self.get_fixture("source.jpg", mode="RGBA")

        dark_opaque_pixels = []
        for x in range(50):
            for y in range(50):
                out_r, out_g, out_b, out_a = image.getpixel((x, y))
                src_r, src_g, src_b, _ = source.getpixel((x, y))
                src_sum = src_r + src_g + src_b
                out_sum = out_r + out_g + out_b
                if out_a == 255 and src_sum > 0 and out_sum < 0.8 * src_sum:
                    dark_opaque_pixels.append((x, y))

        assert dark_opaque_pixels == [], (
            "Opaque edge pixels darkened toward black at "
            f"{len(dark_opaque_pixels)} positions, e.g. "
            f"{dark_opaque_pixels[:5]}"
        )
