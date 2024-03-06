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
from collections import deque
from bstack_utils.constants import *
class bstack1l1llllll1_opy_:
    def __init__(self):
        self._111111l1ll_opy_ = deque()
        self._111111ll11_opy_ = {}
        self._111111l111_opy_ = False
    def bstack1111111l1l_opy_(self, test_name, bstack111111lll1_opy_):
        bstack111111l1l1_opy_ = self._111111ll11_opy_.get(test_name, {})
        return bstack111111l1l1_opy_.get(bstack111111lll1_opy_, 0)
    def bstack11111l1111_opy_(self, test_name, bstack111111lll1_opy_):
        bstack111111l11l_opy_ = self.bstack1111111l1l_opy_(test_name, bstack111111lll1_opy_)
        self.bstack1111111lll_opy_(test_name, bstack111111lll1_opy_)
        return bstack111111l11l_opy_
    def bstack1111111lll_opy_(self, test_name, bstack111111lll1_opy_):
        if test_name not in self._111111ll11_opy_:
            self._111111ll11_opy_[test_name] = {}
        bstack111111l1l1_opy_ = self._111111ll11_opy_[test_name]
        bstack111111l11l_opy_ = bstack111111l1l1_opy_.get(bstack111111lll1_opy_, 0)
        bstack111111l1l1_opy_[bstack111111lll1_opy_] = bstack111111l11l_opy_ + 1
    def bstack1ll1l1l1l_opy_(self, bstack111111llll_opy_, bstack1111111l11_opy_):
        bstack111111ll1l_opy_ = self.bstack11111l1111_opy_(bstack111111llll_opy_, bstack1111111l11_opy_)
        bstack11111l11l1_opy_ = bstack11l1l1l11l_opy_[bstack1111111l11_opy_]
        bstack11111l111l_opy_ = bstack1l1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐔ").format(bstack111111llll_opy_, bstack11111l11l1_opy_, bstack111111ll1l_opy_)
        self._111111l1ll_opy_.append(bstack11111l111l_opy_)
    def bstack11ll111l1_opy_(self):
        return len(self._111111l1ll_opy_) == 0
    def bstack1llll1llll_opy_(self):
        bstack1111111ll1_opy_ = self._111111l1ll_opy_.popleft()
        return bstack1111111ll1_opy_
    def capturing(self):
        return self._111111l111_opy_
    def bstack1ll11lll11_opy_(self):
        self._111111l111_opy_ = True
    def bstack1llllll111_opy_(self):
        self._111111l111_opy_ = False