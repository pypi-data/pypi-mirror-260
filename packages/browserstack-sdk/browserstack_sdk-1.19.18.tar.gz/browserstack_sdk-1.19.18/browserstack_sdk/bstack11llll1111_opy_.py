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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lll111ll_opy_, bstack11lll1111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
        self.bstack11lll1111l_opy_ = bstack11lll1111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l11111_opy_(bstack11ll1l1l1l_opy_):
        bstack11ll1l1l11_opy_ = []
        if bstack11ll1l1l1l_opy_:
            tokens = str(os.path.basename(bstack11ll1l1l1l_opy_)).split(bstack1l1l1_opy_ (u"ࠦࡤࠨว"))
            camelcase_name = bstack1l1l1_opy_ (u"ࠧࠦࠢศ").join(t.title() for t in tokens)
            suite_name, bstack11ll1l11ll_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l1l11_opy_.append(suite_name)
        return bstack11ll1l1l11_opy_
    @staticmethod
    def bstack11ll1l1ll1_opy_(typename):
        if bstack1l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤษ") in typename:
            return bstack1l1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣส")
        return bstack1l1l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤห")