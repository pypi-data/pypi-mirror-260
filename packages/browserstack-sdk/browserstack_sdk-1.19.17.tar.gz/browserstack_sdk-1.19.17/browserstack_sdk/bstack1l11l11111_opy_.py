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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lll11l11_opy_, bstack11ll1ll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
        self.bstack11ll1ll1l1_opy_ = bstack11ll1ll1l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11llll1l11_opy_(bstack11ll1l1l11_opy_):
        bstack11ll1l11ll_opy_ = []
        if bstack11ll1l1l11_opy_:
            tokens = str(os.path.basename(bstack11ll1l1l11_opy_)).split(bstack1l1111l_opy_ (u"ࠦࡤࠨว"))
            camelcase_name = bstack1l1111l_opy_ (u"ࠧࠦࠢศ").join(t.title() for t in tokens)
            suite_name, bstack11ll1l1l1l_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l11ll_opy_.append(suite_name)
        return bstack11ll1l11ll_opy_
    @staticmethod
    def bstack11ll1l1ll1_opy_(typename):
        if bstack1l1111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤษ") in typename:
            return bstack1l1111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣส")
        return bstack1l1111l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤห")