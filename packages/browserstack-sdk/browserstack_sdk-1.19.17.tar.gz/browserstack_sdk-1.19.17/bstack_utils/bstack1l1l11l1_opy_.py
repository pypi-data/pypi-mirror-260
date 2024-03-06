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
from browserstack_sdk.bstack1l1l1111l_opy_ import bstack11l1l11ll_opy_
from browserstack_sdk.bstack1l11l11111_opy_ import RobotHandler
def bstack11ll1l11l_opy_(framework):
    if framework.lower() == bstack1l1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᅹ"):
        return bstack11l1l11ll_opy_.version()
    elif framework.lower() == bstack1l1111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᅺ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᅻ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1111l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᅼ")