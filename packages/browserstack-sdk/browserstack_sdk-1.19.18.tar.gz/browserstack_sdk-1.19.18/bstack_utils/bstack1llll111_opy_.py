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
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11l1llllll_opy_ as bstack11l1lll111_opy_
from bstack_utils.bstack11111111_opy_ import bstack11111111_opy_
from bstack_utils.helper import bstack1lll1l1ll1_opy_, bstack1l1l1lll1l_opy_, bstack11ll11111l_opy_, bstack11ll1l1111_opy_, bstack11llll11_opy_, get_host_info, bstack11ll1111l1_opy_, bstack1l1lll11ll_opy_, bstack1l1111l1ll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1111l1ll_opy_(class_method=False)
def _11ll11l111_opy_(driver, bstack1l11l1l1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1l1_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪฬ"): caps.get(bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩอ"), None),
        bstack1l1l1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨฮ"): bstack1l11l1l1l_opy_.get(bstack1l1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨฯ"), None),
        bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬะ"): caps.get(bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬั"), None),
        bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪา"): caps.get(bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪำ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧิ") + str(error))
  return response
def bstack1llll1l1ll_opy_(config):
  return config.get(bstack1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫี"), False) or any([p.get(bstack1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬึ"), False) == True for p in config.get(bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩื"), [])])
def bstack11l11l1l_opy_(config, bstack1l1l1111_opy_):
  try:
    if not bstack1l1l1lll1l_opy_(config):
      return False
    bstack11ll11l11l_opy_ = config.get(bstack1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿุࠧ"), False)
    bstack11ll111l1l_opy_ = config[bstack1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶูࠫ")][bstack1l1l1111_opy_].get(bstack1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺฺࠩ"), None)
    if bstack11ll111l1l_opy_ != None:
      bstack11ll11l11l_opy_ = bstack11ll111l1l_opy_
    bstack11ll111111_opy_ = os.getenv(bstack1l1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ฻")) is not None and len(os.getenv(bstack1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ฼"))) > 0 and os.getenv(bstack1l1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ฽")) != bstack1l1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ฾")
    return bstack11ll11l11l_opy_ and bstack11ll111111_opy_
  except Exception as error:
    logger.debug(bstack1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧ฿") + str(error))
  return False
def bstack1l111111l_opy_(bstack11ll1111ll_opy_, test_tags):
  bstack11ll1111ll_opy_ = os.getenv(bstack1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩเ"))
  if bstack11ll1111ll_opy_ is None:
    return True
  bstack11ll1111ll_opy_ = json.loads(bstack11ll1111ll_opy_)
  try:
    include_tags = bstack11ll1111ll_opy_[bstack1l1l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧแ")] if bstack1l1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨโ") in bstack11ll1111ll_opy_ and isinstance(bstack11ll1111ll_opy_[bstack1l1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩใ")], list) else []
    exclude_tags = bstack11ll1111ll_opy_[bstack1l1l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪไ")] if bstack1l1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫๅ") in bstack11ll1111ll_opy_ and isinstance(bstack11ll1111ll_opy_[bstack1l1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬๆ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣ็") + str(error))
  return False
def bstack1lll11llll_opy_(config, bstack11ll11ll11_opy_, bstack11l1lll11l_opy_, bstack11ll111l11_opy_):
  bstack11ll1l11l1_opy_ = bstack11ll11111l_opy_(config)
  bstack11l1lll1ll_opy_ = bstack11ll1l1111_opy_(config)
  if bstack11ll1l11l1_opy_ is None or bstack11l1lll1ll_opy_ is None:
    logger.error(bstack1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰ่ࠪ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏ้ࠫ"), bstack1l1l1_opy_ (u"ࠫࢀࢃ๊ࠧ")))
    data = {
        bstack1l1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧ๋ࠪ"): config[bstack1l1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ์")],
        bstack1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪํ"): config.get(bstack1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๎"), os.path.basename(os.getcwd())),
        bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬ๏"): bstack1lll1l1ll1_opy_(),
        bstack1l1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ๐"): config.get(bstack1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ๑"), bstack1l1l1_opy_ (u"ࠬ࠭๒")),
        bstack1l1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭๓"): {
            bstack1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ๔"): bstack11ll11ll11_opy_,
            bstack1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ๕"): bstack11l1lll11l_opy_,
            bstack1l1l1_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๖"): __version__,
            bstack1l1l1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ๗"): bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ๘"),
            bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ๙"): bstack1l1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ๚"),
            bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ๛"): bstack11ll111l11_opy_
        },
        bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ๜"): settings,
        bstack1l1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ๝"): bstack11ll1111l1_opy_(),
        bstack1l1l1_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ๞"): bstack11llll11_opy_(),
        bstack1l1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭๟"): get_host_info(),
        bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ๠"): bstack1l1l1lll1l_opy_(config)
    }
    headers = {
        bstack1l1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ๡"): bstack1l1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ๢"),
    }
    config = {
        bstack1l1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭๣"): (bstack11ll1l11l1_opy_, bstack11l1lll1ll_opy_),
        bstack1l1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ๤"): headers
    }
    response = bstack1l1lll11ll_opy_(bstack1l1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ๥"), bstack11l1lll111_opy_ + bstack1l1l1_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫ๦"), data, config)
    bstack11ll11llll_opy_ = response.json()
    if bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭๧")]:
      parsed = json.loads(os.getenv(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ๨"), bstack1l1l1_opy_ (u"ࠧࡼࡿࠪ๩")))
      parsed[bstack1l1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๪")] = bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧ๫")][bstack1l1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๬")]
      os.environ[bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๭")] = json.dumps(parsed)
      bstack11111111_opy_.bstack11l1lllll1_opy_(bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪ๮")][bstack1l1l1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ๯")])
      bstack11111111_opy_.bstack11ll111ll1_opy_(bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬ๰")][bstack1l1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ๱")])
      bstack11111111_opy_.store()
      return bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧ๲")][bstack1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ๳")], bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩ๴")][bstack1l1l1_opy_ (u"ࠬ࡯ࡤࠨ๵")]
    else:
      logger.error(bstack1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧ๶") + bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๷")])
      if bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๸")] == bstack1l1l1_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫ๹"):
        for bstack11ll11lll1_opy_ in bstack11ll11llll_opy_[bstack1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ๺")]:
          logger.error(bstack11ll11lll1_opy_[bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ๻")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨ๼") +  str(error))
    return None, None
def bstack1l1ll1l11_opy_():
  if os.getenv(bstack1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ๽")) is None:
    return {
        bstack1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ๾"): bstack1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ๿"),
        bstack1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ຀"): bstack1l1l1_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩກ")
    }
  data = {bstack1l1l1_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬຂ"): bstack1lll1l1ll1_opy_()}
  headers = {
      bstack1l1l1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ຃"): bstack1l1l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧຄ") + os.getenv(bstack1l1l1_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧ຅")),
      bstack1l1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧຆ"): bstack1l1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬງ")
  }
  response = bstack1l1lll11ll_opy_(bstack1l1l1_opy_ (u"ࠪࡔ࡚࡚ࠧຈ"), bstack11l1lll111_opy_ + bstack1l1l1_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ຉ"), data, { bstack1l1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ຊ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢ຋") + datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"࡛ࠧࠩຌ"))
      return {bstack1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨຍ"): bstack1l1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪຎ"), bstack1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຏ"): bstack1l1l1_opy_ (u"ࠫࠬຐ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣຑ") + str(error))
    return {
        bstack1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ຒ"): bstack1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ຓ"),
        bstack1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩດ"): str(error)
    }
def bstack1l1l11llll_opy_(caps, options):
  try:
    bstack11l1llll11_opy_ = caps.get(bstack1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪຕ"), {}).get(bstack1l1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧຖ"), caps.get(bstack1l1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫທ"), bstack1l1l1_opy_ (u"ࠬ࠭ຘ")))
    if bstack11l1llll11_opy_:
      logger.warn(bstack1l1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥນ"))
      return False
    browser = caps.get(bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬບ"), bstack1l1l1_opy_ (u"ࠨࠩປ")).lower()
    if browser != bstack1l1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩຜ"):
      logger.warn(bstack1l1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨຝ"))
      return False
    browser_version = caps.get(bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬພ"), caps.get(bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧຟ")))
    if browser_version and browser_version != bstack1l1l1_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ຠ") and int(browser_version.split(bstack1l1l1_opy_ (u"ࠧ࠯ࠩມ"))[0]) <= 94:
      logger.warn(bstack1l1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠸࠳ࠨຢ"))
      return False
    if not options is None:
      bstack11l1lll1l1_opy_ = options.to_capabilities().get(bstack1l1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧຣ"), {})
      if bstack1l1l1_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ຤") in bstack11l1lll1l1_opy_.get(bstack1l1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩລ"), []):
        logger.warn(bstack1l1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ຦"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣວ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1ll1lll_opy_ = config.get(bstack1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧຨ"), {})
    bstack11l1ll1lll_opy_[bstack1l1l1_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫຩ")] = os.getenv(bstack1l1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧສ"))
    bstack11ll11l1l1_opy_ = json.loads(os.getenv(bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫຫ"), bstack1l1l1_opy_ (u"ࠫࢀࢃࠧຬ"))).get(bstack1l1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ອ"))
    caps[bstack1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ຮ")] = True
    if bstack1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨຯ") in caps:
      caps[bstack1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩະ")][bstack1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩັ")] = bstack11l1ll1lll_opy_
      caps[bstack1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫາ")][bstack1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫຳ")][bstack1l1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ິ")] = bstack11ll11l1l1_opy_
    else:
      caps[bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬີ")] = bstack11l1ll1lll_opy_
      caps[bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຶ")][bstack1l1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩື")] = bstack11ll11l1l1_opy_
  except Exception as error:
    logger.debug(bstack1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ຸࠢࠥ") +  str(error))
def bstack1111111ll_opy_(driver, bstack11ll111lll_opy_):
  try:
    setattr(driver, bstack1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰູࠪ"), True)
    session = driver.session_id
    if session:
      bstack11ll11ll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll11ll1l_opy_ = False
      bstack11ll11ll1l_opy_ = url.scheme in [bstack1l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ຺"), bstack1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦົ")]
      if bstack11ll11ll1l_opy_:
        if bstack11ll111lll_opy_:
          logger.info(bstack1l1l1_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨຼ"))
      return bstack11ll111lll_opy_
  except Exception as e:
    logger.error(bstack1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥຽ") + str(e))
    return False
def bstack11llll11l_opy_(driver, class_name, name, module_name, path, bstack1l11l1l1l_opy_):
  try:
    bstack11ll1ll11l_opy_ = [class_name] if not class_name is None else []
    bstack11l1llll1l_opy_ = {
        bstack1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨ຾"): True,
        bstack1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࡄࡦࡶࡤ࡭ࡱࡹࠢ຿"): {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣເ"): name,
            bstack1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡔࡸࡲࡎࡪࠢແ"): os.environ.get(bstack1l1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡗ࡛ࡎࡠࡋࡇࠫໂ")),
            bstack1l1l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡔࡦࡺࡨࠣໃ"): str(path),
            bstack1l1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࡒࡩࡴࡶࠥໄ"): [module_name, *bstack11ll1ll11l_opy_, name],
        },
        bstack1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ໅"): _11ll11l111_opy_(driver, bstack1l11l1l1l_opy_)
    }
    logger.debug(bstack1l1l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬໆ"))
    logger.debug(driver.execute_async_script(bstack11111111_opy_.perform_scan, {bstack1l1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥ໇"): name}))
    logger.debug(driver.execute_async_script(bstack11111111_opy_.bstack11ll11l1ll_opy_, bstack11l1llll1l_opy_))
    logger.info(bstack1l1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴່ࠢ"))
  except Exception as bstack11ll1l111l_opy_:
    logger.error(bstack1l1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿້ࠦࠢ") + str(path) + bstack1l1l1_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺໊ࠣ") + str(bstack11ll1l111l_opy_))