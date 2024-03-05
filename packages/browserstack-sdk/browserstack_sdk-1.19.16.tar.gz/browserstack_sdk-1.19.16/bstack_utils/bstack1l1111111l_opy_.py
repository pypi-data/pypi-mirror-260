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
from uuid import uuid4
from bstack_utils.helper import bstack1lll11lll_opy_, bstack11l11l11ll_opy_
from bstack_utils.bstack1ll111111l_opy_ import bstack1lllll11lll_opy_
class bstack11lll111l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l1l1l_opy_=None, framework=None, tags=[], scope=[], bstack1lll1llll1l_opy_=None, bstack1llll1111ll_opy_=True, bstack1lll1lllll1_opy_=None, bstack111lllll1_opy_=None, result=None, duration=None, bstack11lll1l11l_opy_=None, meta={}):
        self.bstack11lll1l11l_opy_ = bstack11lll1l11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll1111ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l1l1l_opy_ = bstack1l111l1l1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
        self.bstack1lll1lllll1_opy_ = bstack1lll1lllll1_opy_
        self.bstack111lllll1_opy_ = bstack111lllll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11llllll1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll11llll_opy_(self):
        bstack1llll11ll1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᒣ"): bstack1llll11ll1l_opy_,
            bstack1l11l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᒤ"): bstack1llll11ll1l_opy_,
            bstack1l11l11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᒥ"): bstack1llll11ll1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11l11_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᒦ") + key)
            setattr(self, key, val)
    def bstack1llll111ll1_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒧ"): self.name,
            bstack1l11l11_opy_ (u"ࠪࡦࡴࡪࡹࠨᒨ"): {
                bstack1l11l11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᒩ"): bstack1l11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒪ"),
                bstack1l11l11_opy_ (u"࠭ࡣࡰࡦࡨࠫᒫ"): self.code
            },
            bstack1l11l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᒬ"): self.scope,
            bstack1l11l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒭ"): self.tags,
            bstack1l11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᒮ"): self.framework,
            bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒯ"): self.bstack1l111l1l1l_opy_
        }
    def bstack1llll11ll11_opy_(self):
        return {
         bstack1l11l11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᒰ"): self.meta
        }
    def bstack1llll111lll_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒱ"): {
                bstack1l11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒲ"): self.bstack1lll1llll1l_opy_
            }
        }
    def bstack1lll1llllll_opy_(self, bstack1llll11111l_opy_, details):
        step = next(filter(lambda st: st[bstack1l11l11_opy_ (u"ࠧࡪࡦࠪᒳ")] == bstack1llll11111l_opy_, self.meta[bstack1l11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒴ")]), None)
        step.update(details)
    def bstack1llll11l111_opy_(self, bstack1llll11111l_opy_):
        step = next(filter(lambda st: st[bstack1l11l11_opy_ (u"ࠩ࡬ࡨࠬᒵ")] == bstack1llll11111l_opy_, self.meta[bstack1l11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒶ")]), None)
        step.update({
            bstack1l11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᒷ"): bstack1lll11lll_opy_()
        })
    def bstack1l111ll11l_opy_(self, bstack1llll11111l_opy_, result, duration=None):
        bstack1lll1lllll1_opy_ = bstack1lll11lll_opy_()
        if bstack1llll11111l_opy_ is not None and self.meta.get(bstack1l11l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒸ")):
            step = next(filter(lambda st: st[bstack1l11l11_opy_ (u"࠭ࡩࡥࠩᒹ")] == bstack1llll11111l_opy_, self.meta[bstack1l11l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒺ")]), None)
            step.update({
                bstack1l11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᒻ"): bstack1lll1lllll1_opy_,
                bstack1l11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᒼ"): duration if duration else bstack11l11l11ll_opy_(step[bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒽ")], bstack1lll1lllll1_opy_),
                bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᒾ"): result.result,
                bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᒿ"): str(result.exception) if result.exception else None
            })
    def bstack1l11111l1l_opy_(self, bstack1llll111l1l_opy_):
        if self.meta.get(bstack1l11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓀ")):
            self.meta[bstack1l11l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓁ")].append(bstack1llll111l1l_opy_)
        else:
            self.meta[bstack1l11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓂ")] = [ bstack1llll111l1l_opy_ ]
    def bstack1llll111111_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓃ"): self.bstack11llllll1l_opy_(),
            **self.bstack1llll111ll1_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll11ll11_opy_()
        }
    def bstack1llll11lll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓄ"): self.bstack1lll1lllll1_opy_,
            bstack1l11l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᓅ"): self.duration,
            bstack1l11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓆ"): self.result.result
        }
        if data[bstack1l11l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓇ")] == bstack1l11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᓈ"):
            data[bstack1l11l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᓉ")] = self.result.bstack11ll1l111l_opy_()
            data[bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᓊ")] = [{bstack1l11l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᓋ"): self.result.bstack111lll1l11_opy_()}]
        return data
    def bstack1llll11l1l1_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᓌ"): self.bstack11llllll1l_opy_(),
            **self.bstack1llll111ll1_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll11lll1_opy_(),
            **self.bstack1llll11ll11_opy_()
        }
    def bstack1l11111lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11l11_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᓍ") in event:
            return self.bstack1llll111111_opy_()
        elif bstack1l11l11_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓎ") in event:
            return self.bstack1llll11l1l1_opy_()
    def bstack1l11l1111l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1lll1lllll1_opy_ = time if time else bstack1lll11lll_opy_()
        self.duration = duration if duration else bstack11l11l11ll_opy_(self.bstack1l111l1l1l_opy_, self.bstack1lll1lllll1_opy_)
        if result:
            self.result = result
class bstack1l111ll1l1_opy_(bstack11lll111l1_opy_):
    def __init__(self, hooks=[], bstack11lll11lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lll11lll_opy_ = bstack11lll11lll_opy_
        super().__init__(*args, **kwargs, bstack111lllll1_opy_=bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࠬᓏ"))
    @classmethod
    def bstack1llll111l11_opy_(cls, bstack1lllll1lll1_opy_, feature, test, **kwargs):
        steps = []
        for step in bstack1lllll1lll1_opy_.steps:
            steps.append({
                bstack1l11l11_opy_ (u"ࠨ࡫ࡧࠫᓐ"): id(step),
                bstack1l11l11_opy_ (u"ࠩࡷࡩࡽࡺࠧᓑ"): step.name,
                bstack1l11l11_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᓒ"): step.keyword,
            })
        return bstack1l111ll1l1_opy_(
            **kwargs,
            meta={
                bstack1l11l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᓓ"): {
                    bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓔ"): feature.name,
                    bstack1l11l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᓕ"): feature.filename,
                    bstack1l11l11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᓖ"): feature.description
                },
                bstack1l11l11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᓗ"): {
                    bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᓘ"): bstack1lllll1lll1_opy_.name
                },
                bstack1l11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓙ"): steps,
                bstack1l11l11_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᓚ"): bstack1lllll11lll_opy_(test)
            }
        )
    def bstack1llll11l1ll_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᓛ"): self.hooks
        }
    def bstack1llll11l11l_opy_(self):
        if self.bstack11lll11lll_opy_:
            return {
                bstack1l11l11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᓜ"): self.bstack11lll11lll_opy_
            }
        return {}
    def bstack1llll11l1l1_opy_(self):
        return {
            **super().bstack1llll11l1l1_opy_(),
            **self.bstack1llll11l1ll_opy_()
        }
    def bstack1llll111111_opy_(self):
        return {
            **super().bstack1llll111111_opy_(),
            **self.bstack1llll11l11l_opy_()
        }
    def bstack1l11l1111l_opy_(self):
        return bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᓝ")
class bstack1l1111llll_opy_(bstack11lll111l1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack111lllll1_opy_=bstack1l11l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᓞ"))
    def bstack11lll1lll1_opy_(self):
        return self.hook_type
    def bstack1llll1111l1_opy_(self):
        return {
            bstack1l11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᓟ"): self.hook_type
        }
    def bstack1llll11l1l1_opy_(self):
        return {
            **super().bstack1llll11l1l1_opy_(),
            **self.bstack1llll1111l1_opy_()
        }
    def bstack1llll111111_opy_(self):
        return {
            **super().bstack1llll111111_opy_(),
            **self.bstack1llll1111l1_opy_()
        }
    def bstack1l11l1111l_opy_(self):
        return bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᓠ")