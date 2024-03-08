# coding: UTF-8
import sys
bstack1l1l11_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack1l1l1ll_opy_ = 7
def bstack1l1l1_opy_ (bstack1ll11l_opy_):
    global bstack1l11_opy_
    bstack11l1lll_opy_ = ord (bstack1ll11l_opy_ [-1])
    bstack111llll_opy_ = bstack1ll11l_opy_ [:-1]
    bstack1ll1ll1_opy_ = bstack11l1lll_opy_ % len (bstack111llll_opy_)
    bstack11llll1_opy_ = bstack111llll_opy_ [:bstack1ll1ll1_opy_] + bstack111llll_opy_ [bstack1ll1ll1_opy_:]
    if bstack1l1l11_opy_:
        bstack111ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll1l_opy_ + bstack11l1lll_opy_) % bstack1l1l1ll_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack111ll_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll1l_opy_ + bstack11l1lll_opy_) % bstack1l1l1ll_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack111ll_opy_)
class bstack111l111l1_opy_:
    def __init__(self, handler):
        self._1lllll11111_opy_ = None
        self.handler = handler
        self._1lllll1111l_opy_ = self.bstack1lllll111l1_opy_()
        self.patch()
    def patch(self):
        self._1lllll11111_opy_ = self._1lllll1111l_opy_.execute
        self._1lllll1111l_opy_.execute = self.bstack1llll1lllll_opy_()
    def bstack1llll1lllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑭ"), driver_command, None, this, args)
            response = self._1lllll11111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑮ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lllll1111l_opy_.execute = self._1lllll11111_opy_
    @staticmethod
    def bstack1lllll111l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver