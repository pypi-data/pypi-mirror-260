from typing import Union

from typeguard import typechecked
from loguru import logger
import attr

@attr.define(repr=False)
class ATest():
    param: str = None

    @logger.catch(reraise=True)
    @typechecked
    def __init__(self, param: str = None):
        self.param = param

if __name__=="__main__":
    obj = ATest()
