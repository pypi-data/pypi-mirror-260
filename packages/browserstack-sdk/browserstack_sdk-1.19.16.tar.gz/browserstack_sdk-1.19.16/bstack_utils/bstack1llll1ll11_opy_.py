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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack1l1lll11l1_opy_, bstack11l1lllll_opy_, bstack1ll111lll_opy_, \
    bstack111lllllll_opy_
def bstack111lll1l1_opy_(bstack1llll1l11l1_opy_):
    for driver in bstack1llll1l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l111l1l_opy_(driver, status, reason=bstack1l11l11_opy_ (u"ࠩࠪᑯ")):
    bstack1l1l1l11l_opy_ = Config.bstack1l11l1llll_opy_()
    if bstack1l1l1l11l_opy_.bstack11ll1l11l1_opy_():
        return
    bstack1l1l1l1lll_opy_ = bstack1ll1111ll_opy_(bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑰ"), bstack1l11l11_opy_ (u"ࠫࠬᑱ"), status, reason, bstack1l11l11_opy_ (u"ࠬ࠭ᑲ"), bstack1l11l11_opy_ (u"࠭ࠧᑳ"))
    driver.execute_script(bstack1l1l1l1lll_opy_)
def bstack1ll1lll11_opy_(page, status, reason=bstack1l11l11_opy_ (u"ࠧࠨᑴ")):
    try:
        if page is None:
            return
        bstack1l1l1l11l_opy_ = Config.bstack1l11l1llll_opy_()
        if bstack1l1l1l11l_opy_.bstack11ll1l11l1_opy_():
            return
        bstack1l1l1l1lll_opy_ = bstack1ll1111ll_opy_(bstack1l11l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᑵ"), bstack1l11l11_opy_ (u"ࠩࠪᑶ"), status, reason, bstack1l11l11_opy_ (u"ࠪࠫᑷ"), bstack1l11l11_opy_ (u"ࠫࠬᑸ"))
        page.evaluate(bstack1l11l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᑹ"), bstack1l1l1l1lll_opy_)
    except Exception as e:
        print(bstack1l11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᑺ"), e)
def bstack1ll1111ll_opy_(type, name, status, reason, bstack1ll11lll1l_opy_, bstack1lll11ll_opy_):
    bstack11ll1l1l1_opy_ = {
        bstack1l11l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᑻ"): type,
        bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᑼ"): {}
    }
    if type == bstack1l11l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᑽ"):
        bstack11ll1l1l1_opy_[bstack1l11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᑾ")][bstack1l11l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᑿ")] = bstack1ll11lll1l_opy_
        bstack11ll1l1l1_opy_[bstack1l11l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒀ")][bstack1l11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᒁ")] = json.dumps(str(bstack1lll11ll_opy_))
    if type == bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒂ"):
        bstack11ll1l1l1_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ")][bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒄ")] = name
    if type == bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒅ"):
        bstack11ll1l1l1_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒆ")][bstack1l11l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᒇ")] = status
        if status == bstack1l11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒈ") and str(reason) != bstack1l11l11_opy_ (u"ࠢࠣᒉ"):
            bstack11ll1l1l1_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒊ")][bstack1l11l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᒋ")] = json.dumps(str(reason))
    bstack1l11l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᒌ").format(json.dumps(bstack11ll1l1l1_opy_))
    return bstack1l11l1ll1_opy_
def bstack1ll111l111_opy_(url, config, logger, bstack1ll1111l11_opy_=False):
    hostname = bstack1l1lll11l1_opy_(url)
    is_private = bstack1ll111lll_opy_(hostname)
    try:
        if is_private or bstack1ll1111l11_opy_:
            file_path = bstack111lll1ll1_opy_(bstack1l11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒍ"), bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒎ"), logger)
            if os.environ.get(bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᒏ")) and eval(
                    os.environ.get(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒐ"))):
                return
            if (bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᒑ") in config and not config[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᒒ")]):
                os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒓ")] = str(True)
                bstack1llll1l111l_opy_ = {bstack1l11l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᒔ"): hostname}
                bstack111lllllll_opy_(bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒕ"), bstack1l11l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᒖ"), bstack1llll1l111l_opy_, logger)
    except Exception as e:
        pass
def bstack1lllllll11_opy_(caps, bstack1llll1l1111_opy_):
    if bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒗ") in caps:
        caps[bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒘ")][bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᒙ")] = True
        if bstack1llll1l1111_opy_:
            caps[bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒚ")][bstack1l11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᒛ")] = bstack1llll1l1111_opy_
    else:
        caps[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᒜ")] = True
        if bstack1llll1l1111_opy_:
            caps[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒝ")] = bstack1llll1l1111_opy_
def bstack1lllll1l1ll_opy_(bstack1l111111ll_opy_):
    bstack1llll1l11ll_opy_ = bstack11l1lllll_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᒞ"), bstack1l11l11_opy_ (u"ࠨࠩᒟ"))
    if bstack1llll1l11ll_opy_ == bstack1l11l11_opy_ (u"ࠩࠪᒠ") or bstack1llll1l11ll_opy_ == bstack1l11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒡ"):
        threading.current_thread().testStatus = bstack1l111111ll_opy_
    else:
        if bstack1l111111ll_opy_ == bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒢ"):
            threading.current_thread().testStatus = bstack1l111111ll_opy_