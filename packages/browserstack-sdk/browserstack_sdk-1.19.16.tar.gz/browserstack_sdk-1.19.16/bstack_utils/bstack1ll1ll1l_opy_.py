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
from collections import deque
from bstack_utils.constants import *
class bstack111l1l1l_opy_:
    def __init__(self):
        self._1111111111_opy_ = deque()
        self._1llllllll1l_opy_ = {}
        self._111111l11l_opy_ = False
    def bstack1lllllllll1_opy_(self, bstack1ll11l1l1l_opy_, bstack11111111ll_opy_):
        bstack1111111l1l_opy_ = self._1llllllll1l_opy_.get(bstack1ll11l1l1l_opy_, {})
        return bstack1111111l1l_opy_.get(bstack11111111ll_opy_, 0)
    def bstack1lllllll1ll_opy_(self, bstack1ll11l1l1l_opy_, bstack11111111ll_opy_):
        bstack111111l111_opy_ = self.bstack1lllllllll1_opy_(bstack1ll11l1l1l_opy_, bstack11111111ll_opy_)
        self.bstack1111111l11_opy_(bstack1ll11l1l1l_opy_, bstack11111111ll_opy_)
        return bstack111111l111_opy_
    def bstack1111111l11_opy_(self, bstack1ll11l1l1l_opy_, bstack11111111ll_opy_):
        if bstack1ll11l1l1l_opy_ not in self._1llllllll1l_opy_:
            self._1llllllll1l_opy_[bstack1ll11l1l1l_opy_] = {}
        bstack1111111l1l_opy_ = self._1llllllll1l_opy_[bstack1ll11l1l1l_opy_]
        bstack111111l111_opy_ = bstack1111111l1l_opy_.get(bstack11111111ll_opy_, 0)
        bstack1111111l1l_opy_[bstack11111111ll_opy_] = bstack111111l111_opy_ + 1
    def bstack11l1lll1l_opy_(self, bstack11111111l1_opy_, bstack1111111lll_opy_):
        bstack1111111ll1_opy_ = self.bstack1lllllll1ll_opy_(bstack11111111l1_opy_, bstack1111111lll_opy_)
        bstack111111111l_opy_ = bstack11l11lll1l_opy_[bstack1111111lll_opy_]
        bstack1llllllllll_opy_ = bstack1l11l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐔ").format(bstack11111111l1_opy_, bstack111111111l_opy_, bstack1111111ll1_opy_)
        self._1111111111_opy_.append(bstack1llllllllll_opy_)
    def bstack1l11ll1ll_opy_(self):
        return len(self._1111111111_opy_) == 0
    def bstack11l1ll11l_opy_(self):
        bstack1llllllll11_opy_ = self._1111111111_opy_.popleft()
        return bstack1llllllll11_opy_
    def capturing(self):
        return self._111111l11l_opy_
    def bstack1l11lllll_opy_(self):
        self._111111l11l_opy_ = True
    def bstack11lllllll_opy_(self):
        self._111111l11l_opy_ = False