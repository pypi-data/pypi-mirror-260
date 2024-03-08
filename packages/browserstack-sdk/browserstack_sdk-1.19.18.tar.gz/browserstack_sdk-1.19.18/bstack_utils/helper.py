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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1l11lll_opy_, bstack111l1lll1_opy_, bstack1ll1ll11l_opy_, bstack1l1l11ll1_opy_
from bstack_utils.messages import bstack1ll1ll1ll_opy_, bstack111ll1l11_opy_
from bstack_utils.proxy import bstack1lll1l111_opy_, bstack1l1lll1l1l_opy_
bstack11l11111_opy_ = Config.bstack1llllllll_opy_()
def bstack11ll11111l_opy_(config):
    return config[bstack1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᅽ")]
def bstack11ll1l1111_opy_(config):
    return config[bstack1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᅾ")]
def bstack1llll1lll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll11_opy_(obj):
    values = []
    bstack11l1111ll1_opy_ = re.compile(bstack1l1l1_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᅿ"), re.I)
    for key in obj.keys():
        if bstack11l1111ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111lll1l1l_opy_(config):
    tags = []
    tags.extend(bstack11l11lll11_opy_(os.environ))
    tags.extend(bstack11l11lll11_opy_(config))
    return tags
def bstack111lll111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lllll1l_opy_(bstack111lll11l1_opy_):
    if not bstack111lll11l1_opy_:
        return bstack1l1l1_opy_ (u"ࠧࠨᆀ")
    return bstack1l1l1_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᆁ").format(bstack111lll11l1_opy_.name, bstack111lll11l1_opy_.email)
def bstack11ll1111l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111ll1l1ll_opy_ = repo.common_dir
        info = {
            bstack1l1l1_opy_ (u"ࠤࡶ࡬ࡦࠨᆂ"): repo.head.commit.hexsha,
            bstack1l1l1_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᆃ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᆄ"): repo.active_branch.name,
            bstack1l1l1_opy_ (u"ࠧࡺࡡࡨࠤᆅ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᆆ"): bstack111lllll1l_opy_(repo.head.commit.committer),
            bstack1l1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᆇ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᆈ"): bstack111lllll1l_opy_(repo.head.commit.author),
            bstack1l1l1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᆉ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᆊ"): repo.head.commit.message,
            bstack1l1l1_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᆋ"): repo.git.rev_parse(bstack1l1l1_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᆌ")),
            bstack1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᆍ"): bstack111ll1l1ll_opy_,
            bstack1l1l1_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᆎ"): subprocess.check_output([bstack1l1l1_opy_ (u"ࠣࡩ࡬ࡸࠧᆏ"), bstack1l1l1_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᆐ"), bstack1l1l1_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᆑ")]).strip().decode(
                bstack1l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᆒ")),
            bstack1l1l1_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᆓ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᆔ"): repo.git.rev_list(
                bstack1l1l1_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᆕ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111llll11l_opy_ = []
        for remote in remotes:
            bstack11l11l11ll_opy_ = {
                bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᆖ"): remote.name,
                bstack1l1l1_opy_ (u"ࠤࡸࡶࡱࠨᆗ"): remote.url,
            }
            bstack111llll11l_opy_.append(bstack11l11l11ll_opy_)
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᆘ"): bstack1l1l1_opy_ (u"ࠦ࡬࡯ࡴࠣᆙ"),
            **info,
            bstack1l1l1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᆚ"): bstack111llll11l_opy_
        }
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᆛ").format(err))
        return {}
def bstack11llll11_opy_():
    env = os.environ
    if (bstack1l1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᆜ") in env and len(env[bstack1l1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᆝ")]) > 0) or (
            bstack1l1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᆞ") in env and len(env[bstack1l1l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᆟ")]) > 0):
        return {
            bstack1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆠ"): bstack1l1l1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᆡ"),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆢ"): env.get(bstack1l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆣ")),
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆤ"): env.get(bstack1l1l1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᆥ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆦ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆧ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠧࡉࡉࠣᆨ")) == bstack1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᆩ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᆪ"))):
        return {
            bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᆫ"): bstack1l1l1_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᆬ"),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆭ"): env.get(bstack1l1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᆮ")),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆯ"): env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᆰ")),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆱ"): env.get(bstack1l1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᆲ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠤࡆࡍࠧᆳ")) == bstack1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᆴ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᆵ"))):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆶ"): bstack1l1l1_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᆷ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆸ"): env.get(bstack1l1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᆹ")),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆺ"): env.get(bstack1l1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᆻ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆼ"): env.get(bstack1l1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆽ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࠤᆾ")) == bstack1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᆿ") and env.get(bstack1l1l1_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᇀ")) == bstack1l1l1_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᇁ"):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᇂ"): bstack1l1l1_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᇃ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇄ"): None,
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇅ"): None,
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇆ"): None
        }
    if env.get(bstack1l1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᇇ")) and env.get(bstack1l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᇈ")):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᇉ"): bstack1l1l1_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᇊ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇋ"): env.get(bstack1l1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᇌ")),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇍ"): None,
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇎ"): env.get(bstack1l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇏ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࠨᇐ")) == bstack1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᇑ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᇒ"))):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇓ"): bstack1l1l1_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᇔ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇕ"): env.get(bstack1l1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᇖ")),
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇗ"): None,
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇘ"): env.get(bstack1l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇙ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࠤᇚ")) == bstack1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᇛ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᇜ"))):
        return {
            bstack1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇝ"): bstack1l1l1_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᇞ"),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇟ"): env.get(bstack1l1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᇠ")),
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇡ"): env.get(bstack1l1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇢ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇣ"): env.get(bstack1l1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᇤ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࠨᇥ")) == bstack1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᇦ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᇧ"))):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇨ"): bstack1l1l1_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᇩ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇪ"): env.get(bstack1l1l1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᇫ")),
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇬ"): env.get(bstack1l1l1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᇭ")),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇮ"): env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᇯ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠢࡄࡋࠥᇰ")) == bstack1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᇱ") and bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᇲ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᇳ"): bstack1l1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᇴ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇵ"): env.get(bstack1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇶ")),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇷ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᇸ")) or env.get(bstack1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᇹ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇺ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᇻ"))
        }
    if bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᇼ"))):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇽ"): bstack1l1l1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᇾ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇿ"): bstack1l1l1_opy_ (u"ࠤࡾࢁࢀࢃࠢሀ").format(env.get(bstack1l1l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ሁ")), env.get(bstack1l1l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫሂ"))),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሃ"): env.get(bstack1l1l1_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧሄ")),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨህ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣሆ"))
        }
    if bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦሇ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣለ"): bstack1l1l1_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨሉ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሊ"): bstack1l1l1_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧላ").format(env.get(bstack1l1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ሌ")), env.get(bstack1l1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩል")), env.get(bstack1l1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪሎ")), env.get(bstack1l1l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧሏ"))),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሐ"): env.get(bstack1l1l1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤሑ")),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሒ"): env.get(bstack1l1l1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣሓ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤሔ")) and env.get(bstack1l1l1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦሕ")):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣሖ"): bstack1l1l1_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨሗ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣመ"): bstack1l1l1_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤሙ").format(env.get(bstack1l1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪሚ")), env.get(bstack1l1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ማ")), env.get(bstack1l1l1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩሜ"))),
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧም"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦሞ")),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሟ"): env.get(bstack1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨሠ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧሡ")), env.get(bstack1l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢሢ")), env.get(bstack1l1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨሣ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣሤ"): bstack1l1l1_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦሥ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሦ"): env.get(bstack1l1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧሧ")),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤረ"): env.get(bstack1l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨሩ")),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሪ"): env.get(bstack1l1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣራ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤሬ")):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥር"): bstack1l1l1_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨሮ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሯ"): env.get(bstack1l1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥሰ")),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሱ"): env.get(bstack1l1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤሲ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሳ"): env.get(bstack1l1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥሴ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢስ")) or env.get(bstack1l1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤሶ")):
        return {
            bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨሷ"): bstack1l1l1_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥሸ"),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሹ"): env.get(bstack1l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሺ")),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሻ"): bstack1l1l1_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨሼ") if env.get(bstack1l1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤሽ")) else None,
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሾ"): env.get(bstack1l1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢሿ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቀ")), env.get(bstack1l1l1_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧቁ")), env.get(bstack1l1l1_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧቂ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቃ"): bstack1l1l1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨቄ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቅ"): None,
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦቆ"): env.get(bstack1l1l1_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢቇ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቈ"): env.get(bstack1l1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ቉"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤቊ")):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቋ"): bstack1l1l1_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦቌ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቍ"): env.get(bstack1l1l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ቎")),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ቏"): bstack1l1l1_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨቐ").format(env.get(bstack1l1l1_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩቑ"))) if env.get(bstack1l1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥቒ")) else None,
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቓ"): env.get(bstack1l1l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦቔ"))
        }
    if bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦቕ"))):
        return {
            bstack1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቖ"): bstack1l1l1_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ቗"),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቘ"): env.get(bstack1l1l1_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ቙")),
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቚ"): env.get(bstack1l1l1_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧቛ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቜ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቝ"))
        }
    if bstack111l11l1l_opy_(env.get(bstack1l1l1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨ቞"))):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ቟"): bstack1l1l1_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣበ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቡ"): bstack1l1l1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥቢ").format(env.get(bstack1l1l1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧባ")), env.get(bstack1l1l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨቤ")), env.get(bstack1l1l1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬብ"))),
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣቦ"): env.get(bstack1l1l1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤቧ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቨ"): env.get(bstack1l1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤቩ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࠨቪ")) == bstack1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤቫ") and env.get(bstack1l1l1_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧቬ")) == bstack1l1l1_opy_ (u"ࠨ࠱ࠣቭ"):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቮ"): bstack1l1l1_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣቯ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧተ"): bstack1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨቱ").format(env.get(bstack1l1l1_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨቲ"))),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢታ"): None,
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቴ"): None,
        }
    if env.get(bstack1l1l1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥት")):
        return {
            bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨቶ"): bstack1l1l1_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦቷ"),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቸ"): None,
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቹ"): env.get(bstack1l1l1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨቺ")),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቻ"): env.get(bstack1l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨቼ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦች")), env.get(bstack1l1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤቾ")), env.get(bstack1l1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣቿ")), env.get(bstack1l1l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧኀ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኁ"): bstack1l1l1_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤኂ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኃ"): None,
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኄ"): env.get(bstack1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥኅ")) or None,
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኆ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨኇ"), 0)
        }
    if env.get(bstack1l1l1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥኈ")):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ኉"): bstack1l1l1_opy_ (u"ࠢࡈࡱࡆࡈࠧኊ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኋ"): None,
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦኌ"): env.get(bstack1l1l1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣኍ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ኎"): env.get(bstack1l1l1_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ኏"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦነ")):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኑ"): bstack1l1l1_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦኒ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧና"): env.get(bstack1l1l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤኔ")),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨን"): env.get(bstack1l1l1_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣኖ")),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኗ"): env.get(bstack1l1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧኘ"))
        }
    return {bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኙ"): None}
def get_host_info():
    return {
        bstack1l1l1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦኚ"): platform.node(),
        bstack1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧኛ"): platform.system(),
        bstack1l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤኜ"): platform.machine(),
        bstack1l1l1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨኝ"): platform.version(),
        bstack1l1l1_opy_ (u"ࠨࡡࡳࡥ࡫ࠦኞ"): platform.architecture()[0]
    }
def bstack1ll1111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11lllll_opy_():
    if bstack11l11111_opy_.get_property(bstack1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨኟ")):
        return bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧአ")
    return bstack1l1l1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨኡ")
def bstack111lll1l11_opy_(driver):
    info = {
        bstack1l1l1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩኢ"): driver.capabilities,
        bstack1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨኣ"): driver.session_id,
        bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ኤ"): driver.capabilities.get(bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫእ"), None),
        bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩኦ"): driver.capabilities.get(bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩኧ"), None),
        bstack1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫከ"): driver.capabilities.get(bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩኩ"), None),
    }
    if bstack11l11lllll_opy_() == bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪኪ"):
        info[bstack1l1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ካ")] = bstack1l1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬኬ") if bstack1ll11l11l1_opy_() else bstack1l1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩክ")
    return info
