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
import sys
class bstack1l111111ll_opy_:
    def __init__(self, handler):
        self._11l1l1lll1_opy_ = sys.stdout.write
        self._11l1l1llll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1ll1l_opy_
        sys.stdout.error = self.bstack11l1ll1111_opy_
    def bstack11l1l1ll1l_opy_(self, _str):
        self._11l1l1lll1_opy_(_str)
        if self.handler:
            self.handler({bstack1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໠"): bstack1l1l1_opy_ (u"ࠨࡋࡑࡊࡔ࠭໡"), bstack1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໢"): _str})
    def bstack11l1ll1111_opy_(self, _str):
        self._11l1l1llll_opy_(_str)
        if self.handler:
            self.handler({bstack1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ໣"): bstack1l1l1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ໤"), bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1lll1_opy_
        sys.stderr.write = self._11l1l1llll_opy_