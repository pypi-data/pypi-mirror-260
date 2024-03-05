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
from browserstack_sdk.bstack1lll11l1ll_opy_ import bstack11l11ll11_opy_
from browserstack_sdk.bstack11lll1llll_opy_ import RobotHandler
def bstack1lll1111_opy_(framework):
    if framework.lower() == bstack1l11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᅹ"):
        return bstack11l11ll11_opy_.version()
    elif framework.lower() == bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᅺ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᅻ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11l11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᅼ")