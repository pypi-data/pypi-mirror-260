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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lll1111l_opy_, bstack11ll1l1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll1111l_opy_ = bstack11lll1111l_opy_
        self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11llll1lll_opy_(bstack11ll1l1111_opy_):
        bstack11ll11lll1_opy_ = []
        if bstack11ll1l1111_opy_:
            tokens = str(os.path.basename(bstack11ll1l1111_opy_)).split(bstack1l11l11_opy_ (u"ࠦࡤࠨว"))
            camelcase_name = bstack1l11l11_opy_ (u"ࠧࠦࠢศ").join(t.title() for t in tokens)
            suite_name, bstack11ll11llll_opy_ = os.path.splitext(camelcase_name)
            bstack11ll11lll1_opy_.append(suite_name)
        return bstack11ll11lll1_opy_
    @staticmethod
    def bstack11ll1l111l_opy_(typename):
        if bstack1l11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤษ") in typename:
            return bstack1l11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣส")
        return bstack1l11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤห")