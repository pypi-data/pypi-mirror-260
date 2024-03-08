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
from collections import deque
from bstack_utils.constants import *
class bstack1ll11ll11l_opy_:
    def __init__(self):
        self._11111l111l_opy_ = deque()
        self._111111lll1_opy_ = {}
        self._11111l11l1_opy_ = False
    def bstack111111l11l_opy_(self, test_name, bstack1111111l11_opy_):
        bstack1111111ll1_opy_ = self._111111lll1_opy_.get(test_name, {})
        return bstack1111111ll1_opy_.get(bstack1111111l11_opy_, 0)
    def bstack111111l1ll_opy_(self, test_name, bstack1111111l11_opy_):
        bstack11111l1111_opy_ = self.bstack111111l11l_opy_(test_name, bstack1111111l11_opy_)
        self.bstack1111111lll_opy_(test_name, bstack1111111l11_opy_)
        return bstack11111l1111_opy_
    def bstack1111111lll_opy_(self, test_name, bstack1111111l11_opy_):
        if test_name not in self._111111lll1_opy_:
            self._111111lll1_opy_[test_name] = {}
        bstack1111111ll1_opy_ = self._111111lll1_opy_[test_name]
        bstack11111l1111_opy_ = bstack1111111ll1_opy_.get(bstack1111111l11_opy_, 0)
        bstack1111111ll1_opy_[bstack1111111l11_opy_] = bstack11111l1111_opy_ + 1
    def bstack111lll111_opy_(self, bstack111111l1l1_opy_, bstack111111l111_opy_):
        bstack111111ll1l_opy_ = self.bstack111111l1ll_opy_(bstack111111l1l1_opy_, bstack111111l111_opy_)
        bstack111111ll11_opy_ = bstack11l1l11ll1_opy_[bstack111111l111_opy_]
        bstack111111llll_opy_ = bstack1l1l1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐔ").format(bstack111111l1l1_opy_, bstack111111ll11_opy_, bstack111111ll1l_opy_)
        self._11111l111l_opy_.append(bstack111111llll_opy_)
    def bstack111ll111l_opy_(self):
        return len(self._11111l111l_opy_) == 0
    def bstack1ll1l1lll1_opy_(self):
        bstack1111111l1l_opy_ = self._11111l111l_opy_.popleft()
        return bstack1111111l1l_opy_
    def capturing(self):
        return self._11111l11l1_opy_
    def bstack1l1l1l1l1_opy_(self):
        self._11111l11l1_opy_ = True
    def bstack11l11llll_opy_(self):
        self._11111l11l1_opy_ = False