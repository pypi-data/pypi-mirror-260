#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = wwdeng
import gdb


class Heap:
    def __init__(self):
        try:
            self.xStart = gdb.parse_and_eval("xStart")
            self.pxEnd = gdb.parse_and_eval("pxEnd")
            self.BlockLink_t = gdb.lookup_type("BlockLink_t")
        except gdb.error as err:
            raise err

    def show(self):
        xStart = gdb.parse_and_eval("xStart")
        pxEnd = gdb.parse_and_eval("pxEnd")

        pxNextFreeBlock = xStart["pxNextFreeBlock"]
        while pxNextFreeBlock < pxEnd:
            block = pxNextFreeBlock.cast(
                gdb.lookup_type("BlockLink_t").pointer()
            ).dereference()
            print(block)
            pxNextFreeBlock = block["pxNextFreeBlock"]


class FreeRtosHeap(gdb.Command):
    """Generate a print out of the current heap info."""

    def __init__(self):
        super().__init__("freertos heap", gdb.COMMAND_USER)

    @staticmethod
    def invoke(_, __):
        try:
            Heap().show()
        except gdb.error as err:
            print(err)
