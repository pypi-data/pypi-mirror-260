# coding: UTF-8
import sys
bstack11l1111_opy_ = sys.version_info [0] == 2
bstack11l_opy_ = 2048
bstack11llll_opy_ = 7
def bstack1l1111l_opy_ (bstack11l1ll_opy_):
    global bstack11ll11l_opy_
    bstack1111ll1_opy_ = ord (bstack11l1ll_opy_ [-1])
    bstack11l11_opy_ = bstack11l1ll_opy_ [:-1]
    bstack1ll11_opy_ = bstack1111ll1_opy_ % len (bstack11l11_opy_)
    bstack1l111ll_opy_ = bstack11l11_opy_ [:bstack1ll11_opy_] + bstack11l11_opy_ [bstack1ll11_opy_:]
    if bstack11l1111_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l_opy_ - (bstack111l11_opy_ + bstack1111ll1_opy_) % bstack11llll_opy_) for bstack111l11_opy_, char in enumerate (bstack1l111ll_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack11l_opy_ - (bstack111l11_opy_ + bstack1111ll1_opy_) % bstack11llll_opy_) for bstack111l11_opy_, char in enumerate (bstack1l111ll_opy_)])
    return eval (bstack11lll1l_opy_)
class bstack1ll111lll_opy_:
    def __init__(self, handler):
        self._1lllll1111l_opy_ = None
        self.handler = handler
        self._1llll1lllll_opy_ = self.bstack1lllll111l1_opy_()
        self.patch()
    def patch(self):
        self._1lllll1111l_opy_ = self._1llll1lllll_opy_.execute
        self._1llll1lllll_opy_.execute = self.bstack1lllll11111_opy_()
    def bstack1lllll11111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑭ"), driver_command, None, this, args)
            response = self._1lllll1111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1111l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑮ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1lllll_opy_.execute = self._1lllll1111l_opy_
    @staticmethod
    def bstack1lllll111l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver