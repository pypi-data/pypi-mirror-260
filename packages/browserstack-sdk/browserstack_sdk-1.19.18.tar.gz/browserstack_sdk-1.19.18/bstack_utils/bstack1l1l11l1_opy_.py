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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11lll1l_opy_, bstack1111l1l1_opy_, bstack1l11ll1ll_opy_, bstack1l1l11l11_opy_, \
    bstack11l11l1l1l_opy_
def bstack1l111lll_opy_(bstack1llll1lll1l_opy_):
    for driver in bstack1llll1lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllllll1_opy_(driver, status, reason=bstack1l1l1_opy_ (u"ࠩࠪᑯ")):
    bstack11l11111_opy_ = Config.bstack1llllllll_opy_()
    if bstack11l11111_opy_.bstack11lll11111_opy_():
        return
    bstack1l1l111lll_opy_ = bstack1l11l1l11_opy_(bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑰ"), bstack1l1l1_opy_ (u"ࠫࠬᑱ"), status, reason, bstack1l1l1_opy_ (u"ࠬ࠭ᑲ"), bstack1l1l1_opy_ (u"࠭ࠧᑳ"))
    driver.execute_script(bstack1l1l111lll_opy_)
def bstack11l11l11_opy_(page, status, reason=bstack1l1l1_opy_ (u"ࠧࠨᑴ")):
    try:
        if page is None:
            return
        bstack11l11111_opy_ = Config.bstack1llllllll_opy_()
        if bstack11l11111_opy_.bstack11lll11111_opy_():
            return
        bstack1l1l111lll_opy_ = bstack1l11l1l11_opy_(bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᑵ"), bstack1l1l1_opy_ (u"ࠩࠪᑶ"), status, reason, bstack1l1l1_opy_ (u"ࠪࠫᑷ"), bstack1l1l1_opy_ (u"ࠫࠬᑸ"))
        page.evaluate(bstack1l1l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᑹ"), bstack1l1l111lll_opy_)
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᑺ"), e)
def bstack1l11l1l11_opy_(type, name, status, reason, bstack1l1l111l1_opy_, bstack111111l1_opy_):
    bstack1llll111ll_opy_ = {
        bstack1l1l1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᑻ"): type,
        bstack1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᑼ"): {}
    }
    if type == bstack1l1l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᑽ"):
        bstack1llll111ll_opy_[bstack1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᑾ")][bstack1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᑿ")] = bstack1l1l111l1_opy_
        bstack1llll111ll_opy_[bstack1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒀ")][bstack1l1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᒁ")] = json.dumps(str(bstack111111l1_opy_))
    if type == bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒂ"):
        bstack1llll111ll_opy_[bstack1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ")][bstack1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒄ")] = name
    if type == bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒅ"):
        bstack1llll111ll_opy_[bstack1l1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒆ")][bstack1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᒇ")] = status
        if status == bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒈ") and str(reason) != bstack1l1l1_opy_ (u"ࠢࠣᒉ"):
            bstack1llll111ll_opy_[bstack1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒊ")][bstack1l1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᒋ")] = json.dumps(str(reason))
    bstack1l1l111l1l_opy_ = bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᒌ").format(json.dumps(bstack1llll111ll_opy_))
    return bstack1l1l111l1l_opy_
def bstack1l1lll1ll_opy_(url, config, logger, bstack1l1l11111l_opy_=False):
    hostname = bstack1111l1l1_opy_(url)
    is_private = bstack1l1l11l11_opy_(hostname)
    try:
        if is_private or bstack1l1l11111l_opy_:
            file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒍ"), bstack1l1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒎ"), logger)
            if os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᒏ")) and eval(
                    os.environ.get(bstack1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒐ"))):
                return
            if (bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᒑ") in config and not config[bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᒒ")]):
                os.environ[bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒓ")] = str(True)
                bstack1llll1lll11_opy_ = {bstack1l1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᒔ"): hostname}
                bstack11l11l1l1l_opy_(bstack1l1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒕ"), bstack1l1l1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᒖ"), bstack1llll1lll11_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1ll1ll1_opy_(caps, bstack1llll1ll1ll_opy_):
    if bstack1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒗ") in caps:
        caps[bstack1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒘ")][bstack1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᒙ")] = True
        if bstack1llll1ll1ll_opy_:
            caps[bstack1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒚ")][bstack1l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᒛ")] = bstack1llll1ll1ll_opy_
    else:
        caps[bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᒜ")] = True
        if bstack1llll1ll1ll_opy_:
            caps[bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒝ")] = bstack1llll1ll1ll_opy_
def bstack1lllllll111_opy_(bstack11lll1ll11_opy_):
    bstack1llll1llll1_opy_ = bstack1l11ll1ll_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᒞ"), bstack1l1l1_opy_ (u"ࠨࠩᒟ"))
    if bstack1llll1llll1_opy_ == bstack1l1l1_opy_ (u"ࠩࠪᒠ") or bstack1llll1llll1_opy_ == bstack1l1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒡ"):
        threading.current_thread().testStatus = bstack11lll1ll11_opy_
    else:
        if bstack11lll1ll11_opy_ == bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒢ"):
            threading.current_thread().testStatus = bstack11lll1ll11_opy_