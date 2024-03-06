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
import sys
class bstack1l1111ll1l_opy_:
    def __init__(self, handler):
        self._11l1l1lll1_opy_ = sys.stdout.write
        self._11l1l1ll1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1llll_opy_
        sys.stdout.error = self.bstack11l1ll1111_opy_
    def bstack11l1l1llll_opy_(self, _str):
        self._11l1l1lll1_opy_(_str)
        if self.handler:
            self.handler({bstack1l1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໠"): bstack1l1111l_opy_ (u"ࠨࡋࡑࡊࡔ࠭໡"), bstack1l1111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໢"): _str})
    def bstack11l1ll1111_opy_(self, _str):
        self._11l1l1ll1l_opy_(_str)
        if self.handler:
            self.handler({bstack1l1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ໣"): bstack1l1111l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ໤"), bstack1l1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1lll1_opy_
        sys.stderr.write = self._11l1l1ll1l_opy_