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
from browserstack_sdk.bstack1l11ll1l1l_opy_ import bstack11l111ll1_opy_
from browserstack_sdk.bstack11llll1111_opy_ import RobotHandler
def bstack1lll11ll1l_opy_(framework):
    if framework.lower() == bstack1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᅹ"):
        return bstack11l111ll1_opy_.version()
    elif framework.lower() == bstack1l1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᅺ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᅻ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᅼ")