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
import sys
class bstack11lll1ll1l_opy_:
    def __init__(self, handler):
        self._11l1l1l1ll_opy_ = sys.stdout.write
        self._11l1l1l11l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1l111_opy_
        sys.stdout.error = self.bstack11l1l1l1l1_opy_
    def bstack11l1l1l111_opy_(self, _str):
        self._11l1l1l1ll_opy_(_str)
        if self.handler:
            self.handler({bstack1l11l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໠"): bstack1l11l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭໡"), bstack1l11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໢"): _str})
    def bstack11l1l1l1l1_opy_(self, _str):
        self._11l1l1l11l_opy_(_str)
        if self.handler:
            self.handler({bstack1l11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ໣"): bstack1l11l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ໤"), bstack1l11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1l1ll_opy_
        sys.stderr.write = self._11l1l1l11l_opy_