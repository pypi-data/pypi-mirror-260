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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l11l11l_opy_, bstack11ll1ll1l_opy_
class bstack1l1lll1ll_opy_:
  working_dir = os.getcwd()
  bstack1l11ll11ll_opy_ = False
  config = {}
  binary_path = bstack1l11l11_opy_ (u"ࠧࠨᎰ")
  bstack111111ll11_opy_ = bstack1l11l11_opy_ (u"ࠨࠩᎱ")
  bstack11l1l111l_opy_ = False
  bstack1111ll1111_opy_ = None
  bstack1111lll11l_opy_ = {}
  bstack1111l1ll1l_opy_ = 300
  bstack11111l1ll1_opy_ = False
  logger = None
  bstack1111l1l1ll_opy_ = False
  bstack1111l1ll11_opy_ = bstack1l11l11_opy_ (u"ࠩࠪᎲ")
  bstack1111l1l111_opy_ = {
    bstack1l11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᎳ") : 1,
    bstack1l11l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᎴ") : 2,
    bstack1l11l11_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᎵ") : 3,
    bstack1l11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭Ꮆ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111lll11_opy_(self):
    bstack1111l1111l_opy_ = bstack1l11l11_opy_ (u"ࠧࠨᎷ")
    bstack1111l11111_opy_ = sys.platform
    bstack11111lllll_opy_ = bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᎸ")
    if re.match(bstack1l11l11_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᎹ"), bstack1111l11111_opy_) != None:
      bstack1111l1111l_opy_ = bstack11l11llll1_opy_ + bstack1l11l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᎺ")
      self.bstack1111l1ll11_opy_ = bstack1l11l11_opy_ (u"ࠫࡲࡧࡣࠨᎻ")
    elif re.match(bstack1l11l11_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᎼ"), bstack1111l11111_opy_) != None:
      bstack1111l1111l_opy_ = bstack11l11llll1_opy_ + bstack1l11l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᎽ")
      bstack11111lllll_opy_ = bstack1l11l11_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᎾ")
      self.bstack1111l1ll11_opy_ = bstack1l11l11_opy_ (u"ࠨࡹ࡬ࡲࠬᎿ")
    else:
      bstack1111l1111l_opy_ = bstack11l11llll1_opy_ + bstack1l11l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᏀ")
      self.bstack1111l1ll11_opy_ = bstack1l11l11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᏁ")
    return bstack1111l1111l_opy_, bstack11111lllll_opy_
  def bstack1111l11l11_opy_(self):
    try:
      bstack11111ll111_opy_ = [os.path.join(expanduser(bstack1l11l11_opy_ (u"ࠦࢃࠨᏂ")), bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᏃ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11111ll111_opy_:
        if(self.bstack1111l1lll1_opy_(path)):
          return path
      raise bstack1l11l11_opy_ (u"ࠨࡕ࡯ࡣ࡯ࡦࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᏄ")
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤᏅ").format(e))
  def bstack1111l1lll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111ll11l1_opy_(self, bstack1111l1111l_opy_, bstack11111lllll_opy_):
    try:
      bstack11111l111l_opy_ = self.bstack1111l11l11_opy_()
      bstack1111lll111_opy_ = os.path.join(bstack11111l111l_opy_, bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫᏆ"))
      bstack11111l1111_opy_ = os.path.join(bstack11111l111l_opy_, bstack11111lllll_opy_)
      if os.path.exists(bstack11111l1111_opy_):
        self.logger.info(bstack1l11l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᏇ").format(bstack11111l1111_opy_))
        return bstack11111l1111_opy_
      if os.path.exists(bstack1111lll111_opy_):
        self.logger.info(bstack1l11l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣᏈ").format(bstack1111lll111_opy_))
        return self.bstack1111lll1l1_opy_(bstack1111lll111_opy_, bstack11111lllll_opy_)
      self.logger.info(bstack1l11l11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤᏉ").format(bstack1111l1111l_opy_))
      response = bstack11ll1ll1l_opy_(bstack1l11l11_opy_ (u"ࠬࡍࡅࡕࠩᏊ"), bstack1111l1111l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1111lll111_opy_, bstack1l11l11_opy_ (u"࠭ࡷࡣࠩᏋ")) as file:
          file.write(response.content)
        self.logger.info(bstack111111l1l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࡦ࡮ࡴࡡࡳࡻࡢࡾ࡮ࡶ࡟ࡱࡣࡷ࡬ࢂࠨᏌ"))
        return self.bstack1111lll1l1_opy_(bstack1111lll111_opy_, bstack11111lllll_opy_)
      else:
        raise(bstack111111l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࡸࡺࡡࡵࡷࡶࡣࡨࡵࡤࡦࡿࠥᏍ"))
    except:
      self.logger.error(bstack1l11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᏎ"))
  def bstack1111l111ll_opy_(self, bstack1111l1111l_opy_, bstack11111lllll_opy_):
    try:
      bstack11111l1111_opy_ = self.bstack1111ll11l1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_)
      bstack1111ll1lll_opy_ = self.bstack1111lllll1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_, bstack11111l1111_opy_)
      return bstack11111l1111_opy_, bstack1111ll1lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᏏ").format(e))
    return bstack11111l1111_opy_, False
  def bstack1111lllll1_opy_(self, bstack1111l1111l_opy_, bstack11111lllll_opy_, bstack11111l1111_opy_, bstack11111l1lll_opy_ = 0):
    if bstack11111l1lll_opy_ > 1:
      return False
    if bstack11111l1111_opy_ == None or os.path.exists(bstack11111l1111_opy_) == False:
      self.logger.warn(bstack1l11l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᏐ"))
      bstack11111l1111_opy_ = self.bstack1111ll11l1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_)
      self.bstack1111lllll1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_, bstack11111l1111_opy_, bstack11111l1lll_opy_+1)
    bstack11111l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥᏑ")
    command = bstack1l11l11_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬᏒ").format(bstack11111l1111_opy_)
    bstack1111llll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11111l1l1l_opy_, bstack1111llll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᏓ"))
      bstack11111l1111_opy_ = self.bstack1111ll11l1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_)
      self.bstack1111lllll1_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_, bstack11111l1111_opy_, bstack11111l1lll_opy_+1)
  def bstack1111lll1l1_opy_(self, bstack1111lll111_opy_, bstack11111lllll_opy_):
    try:
      working_dir = os.path.dirname(bstack1111lll111_opy_)
      shutil.unpack_archive(bstack1111lll111_opy_, working_dir)
      bstack11111l1111_opy_ = os.path.join(working_dir, bstack11111lllll_opy_)
      os.chmod(bstack11111l1111_opy_, 0o755)
      return bstack11111l1111_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᏔ"))
  def bstack1111ll1l11_opy_(self):
    try:
      percy = str(self.config.get(bstack1l11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᏕ"), bstack1l11l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᏖ"))).lower()
      if percy != bstack1l11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᏗ"):
        return False
      self.bstack11l1l111l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᏘ").format(e))
  def bstack1111lll1ll_opy_(self):
    try:
      bstack1111lll1ll_opy_ = str(self.config.get(bstack1l11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᏙ"), bstack1l11l11_opy_ (u"ࠢࡢࡷࡷࡳࠧᏚ"))).lower()
      return bstack1111lll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᏛ").format(e))
  def init(self, bstack1l11ll11ll_opy_, config, logger):
    self.bstack1l11ll11ll_opy_ = bstack1l11ll11ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111ll1l11_opy_():
      return
    self.bstack1111lll11l_opy_ = config.get(bstack1l11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᏜ"), {})
    self.bstack1111l1l11l_opy_ = config.get(bstack1l11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ꮭ"), bstack1l11l11_opy_ (u"ࠦࡦࡻࡴࡰࠤᏞ"))
    try:
      bstack1111l1111l_opy_, bstack11111lllll_opy_ = self.bstack11111lll11_opy_()
      bstack11111l1111_opy_, bstack1111ll1lll_opy_ = self.bstack1111l111ll_opy_(bstack1111l1111l_opy_, bstack11111lllll_opy_)
      if bstack1111ll1lll_opy_:
        self.binary_path = bstack11111l1111_opy_
        thread = Thread(target=self.bstack1111ll111l_opy_)
        thread.start()
      else:
        self.bstack1111l1l1ll_opy_ = True
        self.logger.error(bstack1l11l11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤᏟ").format(bstack11111l1111_opy_))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᏠ").format(e))
  def bstack11111llll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡪࠫᏡ"), bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫᏢ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨᏣ").format(logfile))
      self.bstack111111ll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᏤ").format(e))
  def bstack1111ll111l_opy_(self):
    bstack1111l11ll1_opy_ = self.bstack1111ll11ll_opy_()
    if bstack1111l11ll1_opy_ == None:
      self.bstack1111l1l1ll_opy_ = True
      self.logger.error(bstack1l11l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢᏥ"))
      return False
    command_args = [bstack1l11l11_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨᏦ") if self.bstack1l11ll11ll_opy_ else bstack1l11l11_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪᏧ")]
    bstack1111ll1ll1_opy_ = self.bstack11111ll11l_opy_()
    if bstack1111ll1ll1_opy_ != None:
      command_args.append(bstack1l11l11_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨᏨ").format(bstack1111ll1ll1_opy_))
    env = os.environ.copy()
    env[bstack1l11l11_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨᏩ")] = bstack1111l11ll1_opy_
    bstack11111ll1l1_opy_ = [self.binary_path]
    self.bstack11111llll1_opy_()
    self.bstack1111ll1111_opy_ = self.bstack1111l11l1l_opy_(bstack11111ll1l1_opy_ + command_args, env)
    self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᏪ"))
    bstack11111l1lll_opy_ = 0
    while self.bstack1111ll1111_opy_.poll() == None:
      bstack111111ll1l_opy_ = self.bstack11111l11l1_opy_()
      if bstack111111ll1l_opy_:
        self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᏫ"))
        self.bstack11111l1ll1_opy_ = True
        return True
      bstack11111l1lll_opy_ += 1
      self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᏬ").format(bstack11111l1lll_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᏭ").format(bstack11111l1lll_opy_))
    self.bstack1111l1l1ll_opy_ = True
    return False
  def bstack11111l11l1_opy_(self, bstack11111l1lll_opy_ = 0):
    try:
      if bstack11111l1lll_opy_ > 10:
        return False
      bstack11111l11ll_opy_ = os.environ.get(bstack1l11l11_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ꮾ"), bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᏯ"))
      bstack1111ll1l1l_opy_ = bstack11111l11ll_opy_ + bstack11l1l1111l_opy_
      response = requests.get(bstack1111ll1l1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1111ll11ll_opy_(self):
    bstack111111lll1_opy_ = bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࠬᏰ") if self.bstack1l11ll11ll_opy_ else bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᏱ")
    bstack111ll1l111_opy_ = bstack1l11l11_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠤᏲ").format(self.config[bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᏳ")], bstack111111lll1_opy_)
    uri = bstack11l11l11l_opy_(bstack111ll1l111_opy_)
    try:
      response = bstack11ll1ll1l_opy_(bstack1l11l11_opy_ (u"ࠬࡍࡅࡕࠩᏴ"), uri, {}, {bstack1l11l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᏵ"): (self.config[bstack1l11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᏶")], self.config[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᏷")])})
      if response.status_code == 200:
        bstack1111l1l1l1_opy_ = response.json()
        if bstack1l11l11_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᏸ") in bstack1111l1l1l1_opy_:
          return bstack1111l1l1l1_opy_[bstack1l11l11_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᏹ")]
        else:
          raise bstack1l11l11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫᏺ").format(bstack1111l1l1l1_opy_)
      else:
        raise bstack1l11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧᏻ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢᏼ").format(e))
  def bstack11111ll11l_opy_(self):
    bstack11111lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥᏽ"))
    try:
      if bstack1l11l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ᏾") not in self.bstack1111lll11l_opy_:
        self.bstack1111lll11l_opy_[bstack1l11l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ᏿")] = 2
      with open(bstack11111lll1l_opy_, bstack1l11l11_opy_ (u"ࠪࡻࠬ᐀")) as fp:
        json.dump(self.bstack1111lll11l_opy_, fp)
      return bstack11111lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᐁ").format(e))
  def bstack1111l11l1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1ll11_opy_ == bstack1l11l11_opy_ (u"ࠬࡽࡩ࡯ࠩᐂ"):
        bstack1111l11lll_opy_ = [bstack1l11l11_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧᐃ"), bstack1l11l11_opy_ (u"ࠧ࠰ࡥࠪᐄ")]
        cmd = bstack1111l11lll_opy_ + cmd
      cmd = bstack1l11l11_opy_ (u"ࠨࠢࠪᐅ").join(cmd)
      self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨᐆ").format(cmd))
      with open(self.bstack111111ll11_opy_, bstack1l11l11_opy_ (u"ࠥࡥࠧᐇ")) as bstack1111l111l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111l111l1_opy_, text=True, stderr=bstack1111l111l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l1l1ll_opy_ = True
      self.logger.error(bstack1l11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᐈ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111l1ll1_opy_:
        self.logger.info(bstack1l11l11_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᐉ"))
        cmd = [self.binary_path, bstack1l11l11_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤᐊ")]
        self.bstack1111l11l1l_opy_(cmd)
        self.bstack11111l1ll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᐋ").format(cmd, e))
  def bstack111111lll_opy_(self):
    if not self.bstack11l1l111l_opy_:
      return
    try:
      bstack1111l1llll_opy_ = 0
      while not self.bstack11111l1ll1_opy_ and bstack1111l1llll_opy_ < self.bstack1111l1ll1l_opy_:
        if self.bstack1111l1l1ll_opy_:
          self.logger.info(bstack1l11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨᐌ"))
          return
        time.sleep(1)
        bstack1111l1llll_opy_ += 1
      os.environ[bstack1l11l11_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᐍ")] = str(self.bstack1111llll11_opy_())
      self.logger.info(bstack1l11l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦᐎ"))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᐏ").format(e))
  def bstack1111llll11_opy_(self):
    if self.bstack1l11ll11ll_opy_:
      return
    try:
      bstack111111llll_opy_ = [platform[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᐐ")].lower() for platform in self.config.get(bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᐑ"), [])]
      bstack111111l1ll_opy_ = sys.maxsize
      bstack11111l1l11_opy_ = bstack1l11l11_opy_ (u"ࠧࠨᐒ")
      for browser in bstack111111llll_opy_:
        if browser in self.bstack1111l1l111_opy_:
          bstack11111ll1ll_opy_ = self.bstack1111l1l111_opy_[browser]
        if bstack11111ll1ll_opy_ < bstack111111l1ll_opy_:
          bstack111111l1ll_opy_ = bstack11111ll1ll_opy_
          bstack11111l1l11_opy_ = browser
      return bstack11111l1l11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᐓ").format(e))