def bstack1ll11l11l1_opy_():
    if bstack11l11111_opy_.get_property(bstack1l1l1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧኮ")):
        return True
    if bstack111l11l1l_opy_(os.environ.get(bstack1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪኯ"), None)):
        return True
    return False
def bstack1l1lll11ll_opy_(bstack111lll1lll_opy_, url, data, config):
    headers = config.get(bstack1l1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫኰ"), None)
    proxies = bstack1lll1l111_opy_(config, url)
    auth = config.get(bstack1l1l1_opy_ (u"ࠫࡦࡻࡴࡩࠩ኱"), None)
    response = requests.request(
            bstack111lll1lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll1lll_opy_(bstack1ll1lll1l1_opy_, size):
    bstack1lll111l1_opy_ = []
    while len(bstack1ll1lll1l1_opy_) > size:
        bstack111ll11l1_opy_ = bstack1ll1lll1l1_opy_[:size]
        bstack1lll111l1_opy_.append(bstack111ll11l1_opy_)
        bstack1ll1lll1l1_opy_ = bstack1ll1lll1l1_opy_[size:]
    bstack1lll111l1_opy_.append(bstack1ll1lll1l1_opy_)
    return bstack1lll111l1_opy_
def bstack11l11ll1l1_opy_(message, bstack111ll1ll1l_opy_=False):
    os.write(1, bytes(message, bstack1l1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫኲ")))
    os.write(1, bytes(bstack1l1l1_opy_ (u"࠭࡜࡯ࠩኳ"), bstack1l1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ኴ")))
    if bstack111ll1ll1l_opy_:
        with open(bstack1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧኵ") + os.environ[bstack1l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ኶")] + bstack1l1l1_opy_ (u"ࠪ࠲ࡱࡵࡧࠨ኷"), bstack1l1l1_opy_ (u"ࠫࡦ࠭ኸ")) as f:
            f.write(message + bstack1l1l1_opy_ (u"ࠬࡢ࡮ࠨኹ"))
def bstack11l111llll_opy_():
    return os.environ[bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩኺ")].lower() == bstack1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬኻ")
def bstack1l11llll11_opy_(bstack11l11l11l1_opy_):
    return bstack1l1l1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧኼ").format(bstack11l1l11lll_opy_, bstack11l11l11l1_opy_)
def bstack1lll1l1ll1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫኽ")
def bstack11l11l1l11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1_opy_ (u"ࠪ࡞ࠬኾ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1_opy_ (u"ࠫ࡟࠭኿")))).total_seconds() * 1000
def bstack111llllll1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1l1l1_opy_ (u"ࠬࡠࠧዀ")
def bstack11l11l111l_opy_(bstack11l11ll111_opy_):
    date_format = bstack1l1l1_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫ዁")
    bstack11l11ll1ll_opy_ = datetime.datetime.strptime(bstack11l11ll111_opy_, date_format)
    return bstack11l11ll1ll_opy_.isoformat() + bstack1l1l1_opy_ (u"࡛ࠧࠩዂ")
def bstack11l11l1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዃ")
    else:
        return bstack1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዄ")
def bstack111l11l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨዅ")
def bstack111lll11ll_opy_(val):
    return val.__str__().lower() == bstack1l1l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ዆")
def bstack1l1111l1ll_opy_(bstack11l1111l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1111l1l_opy_ as e:
                print(bstack1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧ዇").format(func.__name__, bstack11l1111l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1111l11_opy_(bstack111lll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lll1111_opy_(cls, *args, **kwargs)
            except bstack11l1111l1l_opy_ as e:
                print(bstack1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨወ").format(bstack111lll1111_opy_.__name__, bstack11l1111l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1111l11_opy_
    else:
        return decorator
def bstack1l1l1lll1l_opy_(bstack11lll111ll_opy_):
    if bstack1l1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዉ") in bstack11lll111ll_opy_ and bstack111lll11ll_opy_(bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዊ")]):
        return False
    if bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዋ") in bstack11lll111ll_opy_ and bstack111lll11ll_opy_(bstack11lll111ll_opy_[bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዌ")]):
        return False
    return True
def bstack1l11l1l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1lll1lll_opy_(hub_url):
    if bstack1111111l1_opy_() <= version.parse(bstack1l1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫው")):
        if hub_url != bstack1l1l1_opy_ (u"ࠬ࠭ዎ"):
            return bstack1l1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢዏ") + hub_url + bstack1l1l1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦዐ")
        return bstack1ll1ll11l_opy_
    if hub_url != bstack1l1l1_opy_ (u"ࠨࠩዑ"):
        return bstack1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦዒ") + hub_url + bstack1l1l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦዓ")
    return bstack1l1l11ll1_opy_
def bstack11l11l1111_opy_():
    return isinstance(os.getenv(bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪዔ")), str)
def bstack1111l1l1_opy_(url):
    return urlparse(url).hostname
def bstack1l1l11l11_opy_(hostname):
    for bstack1l11l11ll_opy_ in bstack111l1lll1_opy_:
        regex = re.compile(bstack1l11l11ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11lll1l_opy_(bstack11l111l11l_opy_, file_name, logger):
    bstack1l1l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1_opy_ (u"ࠬࢄࠧዕ")), bstack11l111l11l_opy_)
    try:
        if not os.path.exists(bstack1l1l11l1ll_opy_):
            os.makedirs(bstack1l1l11l1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1_opy_ (u"࠭ࡾࠨዖ")), bstack11l111l11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1_opy_ (u"ࠧࡸࠩ዗")):
                pass
            with open(file_path, bstack1l1l1_opy_ (u"ࠣࡹ࠮ࠦዘ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1ll1ll_opy_.format(str(e)))
def bstack11l11l1l1l_opy_(file_name, key, value, logger):
    file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩዙ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lllll_opy_ = json.load(open(file_path, bstack1l1l1_opy_ (u"ࠪࡶࡧ࠭ዚ")))
        else:
            bstack1l1lllll_opy_ = {}
        bstack1l1lllll_opy_[key] = value
        with open(file_path, bstack1l1l1_opy_ (u"ࠦࡼ࠱ࠢዛ")) as outfile:
            json.dump(bstack1l1lllll_opy_, outfile)
def bstack1l1ll1l1ll_opy_(file_name, logger):
    file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬዜ"), file_name, logger)
    bstack1l1lllll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1_opy_ (u"࠭ࡲࠨዝ")) as bstack1l11l1111_opy_:
            bstack1l1lllll_opy_ = json.load(bstack1l11l1111_opy_)
    return bstack1l1lllll_opy_
def bstack11ll11ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫዞ") + file_path + bstack1l1l1_opy_ (u"ࠨࠢࠪዟ") + str(e))
def bstack1111111l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦዠ")
def bstack1ll1lll1ll_opy_(config):
    if bstack1l1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩዡ") in config:
        del (config[bstack1l1l1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪዢ")])
        return False
    if bstack1111111l1_opy_() < version.parse(bstack1l1l1_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫዣ")):
        return False
    if bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬዤ")):
        return True
    if bstack1l1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧዥ") in config and config[bstack1l1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨዦ")] is False:
        return False
    else:
        return True
def bstack1ll1l11111_opy_(args_list, bstack111lllllll_opy_):
    index = -1
    for value in bstack111lllllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l111llll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l111llll1_opy_ = bstack1l111llll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዧ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪየ"), exception=exception)
    def bstack11ll1l1ll1_opy_(self):
        if self.result != bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዩ"):
            return None
        if bstack1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣዪ") in self.exception_type:
            return bstack1l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢያ")
        return bstack1l1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣዬ")
    def bstack11l11111l1_opy_(self):
        if self.result != bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨይ"):
            return None
        if self.bstack1l111llll1_opy_:
            return self.bstack1l111llll1_opy_
        return bstack111ll1lll1_opy_(self.exception)
def bstack111ll1lll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1111111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11ll1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11l11l_opy_(config, logger):
    try:
        import playwright
        bstack11l111l111_opy_ = playwright.__file__
        bstack11l11llll1_opy_ = os.path.split(bstack11l111l111_opy_)
        bstack11l11l1ll1_opy_ = bstack11l11llll1_opy_[0] + bstack1l1l1_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬዮ")
        os.environ[bstack1l1l1_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ዯ")] = bstack1l1lll1l1l_opy_(config)
        with open(bstack11l11l1ll1_opy_, bstack1l1l1_opy_ (u"ࠫࡷ࠭ደ")) as f:
            bstack1ll1l1l1ll_opy_ = f.read()
            bstack11l11111ll_opy_ = bstack1l1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫዱ")
            bstack11l111lll1_opy_ = bstack1ll1l1l1ll_opy_.find(bstack11l11111ll_opy_)
            if bstack11l111lll1_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥዲ"), shell=True, cwd=bstack11l11llll1_opy_[0])
              process.wait()
              bstack111lll1ll1_opy_ = bstack1l1l1_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧዳ")
              bstack111ll1llll_opy_ = bstack1l1l1_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧዴ")
              bstack11l1111lll_opy_ = bstack1ll1l1l1ll_opy_.replace(bstack111lll1ll1_opy_, bstack111ll1llll_opy_)
              with open(bstack11l11l1ll1_opy_, bstack1l1l1_opy_ (u"ࠩࡺࠫድ")) as f:
                f.write(bstack11l1111lll_opy_)
    except Exception as e:
        logger.error(bstack111ll1l11_opy_.format(str(e)))
def bstack1lll1l1l11_opy_():
  try:
    bstack111llll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪዶ"))
    bstack111llll1ll_opy_ = []
    if os.path.exists(bstack111llll1l1_opy_):
      with open(bstack111llll1l1_opy_) as f:
        bstack111llll1ll_opy_ = json.load(f)
      os.remove(bstack111llll1l1_opy_)
    return bstack111llll1ll_opy_
  except:
    pass
  return []
def bstack11ll1lll1_opy_(bstack1llll1l1l1_opy_):
  try:
    bstack111llll1ll_opy_ = []
    bstack111llll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫዷ"))
    if os.path.exists(bstack111llll1l1_opy_):
      with open(bstack111llll1l1_opy_) as f:
        bstack111llll1ll_opy_ = json.load(f)
    bstack111llll1ll_opy_.append(bstack1llll1l1l1_opy_)
    with open(bstack111llll1l1_opy_, bstack1l1l1_opy_ (u"ࠬࡽࠧዸ")) as f:
        json.dump(bstack111llll1ll_opy_, f)
  except:
    pass
def bstack1l1llll1_opy_(logger, bstack111llll111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩዹ"), bstack1l1l1_opy_ (u"ࠧࠨዺ"))
    if test_name == bstack1l1l1_opy_ (u"ࠨࠩዻ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨዼ"), bstack1l1l1_opy_ (u"ࠪࠫዽ"))
    bstack11l11ll11l_opy_ = bstack1l1l1_opy_ (u"ࠫ࠱ࠦࠧዾ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111llll111_opy_:
        bstack1l1l1111_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬዿ"), bstack1l1l1_opy_ (u"࠭࠰ࠨጀ"))
        bstack1lll11l11_opy_ = {bstack1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬጁ"): test_name, bstack1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጂ"): bstack11l11ll11l_opy_, bstack1l1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨጃ"): bstack1l1l1111_opy_}
        bstack111ll1ll11_opy_ = []
        bstack11l111l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩጄ"))
        if os.path.exists(bstack11l111l1l1_opy_):
            with open(bstack11l111l1l1_opy_) as f:
                bstack111ll1ll11_opy_ = json.load(f)
        bstack111ll1ll11_opy_.append(bstack1lll11l11_opy_)
        with open(bstack11l111l1l1_opy_, bstack1l1l1_opy_ (u"ࠫࡼ࠭ጅ")) as f:
            json.dump(bstack111ll1ll11_opy_, f)
    else:
        bstack1lll11l11_opy_ = {bstack1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪጆ"): test_name, bstack1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጇ"): bstack11l11ll11l_opy_, bstack1l1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ገ"): str(multiprocessing.current_process().name)}
        if bstack1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬጉ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll11l11_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨጊ").format(e))
def bstack1l1l11l11l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l111ll1l_opy_ = []
    bstack1lll11l11_opy_ = {bstack1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨጋ"): test_name, bstack1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪጌ"): error_message, bstack1l1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫግ"): index}
    bstack11l111ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧጎ"))
    if os.path.exists(bstack11l111ll11_opy_):
        with open(bstack11l111ll11_opy_) as f:
            bstack11l111ll1l_opy_ = json.load(f)
    bstack11l111ll1l_opy_.append(bstack1lll11l11_opy_)
    with open(bstack11l111ll11_opy_, bstack1l1l1_opy_ (u"ࠧࡸࠩጏ")) as f:
        json.dump(bstack11l111ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦጐ").format(e))
def bstack1ll11l111_opy_(bstack111111ll_opy_, name, logger):
  try:
    bstack1lll11l11_opy_ = {bstack1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ጑"): name, bstack1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩጒ"): bstack111111ll_opy_, bstack1l1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪጓ"): str(threading.current_thread()._name)}
    return bstack1lll11l11_opy_
  except Exception as e:
    logger.warn(bstack1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤጔ").format(e))
  return
def bstack11l111l1ll_opy_():
    return platform.system() == bstack1l1l1_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧጕ")
def bstack11l111l1l_opy_(bstack11l111111l_opy_, config, logger):
    bstack111lllll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ጖").format(e))
    return bstack111lllll11_opy_