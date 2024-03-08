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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1llll111_opy_ as bstack1l11lllll_opy_
from browserstack_sdk.bstack1ll11l1l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1111_opy_
class bstack11l111ll1_opy_:
    def __init__(self, args, logger, bstack11lll111ll_opy_, bstack11lll1111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
        self.bstack11lll1111l_opy_ = bstack11lll1111l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11ll111_opy_ = []
        self.bstack11ll1ll1ll_opy_ = None
        self.bstack11111ll1_opy_ = []
        self.bstack11ll1lllll_opy_ = self.bstack1l1ll11l11_opy_()
        self.bstack1llll1ll11_opy_ = -1
    def bstack11llll111_opy_(self, bstack11ll1lll1l_opy_):
        self.parse_args()
        self.bstack11ll1l1lll_opy_()
        self.bstack11lll11l1l_opy_(bstack11ll1lll1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll1ll1l1_opy_():
        import importlib
        if getattr(importlib, bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭จ"), False):
            bstack11ll1llll1_opy_ = importlib.find_loader(bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫฉ"))
        else:
            bstack11ll1llll1_opy_ = importlib.util.find_spec(bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬช"))
    def bstack11lll11l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1llll1ll11_opy_ = -1
        if bstack1l1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫซ") in self.bstack11lll111ll_opy_:
            self.bstack1llll1ll11_opy_ = int(self.bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬฌ")])
        try:
            bstack11lll111l1_opy_ = [bstack1l1l1_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨญ"), bstack1l1l1_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪฎ"), bstack1l1l1_opy_ (u"ࠨ࠯ࡳࠫฏ")]
            if self.bstack1llll1ll11_opy_ >= 0:
                bstack11lll111l1_opy_.extend([bstack1l1l1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฐ"), bstack1l1l1_opy_ (u"ࠪ࠱ࡳ࠭ฑ")])
            for arg in bstack11lll111l1_opy_:
                self.bstack11lll11l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1l1lll_opy_(self):
        bstack11ll1ll1ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll1ll1ll_opy_ = bstack11ll1ll1ll_opy_
        return bstack11ll1ll1ll_opy_
    def bstack1l1l1llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll1ll1l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack111l1111_opy_)
    def bstack11lll11l1l_opy_(self, bstack11ll1lll1l_opy_):
        bstack11l11111_opy_ = Config.bstack1llllllll_opy_()
        if bstack11ll1lll1l_opy_:
            self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨฒ"))
            self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"࡚ࠬࡲࡶࡧࠪณ"))
        if bstack11l11111_opy_.bstack11lll11111_opy_():
            self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬด"))
            self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠧࡕࡴࡸࡩࠬต"))
        self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠨ࠯ࡳࠫถ"))
        self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧท"))
        self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬธ"))
        self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫน"))
        if self.bstack1llll1ll11_opy_ > 1:
            self.bstack11ll1ll1ll_opy_.append(bstack1l1l1_opy_ (u"ࠬ࠳࡮ࠨบ"))
            self.bstack11ll1ll1ll_opy_.append(str(self.bstack1llll1ll11_opy_))
    def bstack11ll1lll11_opy_(self):
        bstack11111ll1_opy_ = []
        for spec in self.bstack1l11ll111_opy_:
            bstack1lll11l1ll_opy_ = [spec]
            bstack1lll11l1ll_opy_ += self.bstack11ll1ll1ll_opy_
            bstack11111ll1_opy_.append(bstack1lll11l1ll_opy_)
        self.bstack11111ll1_opy_ = bstack11111ll1_opy_
        return bstack11111ll1_opy_
    def bstack1l1ll11l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1lllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1lllll_opy_ = False
        return self.bstack11ll1lllll_opy_
    def bstack111llll11_opy_(self, bstack11ll1ll111_opy_, bstack11llll111_opy_):
        bstack11llll111_opy_[bstack1l1l1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ป")] = self.bstack11lll111ll_opy_
        multiprocessing.set_start_method(bstack1l1l1_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭ผ"))
        if bstack1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฝ") in self.bstack11lll111ll_opy_:
            bstack1llll11111_opy_ = []
            manager = multiprocessing.Manager()
            bstack1ll111llll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬพ")]):
                bstack1llll11111_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11ll1ll111_opy_,
                                                           args=(self.bstack11ll1ll1ll_opy_, bstack11llll111_opy_, bstack1ll111llll_opy_)))
            i = 0
            bstack11lll11ll1_opy_ = len(self.bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฟ")])
            for t in bstack1llll11111_opy_:
                os.environ[bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫภ")] = str(i)
                os.environ[bstack1l1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ม")] = json.dumps(self.bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩย")][i % bstack11lll11ll1_opy_])
                i += 1
                t.start()
            for t in bstack1llll11111_opy_:
                t.join()
            return list(bstack1ll111llll_opy_)
    @staticmethod
    def bstack1l1111l1l_opy_(driver, bstack1l11l1l1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫร"), None)
        if item and getattr(item, bstack1l1l1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࠪฤ"), None) and not getattr(item, bstack1l1l1_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡳࡵࡥࡤࡰࡰࡨࠫล"), False):
            logger.info(
                bstack1l1l1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠤฦ"))
            bstack11ll1ll11l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11lllll_opy_.bstack11llll11l_opy_(driver, bstack11ll1ll11l_opy_, item.name, item.module.__name__, item.path, bstack1l11l1l1l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)