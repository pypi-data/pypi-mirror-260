# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll1ll_opy_ = 2048
bstack1l111ll_opy_ = 7
def bstack1l11l11_opy_ (bstack1l1l1l_opy_):
    global bstack111ll1l_opy_
    bstack1l1_opy_ = ord (bstack1l1l1l_opy_ [-1])
    bstack1lllllll_opy_ = bstack1l1l1l_opy_ [:-1]
    bstack1ll_opy_ = bstack1l1_opy_ % len (bstack1lllllll_opy_)
    bstack1l1l_opy_ = bstack1lllllll_opy_ [:bstack1ll_opy_] + bstack1lllllll_opy_ [bstack1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1ll_opy_ - (bstack1l1l11_opy_ + bstack1l1_opy_) % bstack1l111ll_opy_) for bstack1l1l11_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll1ll_opy_ - (bstack1l1l11_opy_ + bstack1l1_opy_) % bstack1l111ll_opy_) for bstack1l1l11_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack1l_opy_)
class bstack11lll1lll_opy_:
    def __init__(self, handler):
        self._1llll1l1l11_opy_ = None
        self.handler = handler
        self._1llll1l1l1l_opy_ = self.bstack1llll1l1ll1_opy_()
        self.patch()
    def patch(self):
        self._1llll1l1l11_opy_ = self._1llll1l1l1l_opy_.execute
        self._1llll1l1l1l_opy_.execute = self.bstack1llll1l1lll_opy_()
    def bstack1llll1l1lll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑭ"), driver_command, None, this, args)
            response = self._1llll1l1l11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11l11_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑮ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1l1l1l_opy_.execute = self._1llll1l1l11_opy_
    @staticmethod
    def bstack1llll1l1ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver