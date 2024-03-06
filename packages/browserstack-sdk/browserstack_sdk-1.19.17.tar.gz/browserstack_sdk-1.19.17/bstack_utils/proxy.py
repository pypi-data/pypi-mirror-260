# coding: UTF-8
import sys
bstack11l1111_opy_ = sys.version_info [0] == 2
bstack11l_opy_ = 2048
bstack11llll_opy_ = 7
def bstack1l1111l_opy_ (bstack11l1ll_opy_):
    global bstack11ll11l_opy_
    bstack1111ll1_opy_ = ord (bstack11l1ll_opy_ [-1])
    bstack11l11_opy_ = bstack11l1ll_opy_ [:-1]
    bstack1ll11_opy_ = bstack1111ll1_opy_ % len (bstack11l11_opy_)
    bstack1l111ll_opy_ = bstack11l11_opy_ [:bstack1ll11_opy_] + bstack11l11_opy_ [bstack1ll11_opy_:]
    if bstack11l1111_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l_opy_ - (bstack111l11_opy_ + bstack1111ll1_opy_) % bstack11llll_opy_) for bstack111l11_opy_, char in enumerate (bstack1l111ll_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack11l_opy_ - (bstack111l11_opy_ + bstack1111ll1_opy_) % bstack11llll_opy_) for bstack111l11_opy_, char in enumerate (bstack1l111ll_opy_)])
    return eval (bstack11lll1l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l11l1l1_opy_
def bstack1llllllll1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllllllll1_opy_(bstack11111111ll_opy_, bstack1111111111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111111ll_opy_):
        with open(bstack11111111ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llllllll1l_opy_(bstack11111111ll_opy_):
        pac = get_pac(url=bstack11111111ll_opy_)
    else:
        raise Exception(bstack1l1111l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᐕ").format(bstack11111111ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1111l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᐖ"), 80))
        bstack11111111l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111111l1_opy_ = bstack1l1111l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᐗ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111111111_opy_, bstack11111111l1_opy_)
    return proxy_url
def bstack1l11111l1_opy_(config):
    return bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐘ") in config or bstack1l1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐙ") in config
def bstack11111ll1_opy_(config):
    if not bstack1l11111l1_opy_(config):
        return
    if config.get(bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐚ")):
        return config.get(bstack1l1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐛ"))
    if config.get(bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐜ")):
        return config.get(bstack1l1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐝ"))
def bstack11ll1l111_opy_(config, bstack1111111111_opy_):
    proxy = bstack11111ll1_opy_(config)
    proxies = {}
    if config.get(bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐞ")) or config.get(bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐟ")):
        if proxy.endswith(bstack1l1111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᐠ")):
            proxies = bstack11l1lllll_opy_(proxy, bstack1111111111_opy_)
        else:
            proxies = {
                bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐡ"): proxy
            }
    return proxies
def bstack11l1lllll_opy_(bstack11111111ll_opy_, bstack1111111111_opy_):
    proxies = {}
    global bstack1llllllllll_opy_
    if bstack1l1111l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᐢ") in globals():
        return bstack1llllllllll_opy_
    try:
        proxy = bstack1lllllllll1_opy_(bstack11111111ll_opy_, bstack1111111111_opy_)
        if bstack1l1111l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᐣ") in proxy:
            proxies = {}
        elif bstack1l1111l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᐤ") in proxy or bstack1l1111l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᐥ") in proxy or bstack1l1111l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᐦ") in proxy:
            bstack111111111l_opy_ = proxy.split(bstack1l1111l_opy_ (u"ࠢࠡࠤᐧ"))
            if bstack1l1111l_opy_ (u"ࠣ࠼࠲࠳ࠧᐨ") in bstack1l1111l_opy_ (u"ࠤࠥᐩ").join(bstack111111111l_opy_[1:]):
                proxies = {
                    bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐪ"): bstack1l1111l_opy_ (u"ࠦࠧᐫ").join(bstack111111111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐬ"): str(bstack111111111l_opy_[0]).lower() + bstack1l1111l_opy_ (u"ࠨ࠺࠰࠱ࠥᐭ") + bstack1l1111l_opy_ (u"ࠢࠣᐮ").join(bstack111111111l_opy_[1:])
                }
        elif bstack1l1111l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᐯ") in proxy:
            bstack111111111l_opy_ = proxy.split(bstack1l1111l_opy_ (u"ࠤࠣࠦᐰ"))
            if bstack1l1111l_opy_ (u"ࠥ࠾࠴࠵ࠢᐱ") in bstack1l1111l_opy_ (u"ࠦࠧᐲ").join(bstack111111111l_opy_[1:]):
                proxies = {
                    bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐳ"): bstack1l1111l_opy_ (u"ࠨࠢᐴ").join(bstack111111111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐵ"): bstack1l1111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᐶ") + bstack1l1111l_opy_ (u"ࠤࠥᐷ").join(bstack111111111l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐸ"): proxy
            }
    except Exception as e:
        print(bstack1l1111l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᐹ"), bstack111l11l1l1_opy_.format(bstack11111111ll_opy_, str(e)))
    bstack1llllllllll_opy_ = proxies
    return proxies