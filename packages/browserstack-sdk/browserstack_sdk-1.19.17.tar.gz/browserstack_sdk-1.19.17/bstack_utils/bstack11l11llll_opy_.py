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
import json
class bstack11l1ll1ll1_opy_(object):
  bstack1l1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1111l_opy_ (u"ࠧࡿ໋ࠩ")), bstack1l1111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ໌"))
  bstack11l1ll11ll_opy_ = os.path.join(bstack1l1l111l1l_opy_, bstack1l1111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩໍ"))
  bstack11l1ll1l1l_opy_ = None
  perform_scan = None
  bstack11lllll11_opy_ = None
  bstack1lll11ll_opy_ = None
  bstack11ll11llll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1111l_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬ໎")):
      cls.instance = super(bstack11l1ll1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll1l11_opy_()
    return cls.instance
  def bstack11l1ll1l11_opy_(self):
    try:
      with open(self.bstack11l1ll11ll_opy_, bstack1l1111l_opy_ (u"ࠫࡷ࠭໏")) as bstack11ll1111l_opy_:
        bstack11l1ll11l1_opy_ = bstack11ll1111l_opy_.read()
        data = json.loads(bstack11l1ll11l1_opy_)
        if bstack1l1111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ໐") in data:
          self.bstack11ll11l11l_opy_(data[bstack1l1111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ໑")])
        if bstack1l1111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ໒") in data:
          self.bstack11l1lll111_opy_(data[bstack1l1111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ໓")])
    except:
      pass
  def bstack11l1lll111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l1111l_opy_ (u"ࠩࡶࡧࡦࡴࠧ໔")]
      self.bstack11lllll11_opy_ = scripts[bstack1l1111l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧ໕")]
      self.bstack1lll11ll_opy_ = scripts[bstack1l1111l_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨ໖")]
      self.bstack11ll11llll_opy_ = scripts[bstack1l1111l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪ໗")]
  def bstack11ll11l11l_opy_(self, bstack11l1ll1l1l_opy_):
    if bstack11l1ll1l1l_opy_ != None and len(bstack11l1ll1l1l_opy_) != 0:
      self.bstack11l1ll1l1l_opy_ = bstack11l1ll1l1l_opy_
  def store(self):
    try:
      with open(self.bstack11l1ll11ll_opy_, bstack1l1111l_opy_ (u"࠭ࡷࠨ໘")) as file:
        json.dump({
          bstack1l1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤ໙"): self.bstack11l1ll1l1l_opy_,
          bstack1l1111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤ໚"): {
            bstack1l1111l_opy_ (u"ࠤࡶࡧࡦࡴࠢ໛"): self.perform_scan,
            bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢໜ"): self.bstack11lllll11_opy_,
            bstack1l1111l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣໝ"): self.bstack1lll11ll_opy_,
            bstack1l1111l_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥໞ"): self.bstack11ll11llll_opy_
          }
        }, file)
    except:
      pass
  def bstack1l11l1ll_opy_(self, bstack11l1ll111l_opy_):
    try:
      return any(command.get(bstack1l1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫໟ")) == bstack11l1ll111l_opy_ for command in self.bstack11l1ll1l1l_opy_)
    except:
      return False
bstack11l11llll_opy_ = bstack11l1ll1ll1_opy_()