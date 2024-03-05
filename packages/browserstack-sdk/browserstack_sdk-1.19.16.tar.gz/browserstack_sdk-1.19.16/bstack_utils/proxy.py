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
from urllib.parse import urlparse
from bstack_utils.messages import bstack1111llllll_opy_
def bstack1lllllll11l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllllll111_opy_(bstack1llllll1ll1_opy_, bstack1llllll1l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllll1ll1_opy_):
        with open(bstack1llllll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllllll11l_opy_(bstack1llllll1ll1_opy_):
        pac = get_pac(url=bstack1llllll1ll1_opy_)
    else:
        raise Exception(bstack1l11l11_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᐕ").format(bstack1llllll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11l11_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᐖ"), 80))
        bstack1llllll1lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llllll1lll_opy_ = bstack1l11l11_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᐗ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llllll1l11_opy_, bstack1llllll1lll_opy_)
    return proxy_url
def bstack1ll1l11ll_opy_(config):
    return bstack1l11l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐘ") in config or bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐙ") in config
def bstack111111l1_opy_(config):
    if not bstack1ll1l11ll_opy_(config):
        return
    if config.get(bstack1l11l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐚ")):
        return config.get(bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐛ"))
    if config.get(bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐜ")):
        return config.get(bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐝ"))
def bstack1l1111ll1_opy_(config, bstack1llllll1l11_opy_):
    proxy = bstack111111l1_opy_(config)
    proxies = {}
    if config.get(bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐞ")) or config.get(bstack1l11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐟ")):
        if proxy.endswith(bstack1l11l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᐠ")):
            proxies = bstack11lll1111_opy_(proxy, bstack1llllll1l11_opy_)
        else:
            proxies = {
                bstack1l11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐡ"): proxy
            }
    return proxies
def bstack11lll1111_opy_(bstack1llllll1ll1_opy_, bstack1llllll1l11_opy_):
    proxies = {}
    global bstack1llllll1l1l_opy_
    if bstack1l11l11_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᐢ") in globals():
        return bstack1llllll1l1l_opy_
    try:
        proxy = bstack1lllllll111_opy_(bstack1llllll1ll1_opy_, bstack1llllll1l11_opy_)
        if bstack1l11l11_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᐣ") in proxy:
            proxies = {}
        elif bstack1l11l11_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᐤ") in proxy or bstack1l11l11_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᐥ") in proxy or bstack1l11l11_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᐦ") in proxy:
            bstack1lllllll1l1_opy_ = proxy.split(bstack1l11l11_opy_ (u"ࠢࠡࠤᐧ"))
            if bstack1l11l11_opy_ (u"ࠣ࠼࠲࠳ࠧᐨ") in bstack1l11l11_opy_ (u"ࠤࠥᐩ").join(bstack1lllllll1l1_opy_[1:]):
                proxies = {
                    bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐪ"): bstack1l11l11_opy_ (u"ࠦࠧᐫ").join(bstack1lllllll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐬ"): str(bstack1lllllll1l1_opy_[0]).lower() + bstack1l11l11_opy_ (u"ࠨ࠺࠰࠱ࠥᐭ") + bstack1l11l11_opy_ (u"ࠢࠣᐮ").join(bstack1lllllll1l1_opy_[1:])
                }
        elif bstack1l11l11_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᐯ") in proxy:
            bstack1lllllll1l1_opy_ = proxy.split(bstack1l11l11_opy_ (u"ࠤࠣࠦᐰ"))
            if bstack1l11l11_opy_ (u"ࠥ࠾࠴࠵ࠢᐱ") in bstack1l11l11_opy_ (u"ࠦࠧᐲ").join(bstack1lllllll1l1_opy_[1:]):
                proxies = {
                    bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐳ"): bstack1l11l11_opy_ (u"ࠨࠢᐴ").join(bstack1lllllll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐵ"): bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᐶ") + bstack1l11l11_opy_ (u"ࠤࠥᐷ").join(bstack1lllllll1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐸ"): proxy
            }
    except Exception as e:
        print(bstack1l11l11_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᐹ"), bstack1111llllll_opy_.format(bstack1llllll1ll1_opy_, str(e)))
    bstack1llllll1l1l_opy_ = proxies
    return proxies