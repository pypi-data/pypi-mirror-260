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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11l11_opy_
import tempfile
import json
bstack111l1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩጹ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l11l11_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ጺ"),
      datefmt=bstack1l11l11_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫጻ"),
      stream=sys.stdout
    )
  return logger
def bstack111l11l11l_opy_():
  global bstack111l1l111l_opy_
  if os.path.exists(bstack111l1l111l_opy_):
    os.remove(bstack111l1l111l_opy_)
def bstack1ll11ll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll11lllll_opy_(config, log_level):
  bstack111l1l11l1_opy_ = log_level
  if bstack1l11l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬጼ") in config:
    bstack111l1l11l1_opy_ = bstack11l1l11l11_opy_[config[bstack1l11l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ጽ")]]
  if config.get(bstack1l11l11_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧጾ"), False):
    logging.getLogger().setLevel(bstack111l1l11l1_opy_)
    return bstack111l1l11l1_opy_
  global bstack111l1l111l_opy_
  bstack1ll11ll1l_opy_()
  bstack111l11ll11_opy_ = logging.Formatter(
    fmt=bstack1l11l11_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫጿ"),
    datefmt=bstack1l11l11_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩፀ")
  )
  bstack111l111ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1l111l_opy_)
  file_handler.setFormatter(bstack111l11ll11_opy_)
  bstack111l111ll1_opy_.setFormatter(bstack111l11ll11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l111ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l11l11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪፁ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l111ll1_opy_.setLevel(bstack111l1l11l1_opy_)
  logging.getLogger().addHandler(bstack111l111ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1l11l1_opy_
def bstack111l11llll_opy_(config):
  try:
    bstack111l1l1111_opy_ = set([
      bstack1l11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫፂ"), bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ፃ"), bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧፄ"), bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩፅ"), bstack1l11l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨፆ"),
      bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪፇ"), bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫፈ"), bstack1l11l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪፉ"), bstack1l11l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫፊ")
    ])
    bstack111l111l1l_opy_ = bstack1l11l11_opy_ (u"ࠫࠬፋ")
    with open(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨፌ")) as bstack111l11lll1_opy_:
      bstack111l111lll_opy_ = bstack111l11lll1_opy_.read()
      bstack111l111l1l_opy_ = re.sub(bstack1l11l11_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧፍ"), bstack1l11l11_opy_ (u"ࠧࠨፎ"), bstack111l111lll_opy_, flags=re.M)
      bstack111l111l1l_opy_ = re.sub(
        bstack1l11l11_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫፏ") + bstack1l11l11_opy_ (u"ࠩࡿࠫፐ").join(bstack111l1l1111_opy_) + bstack1l11l11_opy_ (u"ࠪ࠭࠳࠰ࠤࠨፑ"),
        bstack1l11l11_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ፒ"),
        bstack111l111l1l_opy_, flags=re.M | re.I
      )
    def bstack111l11ll1l_opy_(dic):
      bstack111l11l111_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1l1111_opy_:
          bstack111l11l111_opy_[key] = bstack1l11l11_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩፓ")
        else:
          if isinstance(value, dict):
            bstack111l11l111_opy_[key] = bstack111l11ll1l_opy_(value)
          else:
            bstack111l11l111_opy_[key] = value
      return bstack111l11l111_opy_
    bstack111l11l111_opy_ = bstack111l11ll1l_opy_(config)
    return {
      bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩፔ"): bstack111l111l1l_opy_,
      bstack1l11l11_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪፕ"): json.dumps(bstack111l11l111_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll111l1_opy_(config):
  global bstack111l1l111l_opy_
  try:
    if config.get(bstack1l11l11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪፖ"), False):
      return
    uuid = os.getenv(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧፗ"))
    if not uuid or uuid == bstack1l11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨፘ"):
      return
    bstack111l11l1ll_opy_ = [bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧፙ"), bstack1l11l11_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭ፚ"), bstack1l11l11_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧ፛"), bstack111l1l111l_opy_]
    bstack1ll11ll1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭፜") + uuid + bstack1l11l11_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ፝"))
    with tarfile.open(output_file, bstack1l11l11_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ፞")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l11l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l11llll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l11l1l1_opy_ = data.encode()
        tarinfo.size = len(bstack111l11l1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l11l1l1_opy_))
    bstack1l1l111ll1_opy_ = MultipartEncoder(
      fields= {
        bstack1l11l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ፟"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l11l11_opy_ (u"ࠫࡷࡨࠧ፠")), bstack1l11l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪ፡")),
        bstack1l11l11_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ።"): uuid
      }
    )
    response = requests.post(
      bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤ፣"),
      data=bstack1l1l111ll1_opy_,
      headers={bstack1l11l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ፤"): bstack1l1l111ll1_opy_.content_type},
      auth=(config[bstack1l11l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ፥")], config[bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭፦")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l11l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪ፧") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l11l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ፨") + str(e))
  finally:
    try:
      bstack111l11l11l_opy_()
    except:
      pass