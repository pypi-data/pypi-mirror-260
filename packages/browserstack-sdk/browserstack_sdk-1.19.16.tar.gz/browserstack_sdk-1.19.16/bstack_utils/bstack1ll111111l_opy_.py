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
import re
from bstack_utils.bstack1llll1ll11_opy_ import bstack1lllll1l1ll_opy_
def bstack1lllll1llll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐺ")):
        return bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᐻ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐼ")):
        return bstack1l11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᐽ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐾ")):
        return bstack1l11l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᐿ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑀ")):
        return bstack1l11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑁ")
def bstack1llllll11l1_opy_(fixture_name):
    return bool(re.match(bstack1l11l11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᑂ"), fixture_name))
def bstack1llllll111l_opy_(fixture_name):
    return bool(re.match(bstack1l11l11_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑃ"), fixture_name))
def bstack1llllll11ll_opy_(fixture_name):
    return bool(re.match(bstack1l11l11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑄ"), fixture_name))
def bstack1lllll11l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑅ")):
        return bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᑆ"), bstack1l11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑇ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑈ")):
        return bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑉ"), bstack1l11l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑊ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑋ")):
        return bstack1l11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᑌ"), bstack1l11l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑍ")
    elif fixture_name.startswith(bstack1l11l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑎ")):
        return bstack1l11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑏ"), bstack1l11l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑐ")
    return None, None
def bstack1lllll11l11_opy_(hook_name):
    if hook_name in [bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑑ"), bstack1l11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑒ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllll1ll11_opy_(hook_name):
    if hook_name in [bstack1l11l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᑓ"), bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᑔ")]:
        return bstack1l11l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑕ")
    elif hook_name in [bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᑖ"), bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᑗ")]:
        return bstack1l11l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑘ")
    elif hook_name in [bstack1l11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑙ"), bstack1l11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᑚ")]:
        return bstack1l11l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑛ")
    elif hook_name in [bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᑜ"), bstack1l11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᑝ")]:
        return bstack1l11l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑞ")
    return hook_name
def bstack1lllll11ll1_opy_(node, bstack1lllll1lll1_opy_):
    if hasattr(node, bstack1l11l11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᑟ")):
        parts = node.nodeid.rsplit(bstack1l11l11_opy_ (u"ࠣ࡝ࠥᑠ"))
        params = parts[-1]
        return bstack1l11l11_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᑡ").format(bstack1lllll1lll1_opy_.name, params)
    return bstack1lllll1lll1_opy_.name
def bstack1lllll11lll_opy_(node):
    try:
        bstack1lllll1l111_opy_ = []
        if hasattr(node, bstack1l11l11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑢ")):
            bstack1lllll1l111_opy_ = list(node.callspec.params[bstack1l11l11_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᑣ")].values())
        return bstack1lllll1l111_opy_
    except:
        return []
def bstack1lllll1l1l1_opy_(feature, bstack1lllll1lll1_opy_):
    return list(feature.tags) + list(bstack1lllll1lll1_opy_.tags)
def bstack1lllll1ll1l_opy_(report):
    try:
        status = bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑤ")
        if report.passed or (report.failed and hasattr(report, bstack1l11l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᑥ"))):
            status = bstack1l11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑦ")
        elif report.skipped:
            status = bstack1l11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᑧ")
        bstack1lllll1l1ll_opy_(status)
    except:
        pass
def bstack1l1l1l1111_opy_(status):
    try:
        bstack1lllll1l11l_opy_ = bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑨ")
        if status == bstack1l11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᑩ"):
            bstack1lllll1l11l_opy_ = bstack1l11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑪ")
        elif status == bstack1l11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᑫ"):
            bstack1lllll1l11l_opy_ = bstack1l11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑬ")
        bstack1lllll1l1ll_opy_(bstack1lllll1l11l_opy_)
    except:
        pass
def bstack1llllll1111_opy_(item=None, report=None, summary=None, extra=None):
    return