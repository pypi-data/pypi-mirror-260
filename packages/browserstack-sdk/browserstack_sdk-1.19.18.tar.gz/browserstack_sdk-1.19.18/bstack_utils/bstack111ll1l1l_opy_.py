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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1111l1_opy_, bstack11llll11_opy_, get_host_info, bstack11ll11111l_opy_, bstack11ll1l1111_opy_, bstack111lll1l1l_opy_, \
    bstack111lll1l11_opy_, bstack11l11lllll_opy_, bstack1l1lll11ll_opy_, bstack11l11ll1l1_opy_, bstack111l11l1l_opy_, bstack1l1111l1ll_opy_
from bstack_utils.bstack1lllll1lll1_opy_ import bstack1lllll11l1l_opy_
from bstack_utils.bstack11llllll1l_opy_ import bstack1l11l1111l_opy_
import bstack_utils.bstack1llll111_opy_ as bstack1l11lllll_opy_
from bstack_utils.constants import bstack11l1l111ll_opy_
bstack1llll1111l1_opy_ = [
    bstack1l1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᓡ"), bstack1l1l1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᓢ"), bstack1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓣ"), bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᓤ"),
    bstack1l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓥ"), bstack1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᓦ"), bstack1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᓧ")
]
bstack1lll1llllll_opy_ = bstack1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᓨ")
logger = logging.getLogger(__name__)
class bstack1ll1l1l1l1_opy_:
    bstack1lllll1lll1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llll111lll_opy_):
        cls.bs_config = bs_config
        cls.bstack1llll11111l_opy_()
        bstack11ll1l11l1_opy_ = bstack11ll11111l_opy_(bs_config)
        bstack11l1lll1ll_opy_ = bstack11ll1l1111_opy_(bs_config)
        bstack1l1ll1l1_opy_ = False
        bstack1ll11l1l1l_opy_ = False
        if bstack1l1l1_opy_ (u"ࠬࡧࡰࡱࠩᓩ") in bs_config:
            bstack1l1ll1l1_opy_ = True
        else:
            bstack1ll11l1l1l_opy_ = True
        bstack1111lll1_opy_ = {
            bstack1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᓪ"): cls.bstack1l1l111l_opy_() and cls.bstack1llll111111_opy_(bstack1llll111lll_opy_.get(bstack1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᓫ"), bstack1l1l1_opy_ (u"ࠨࠩᓬ"))),
            bstack1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᓭ"): bstack1l11lllll_opy_.bstack1llll1l1ll_opy_(bs_config),
            bstack1l1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᓮ"): bs_config.get(bstack1l1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᓯ"), False),
            bstack1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᓰ"): bstack1ll11l1l1l_opy_,
            bstack1l1l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᓱ"): bstack1l1ll1l1_opy_
        }
        data = {
            bstack1l1l1_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᓲ"): bstack1l1l1_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᓳ"),
            bstack1l1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᓴ"): bs_config.get(bstack1l1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᓵ"), bstack1l1l1_opy_ (u"ࠫࠬᓶ")),
            bstack1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓷ"): bs_config.get(bstack1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᓸ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᓹ"): bs_config.get(bstack1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᓺ")),
            bstack1l1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᓻ"): bs_config.get(bstack1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᓼ"), bstack1l1l1_opy_ (u"ࠫࠬᓽ")),
            bstack1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡣࡹ࡯࡭ࡦࠩᓾ"): datetime.datetime.now().isoformat(),
            bstack1l1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫᓿ"): bstack111lll1l1l_opy_(bs_config),
            bstack1l1l1_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪᔀ"): get_host_info(),
            bstack1l1l1_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩᔁ"): bstack11llll11_opy_(),
            bstack1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᔂ"): os.environ.get(bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᔃ")),
            bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᔄ"): os.environ.get(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᔅ"), False),
            bstack1l1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᔆ"): bstack11ll1111l1_opy_(),
            bstack1l1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᔇ"): bstack1111lll1_opy_,
            bstack1l1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᔈ"): {
                bstack1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᔉ"): bstack1llll111lll_opy_.get(bstack1l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫᔊ"), bstack1l1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᔋ")),
                bstack1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔌ"): bstack1llll111lll_opy_.get(bstack1l1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᔍ")),
                bstack1l1l1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᔎ"): bstack1llll111lll_opy_.get(bstack1l1l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔏ"))
            }
        }
        config = {
            bstack1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᔐ"): (bstack11ll1l11l1_opy_, bstack11l1lll1ll_opy_),
            bstack1l1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᔑ"): cls.default_headers()
        }
        response = bstack1l1lll11ll_opy_(bstack1l1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩᔒ"), cls.request_url(bstack1l1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷࠬᔓ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔔ")] = bstack1l1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᔕ")
            os.environ[bstack1l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᔖ")] = bstack1l1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᔗ")
            os.environ[bstack1l1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᔘ")] = bstack1l1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᔙ")
            os.environ[bstack1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᔚ")] = bstack1l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔛ")
            os.environ[bstack1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᔜ")] = bstack1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᔝ")
            bstack1lll1llll11_opy_ = response.json()
            if bstack1lll1llll11_opy_ and bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔞ")]:
                error_message = bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔟ")]
                if bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᔠ")] == bstack1l1l1_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡎࡔࡖࡂࡎࡌࡈࡤࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࠪᔡ"):
                    logger.error(error_message)
                elif bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔢ")] == bstack1l1l1_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉ࠭ᔣ"):
                    logger.info(error_message)
                elif bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᔤ")] == bstack1l1l1_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡕࡇࡏࡤࡊࡅࡑࡔࡈࡇࡆ࡚ࡅࡅࠩᔥ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᔦ"))
            return [None, None, None]
        bstack1lll1llll11_opy_ = response.json()
        os.environ[bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᔧ")] = bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᔨ")]
        if cls.bstack1l1l111l_opy_() is True and cls.bstack1llll111111_opy_(bstack1llll111lll_opy_.get(bstack1l1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧᔩ"), bstack1l1l1_opy_ (u"ࠧࠨᔪ"))):
            logger.debug(bstack1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬᔫ"))
            os.environ[bstack1l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᔬ")] = bstack1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᔭ")
            if bstack1lll1llll11_opy_.get(bstack1l1l1_opy_ (u"ࠫ࡯ࡽࡴࠨᔮ")):
                os.environ[bstack1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔯ")] = bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"࠭ࡪࡸࡶࠪᔰ")]
                os.environ[bstack1l1l1_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫᔱ")] = json.dumps({
                    bstack1l1l1_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪᔲ"): bstack11ll1l11l1_opy_,
                    bstack1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫᔳ"): bstack11l1lll1ll_opy_
                })
            if bstack1lll1llll11_opy_.get(bstack1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᔴ")):
                os.environ[bstack1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᔵ")] = bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᔶ")]
            if bstack1lll1llll11_opy_.get(bstack1l1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᔷ")):
                os.environ[bstack1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᔸ")] = str(bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᔹ")])
        return [bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭ᔺ")], bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᔻ")], bstack1lll1llll11_opy_[bstack1l1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᔼ")]]
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔽ")] == bstack1l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔾ") or os.environ[bstack1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᔿ")] == bstack1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᕀ"):
            print(bstack1l1l1_opy_ (u"ࠩࡈ࡜ࡈࡋࡐࡕࡋࡒࡒࠥࡏࡎࠡࡵࡷࡳࡵࡈࡵࡪ࡮ࡧ࡙ࡵࡹࡴࡳࡧࡤࡱࠥࡘࡅࡒࡗࡈࡗ࡙ࠦࡔࡐࠢࡗࡉࡘ࡚ࠠࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟ࠠ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᕁ"))
            return {
                bstack1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᕂ"): bstack1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᕃ"),
                bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕄ"): bstack1l1l1_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᕅ")
            }
        else:
            cls.bstack1lllll1lll1_opy_.shutdown()
            data = {
                bstack1l1l1_opy_ (u"ࠧࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࠪᕆ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1l1l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᕇ"): cls.default_headers()
            }
            bstack11l11l11l1_opy_ = bstack1l1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪᕈ").format(os.environ[bstack1l1l1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᕉ")])
            bstack1lll1ll1l1l_opy_ = cls.request_url(bstack11l11l11l1_opy_)
            response = bstack1l1lll11ll_opy_(bstack1l1l1_opy_ (u"ࠫࡕ࡛ࡔࠨᕊ"), bstack1lll1ll1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l1_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᕋ"))
    @classmethod
    def bstack11lllll11l_opy_(cls):
        if cls.bstack1lllll1lll1_opy_ is None:
            return
        cls.bstack1lllll1lll1_opy_.shutdown()
    @classmethod
    def bstack11111lll1_opy_(cls):
        if cls.on():
            print(
                bstack1l1l1_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᕌ").format(os.environ[bstack1l1l1_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᕍ")]))
    @classmethod
    def bstack1llll11111l_opy_(cls):
        if cls.bstack1lllll1lll1_opy_ is not None:
            return
        cls.bstack1lllll1lll1_opy_ = bstack1lllll11l1l_opy_(cls.bstack1lll1lll111_opy_)
        cls.bstack1lllll1lll1_opy_.start()
    @classmethod
    def bstack1l111ll1l1_opy_(cls, bstack1l111l1l1l_opy_, bstack1llll111l11_opy_=bstack1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᕎ")):
        if not cls.on():
            return
        bstack1lll1ll111_opy_ = bstack1l111l1l1l_opy_[bstack1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᕏ")]
        bstack1lll1lllll1_opy_ = {
            bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᕐ"): bstack1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᕑ"),
            bstack1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᕒ"): bstack1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᕓ"),
            bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᕔ"): bstack1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓ࡬࡫ࡳࡴࡪࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕕ"),
            bstack1l1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᕖ"): bstack1l1l1_opy_ (u"ࠪࡐࡴ࡭࡟ࡖࡲ࡯ࡳࡦࡪࠧᕗ"),
            bstack1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕘ"): bstack1l1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᕙ"),
            bstack1l1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᕚ"): bstack1l1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᕛ"),
            bstack1l1l1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᕜ"): bstack1l1l1_opy_ (u"ࠩࡆࡆ࡙ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕝ")
        }.get(bstack1lll1ll111_opy_)
        if bstack1llll111l11_opy_ == bstack1l1l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᕞ"):
            cls.bstack1llll11111l_opy_()
            cls.bstack1lllll1lll1_opy_.add(bstack1l111l1l1l_opy_)
        elif bstack1llll111l11_opy_ == bstack1l1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᕟ"):
            cls.bstack1lll1lll111_opy_([bstack1l111l1l1l_opy_], bstack1llll111l11_opy_)
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def bstack1lll1lll111_opy_(cls, bstack1l111l1l1l_opy_, bstack1llll111l11_opy_=bstack1l1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᕠ")):
        config = {
            bstack1l1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕡ"): cls.default_headers()
        }
        response = bstack1l1lll11ll_opy_(bstack1l1l1_opy_ (u"ࠧࡑࡑࡖࡘࠬᕢ"), cls.request_url(bstack1llll111l11_opy_), bstack1l111l1l1l_opy_, config)
        bstack11ll11llll_opy_ = response.json()
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def bstack111lllll1_opy_(cls, bstack1l111l1l11_opy_):
        bstack1lll1lll1ll_opy_ = []
        for log in bstack1l111l1l11_opy_:
            bstack1llll111l1l_opy_ = {
                bstack1l1l1_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᕣ"): bstack1l1l1_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫᕤ"),
                bstack1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᕥ"): log[bstack1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᕦ")],
                bstack1l1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᕧ"): log[bstack1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᕨ")],
                bstack1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧᕩ"): {},
                bstack1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᕪ"): log[bstack1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᕫ")],
            }
            if bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕬ") in log:
                bstack1llll111l1l_opy_[bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕭ")] = log[bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕮ")]
            elif bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕯ") in log:
                bstack1llll111l1l_opy_[bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕰ")] = log[bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕱ")]
            bstack1lll1lll1ll_opy_.append(bstack1llll111l1l_opy_)
        cls.bstack1l111ll1l1_opy_({
            bstack1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᕲ"): bstack1l1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᕳ"),
            bstack1l1l1_opy_ (u"ࠫࡱࡵࡧࡴࠩᕴ"): bstack1lll1lll1ll_opy_
        })
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def bstack1lll1ll1ll1_opy_(cls, steps):
        bstack1lll1lll11l_opy_ = []
        for step in steps:
            bstack1lll1lll1l1_opy_ = {
                bstack1l1l1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᕵ"): bstack1l1l1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩᕶ"),
                bstack1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕷ"): step[bstack1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕸ")],
                bstack1l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᕹ"): step[bstack1l1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕺ")],
                bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᕻ"): step[bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕼ")],
                bstack1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᕽ"): step[bstack1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᕾ")]
            }
            if bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕿ") in step:
                bstack1lll1lll1l1_opy_[bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖀ")] = step[bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖁ")]
            elif bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖂ") in step:
                bstack1lll1lll1l1_opy_[bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖃ")] = step[bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖄ")]
            bstack1lll1lll11l_opy_.append(bstack1lll1lll1l1_opy_)
        cls.bstack1l111ll1l1_opy_({
            bstack1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖅ"): bstack1l1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖆ"),
            bstack1l1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖇ"): bstack1lll1lll11l_opy_
        })
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def bstack1l1l111l11_opy_(cls, screenshot):
        cls.bstack1l111ll1l1_opy_({
            bstack1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᖈ"): bstack1l1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᖉ"),
            bstack1l1l1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᖊ"): [{
                bstack1l1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫᖋ"): bstack1l1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩᖌ"),
                bstack1l1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᖍ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫᖎ"),
                bstack1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖏ"): screenshot[bstack1l1l1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᖐ")],
                bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖑ"): screenshot[bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖒ")]
            }]
        }, bstack1llll111l11_opy_=bstack1l1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᖓ"))
    @classmethod
    @bstack1l1111l1ll_opy_(class_method=True)
    def bstack11l1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111ll1l1_opy_({
            bstack1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖔ"): bstack1l1l1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᖕ"),
            bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᖖ"): {
                bstack1l1l1_opy_ (u"ࠦࡺࡻࡩࡥࠤᖗ"): cls.current_test_uuid(),
                bstack1l1l1_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦᖘ"): cls.bstack1l1111ll11_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᖙ"), None) is None or os.environ[bstack1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᖚ")] == bstack1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᖛ"):
            return False
        return True
    @classmethod
    def bstack1l1l111l_opy_(cls):
        return bstack111l11l1l_opy_(cls.bs_config.get(bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᖜ"), False))
    @classmethod
    def bstack1llll111111_opy_(cls, framework):
        return framework in bstack11l1l111ll_opy_
    @staticmethod
    def request_url(url):
        return bstack1l1l1_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᖝ").format(bstack1lll1llllll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᖞ"): bstack1l1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᖟ"),
            bstack1l1l1_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᖠ"): bstack1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬᖡ")
        }
        if os.environ.get(bstack1l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᖢ"), None):
            headers[bstack1l1l1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖣ")] = bstack1l1l1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᖤ").format(os.environ[bstack1l1l1_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠧᖥ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖦ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖧ"), None)
    @staticmethod
    def bstack1l111l11ll_opy_():
        if getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᖨ"), None):
            return {
                bstack1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖩ"): bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧᖪ"),
                bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖫ"): getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖬ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖭ"), None):
            return {
                bstack1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᖮ"): bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᖯ"),
                bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖰ"): getattr(threading.current_thread(), bstack1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᖱ"), None)
            }
        return None
    @staticmethod
    def bstack1l1111ll11_opy_(driver):
        return {
            bstack11l11lllll_opy_(): bstack111lll1l11_opy_(driver)
        }
    @staticmethod
    def bstack1lll1ll1lll_opy_(exception_info, report):
        return [{bstack1l1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᖲ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l1ll1_opy_(typename):
        if bstack1l1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᖳ") in typename:
            return bstack1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᖴ")
        return bstack1l1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᖵ")
    @staticmethod
    def bstack1llll111ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l1l1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l11111_opy_(test, hook_name=None):
        bstack1llll1111ll_opy_ = test.parent
        if hook_name in [bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᖶ"), bstack1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᖷ"), bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᖸ"), bstack1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᖹ")]:
            bstack1llll1111ll_opy_ = test
        scope = []
        while bstack1llll1111ll_opy_ is not None:
            scope.append(bstack1llll1111ll_opy_.name)
            bstack1llll1111ll_opy_ = bstack1llll1111ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1llll1l_opy_(hook_type):
        if hook_type == bstack1l1l1_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤᖺ"):
            return bstack1l1l1_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤᖻ")
        elif hook_type == bstack1l1l1_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥᖼ"):
            return bstack1l1l1_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢᖽ")
    @staticmethod
    def bstack1lll1ll1l11_opy_(bstack1l11ll111_opy_):
        try:
            if not bstack1ll1l1l1l1_opy_.on():
                return bstack1l11ll111_opy_
            if os.environ.get(bstack1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨᖾ"), None) == bstack1l1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᖿ"):
                tests = os.environ.get(bstack1l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢᗀ"), None)
                if tests is None or tests == bstack1l1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᗁ"):
                    return bstack1l11ll111_opy_
                bstack1l11ll111_opy_ = tests.split(bstack1l1l1_opy_ (u"ࠬ࠲ࠧᗂ"))
                return bstack1l11ll111_opy_
        except Exception as exc:
            print(bstack1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢᗃ"), str(exc))
        return bstack1l11ll111_opy_
    @classmethod
    def bstack1l11111lll_opy_(cls, event: str, bstack1l111l1l1l_opy_: bstack1l11l1111l_opy_):
        bstack1l111l1111_opy_ = {
            bstack1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᗄ"): event,
            bstack1l111l1l1l_opy_.bstack1l111l111l_opy_(): bstack1l111l1l1l_opy_.bstack1l11111111_opy_(event)
        }
        bstack1ll1l1l1l1_opy_.bstack1l111ll1l1_opy_(bstack1l111l1111_opy_)