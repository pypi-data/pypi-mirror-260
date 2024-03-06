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
conf = {
    bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ໦"): False,
    bstack1l1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ໧"): True,
    bstack1l1111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ໨"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l1l1ll11_opy_ = conf
    @classmethod
    def bstack1lll1ll1ll_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._11l1l1ll11_opy_.get(property_name, None)
    def bstack1lllll1ll1_opy_(self, property_name, bstack11l1l1l1ll_opy_):
        self._11l1l1ll11_opy_[property_name] = bstack11l1l1l1ll_opy_
    def bstack1111l1lll_opy_(self, val):
        self._11l1l1ll11_opy_[bstack1l1111l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ໩")] = bool(val)
    def bstack11lll111l1_opy_(self):
        return self._11l1l1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ໪"), False)