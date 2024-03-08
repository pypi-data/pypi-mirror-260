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
import re
from bstack_utils.bstack1l1l11l1_opy_ import bstack1lllllll111_opy_
def bstack1llllll1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐺ")):
        return bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᐻ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐼ")):
        return bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᐽ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᐾ")):
        return bstack1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᐿ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑀ")):
        return bstack1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑁ")
def bstack1llllll1l11_opy_(fixture_name):
    return bool(re.match(bstack1l1l1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᑂ"), fixture_name))
def bstack1lllllll1ll_opy_(fixture_name):
    return bool(re.match(bstack1l1l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑃ"), fixture_name))
def bstack1llllll1ll1_opy_(fixture_name):
    return bool(re.match(bstack1l1l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑄ"), fixture_name))
def bstack1llllll111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑅ")):
        return bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᑆ"), bstack1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑇ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑈ")):
        return bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑉ"), bstack1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑊ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑋ")):
        return bstack1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᑌ"), bstack1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑍ")
    elif fixture_name.startswith(bstack1l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑎ")):
        return bstack1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑏ"), bstack1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑐ")
    return None, None
def bstack1lllll1llll_opy_(hook_name):
    if hook_name in [bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑑ"), bstack1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑒ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llllllll11_opy_(hook_name):
    if hook_name in [bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᑓ"), bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᑔ")]:
        return bstack1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑕ")
    elif hook_name in [bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᑖ"), bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᑗ")]:
        return bstack1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑘ")
    elif hook_name in [bstack1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑙ"), bstack1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᑚ")]:
        return bstack1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑛ")
    elif hook_name in [bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᑜ"), bstack1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᑝ")]:
        return bstack1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑞ")
    return hook_name
def bstack1lllllll1l1_opy_(node, scenario):
    if hasattr(node, bstack1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᑟ")):
        parts = node.nodeid.rsplit(bstack1l1l1_opy_ (u"ࠣ࡝ࠥᑠ"))
        params = parts[-1]
        return bstack1l1l1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᑡ").format(scenario.name, params)
    return scenario.name
def bstack1llllll11l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑢ")):
            examples = list(node.callspec.params[bstack1l1l1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᑣ")].values())
        return examples
    except:
        return []
def bstack1llllll1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllll1l1l_opy_(report):
    try:
        status = bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑤ")
        if report.passed or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᑥ"))):
            status = bstack1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑦ")
        elif report.skipped:
            status = bstack1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᑧ")
        bstack1lllllll111_opy_(status)
    except:
        pass
def bstack1lll1ll1_opy_(status):
    try:
        bstack1lllllll11l_opy_ = bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑨ")
        if status == bstack1l1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᑩ"):
            bstack1lllllll11l_opy_ = bstack1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑪ")
        elif status == bstack1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᑫ"):
            bstack1lllllll11l_opy_ = bstack1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑬ")
        bstack1lllllll111_opy_(bstack1lllllll11l_opy_)
    except:
        pass
def bstack1llllll11ll_opy_(item=None, report=None, summary=None, extra=None):
    return