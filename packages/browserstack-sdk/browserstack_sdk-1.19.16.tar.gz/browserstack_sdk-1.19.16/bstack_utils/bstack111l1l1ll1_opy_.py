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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _111l1lllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l1l11ll_opy_:
    def __init__(self, handler):
        self._111ll11l11_opy_ = {}
        self._111l1ll1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._111ll11l11_opy_[bstack1l11l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ጗")] = Module._111ll1111l_opy_
        self._111ll11l11_opy_[bstack1l11l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጘ")] = Module._111ll111l1_opy_
        self._111ll11l11_opy_[bstack1l11l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጙ")] = Class._111l1ll11l_opy_
        self._111ll11l11_opy_[bstack1l11l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጚ")] = Class._111l1ll1ll_opy_
        Module._111ll1111l_opy_ = self.bstack111l1ll111_opy_(bstack1l11l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጛ"))
        Module._111ll111l1_opy_ = self.bstack111l1ll111_opy_(bstack1l11l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጜ"))
        Class._111l1ll11l_opy_ = self.bstack111l1ll111_opy_(bstack1l11l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጝ"))
        Class._111l1ll1ll_opy_ = self.bstack111l1ll111_opy_(bstack1l11l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጞ"))
    def bstack111l1lll1l_opy_(self, bstack111ll111ll_opy_, hook_type):
        meth = getattr(bstack111ll111ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l1ll1l1_opy_[hook_type] = meth
            setattr(bstack111ll111ll_opy_, hook_type, self.bstack111l1lll11_opy_(hook_type))
    def bstack111ll11l1l_opy_(self, instance, bstack111l1llll1_opy_):
        if bstack111l1llll1_opy_ == bstack1l11l11_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧጟ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦጠ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣጡ"))
        if bstack111l1llll1_opy_ == bstack1l11l11_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨጢ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧጣ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤጤ"))
        if bstack111l1llll1_opy_ == bstack1l11l11_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣጥ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢጦ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦጧ"))
        if bstack111l1llll1_opy_ == bstack1l11l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧጨ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦጩ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack1l11l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣጪ"))
    @staticmethod
    def bstack111l1l1lll_opy_(hook_type, func, args):
        if hook_type in [bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ጫ"), bstack1l11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪጬ")]:
            _111l1lllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l1lll11_opy_(self, hook_type):
        def bstack111l1l1l1l_opy_(arg=None):
            self.handler(hook_type, bstack1l11l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩጭ"))
            result = None
            exception = None
            try:
                self.bstack111l1l1lll_opy_(hook_type, self._111l1ll1l1_opy_[hook_type], (arg,))
                result = Result(result=bstack1l11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪጮ"))
            except Exception as e:
                result = Result(result=bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጯ"), exception=e)
                self.handler(hook_type, bstack1l11l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫጰ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬጱ"), result)
        def bstack111l1l1l11_opy_(this, arg=None):
            self.handler(hook_type, bstack1l11l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧጲ"))
            result = None
            exception = None
            try:
                self.bstack111l1l1lll_opy_(hook_type, self._111l1ll1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l11l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨጳ"))
            except Exception as e:
                result = Result(result=bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩጴ"), exception=e)
                self.handler(hook_type, bstack1l11l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩጵ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪጶ"), result)
        if hook_type in [bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫጷ"), bstack1l11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨጸ")]:
            return bstack111l1l1l11_opy_
        return bstack111l1l1l1l_opy_
    def bstack111l1ll111_opy_(self, bstack111l1llll1_opy_):
        def bstack111ll11111_opy_(this, *args, **kwargs):
            self.bstack111ll11l1l_opy_(this, bstack111l1llll1_opy_)
            self._111ll11l11_opy_[bstack111l1llll1_opy_](this, *args, **kwargs)
        return bstack111ll11111_opy_