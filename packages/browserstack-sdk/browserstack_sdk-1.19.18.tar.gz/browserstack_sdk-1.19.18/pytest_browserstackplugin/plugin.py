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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll11l1_opy_, bstack11l1l1l1_opy_, update, bstack1llll11l1l_opy_,
                                       bstack1ll11l11ll_opy_, bstack1ll11llll_opy_, bstack1l11l11l1_opy_, bstack1ll1111l11_opy_,
                                       bstack1l11l1l11l_opy_, bstack1lll1l1ll_opy_, bstack1ll1lll111_opy_, bstack11l1ll111_opy_,
                                       bstack11lllll11_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l11l111_opy_)
from browserstack_sdk.bstack1l11ll1l1l_opy_ import bstack11l111ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1lllll111l_opy_
from bstack_utils.capture import bstack1l111111ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll1lll1l_opy_, bstack11l11l1l1_opy_, bstack1lll11lll_opy_, \
    bstack11ll111ll_opy_
from bstack_utils.helper import bstack1l11ll1ll_opy_, bstack1ll1111l_opy_, bstack11l111llll_opy_, bstack1lll1l1ll1_opy_, \
    bstack11l11l1lll_opy_, \
    bstack111lll111l_opy_, bstack1111111l1_opy_, bstack1l1lll1lll_opy_, bstack11l11l1111_opy_, bstack1l11l1l1_opy_, Notset, \
    bstack1ll1lll1ll_opy_, bstack11l11l1l11_opy_, bstack111ll1lll1_opy_, Result, bstack111llllll1_opy_, bstack11l1111111_opy_, bstack1l1111l1ll_opy_, \
    bstack11ll1lll1_opy_, bstack1l1llll1_opy_, bstack111l11l1l_opy_, bstack11l111l1ll_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack111ll1111l_opy_
from bstack_utils.messages import bstack1lll1lll_opy_, bstack1lll11ll1_opy_, bstack1l11ll11l1_opy_, bstack1lll1ll1l1_opy_, bstack111l1111_opy_, \
    bstack111ll1l11_opy_, bstack1llll1ll1_opy_, bstack111l11ll1_opy_, bstack1ll11111_opy_, bstack1l11l1l1l1_opy_, \
    bstack1111l1l1l_opy_, bstack1lllll11l1_opy_
from bstack_utils.proxy import bstack1l1lll1l1l_opy_, bstack1lll1ll1ll_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack1llllll11ll_opy_, bstack1lllll1llll_opy_, bstack1llllllll11_opy_, bstack1lllllll1ll_opy_, \
    bstack1llllll1ll1_opy_, bstack1lllllll1l1_opy_, bstack1llllll1111_opy_, bstack1lll1ll1_opy_, bstack1llllll1l1l_opy_
from bstack_utils.bstack1ll1l1ll1l_opy_ import bstack111l111l1_opy_
from bstack_utils.bstack1l1l11l1_opy_ import bstack1l11l1l11_opy_, bstack1l1lll1ll_opy_, bstack1ll1ll1ll1_opy_, \
    bstack1lllllll1_opy_, bstack11l11l11_opy_
from bstack_utils.bstack11llllll1l_opy_ import bstack1l1111ll1l_opy_
from bstack_utils.bstack111ll1l1l_opy_ import bstack1ll1l1l1l1_opy_
import bstack_utils.bstack1llll111_opy_ as bstack1l11lllll_opy_
from bstack_utils.bstack11111111_opy_ import bstack11111111_opy_
bstack1ll1l1l1l_opy_ = None
bstack1llll111l_opy_ = None
bstack11llllll1_opy_ = None
bstack1llll1l1l_opy_ = None
bstack1l1llll1l1_opy_ = None
bstack1ll11ll1ll_opy_ = None
bstack11l11111l_opy_ = None
bstack1llllllll1_opy_ = None
bstack1llll11l_opy_ = None
bstack1lll1l11_opy_ = None
bstack1llll1l11_opy_ = None
bstack1l1lll1111_opy_ = None
bstack1llll1ll_opy_ = None
bstack1lll1ll1l_opy_ = bstack1l1l1_opy_ (u"ࠨࠩᗅ")
CONFIG = {}
bstack11l11ll1l_opy_ = False
bstack1l1ll11l_opy_ = bstack1l1l1_opy_ (u"ࠩࠪᗆ")
bstack11l1lll1l_opy_ = bstack1l1l1_opy_ (u"ࠪࠫᗇ")
bstack111llllll_opy_ = False
bstack1lllll1l1_opy_ = []
bstack1llll11ll1_opy_ = bstack1ll1lll1l_opy_
bstack1lll11lll11_opy_ = bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᗈ")
bstack1lll11ll11l_opy_ = False
bstack1ll1111l1l_opy_ = {}
bstack1lll1llll1_opy_ = False
logger = bstack1lllll111l_opy_.get_logger(__name__, bstack1llll11ll1_opy_)
store = {
    bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗉ"): []
}
bstack1lll1l1lll1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111lll11_opy_ = {}
current_test_uuid = None
def bstack11l1ll11_opy_(page, bstack111111ll1_opy_):
    try:
        page.evaluate(bstack1l1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗊ"),
                      bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᗋ") + json.dumps(
                          bstack111111ll1_opy_) + bstack1l1l1_opy_ (u"ࠣࡿࢀࠦᗌ"))
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᗍ"), e)
def bstack111l111l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᗎ"), bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩᗏ") + json.dumps(
            message) + bstack1l1l1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨᗐ") + json.dumps(level) + bstack1l1l1_opy_ (u"࠭ࡽࡾࠩᗑ"))
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥᗒ"), e)
def pytest_configure(config):
    bstack11l11111_opy_ = Config.bstack1llllllll_opy_()
    config.args = bstack1ll1l1l1l1_opy_.bstack1lll1ll1l11_opy_(config.args)
    bstack11l11111_opy_.bstack1lll1l11l1_opy_(bstack111l11l1l_opy_(config.getoption(bstack1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᗓ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll1l1llll_opy_ = item.config.getoption(bstack1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᗔ"))
    plugins = item.config.getoption(bstack1l1l1_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦᗕ"))
    report = outcome.get_result()
    bstack1lll11lllll_opy_(item, call, report)
    if bstack1l1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤᗖ") not in plugins or bstack1l11l1l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l1_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨᗗ"), None)
    page = getattr(item, bstack1l1l1_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧᗘ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1l11lll_opy_(item, report, summary, bstack1lll1l1llll_opy_)
    if (page is not None):
        bstack1lll11l111l_opy_(item, report, summary, bstack1lll1l1llll_opy_)
def bstack1lll1l11lll_opy_(item, report, summary, bstack1lll1l1llll_opy_):
    if report.when == bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᗙ") and report.skipped:
        bstack1llllll1l1l_opy_(report)
    if report.when in [bstack1l1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗚ"), bstack1l1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᗛ")]:
        return
    if not bstack11l111llll_opy_():
        return
    try:
        if (str(bstack1lll1l1llll_opy_).lower() != bstack1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᗜ")):
            item._driver.execute_script(
                bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᗝ") + json.dumps(
                    report.nodeid) + bstack1l1l1_opy_ (u"ࠬࢃࡽࠨᗞ"))
        os.environ[bstack1l1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᗟ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᗠ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᗡ")))
    bstack1l1ll1ll_opy_ = bstack1l1l1_opy_ (u"ࠤࠥᗢ")
    bstack1llllll1l1l_opy_(report)
    if not passed:
        try:
            bstack1l1ll1ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᗣ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᗤ")))
        bstack1l1ll1ll_opy_ = bstack1l1l1_opy_ (u"ࠧࠨᗥ")
        if not passed:
            try:
                bstack1l1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᗦ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᗧ")
                    + json.dumps(bstack1l1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᗨ"))
                    + bstack1l1l1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᗩ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᗪ")
                    + json.dumps(str(bstack1l1ll1ll_opy_))
                    + bstack1l1l1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᗫ")
                )
        except Exception as e:
            summary.append(bstack1l1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᗬ").format(e))
def bstack1lll11ll1l1_opy_(test_name, error_message):
    try:
        bstack1lll11llll1_opy_ = []
        bstack1l1l1111_opy_ = os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᗭ"), bstack1l1l1_opy_ (u"ࠧ࠱ࠩᗮ"))
        bstack1lll11l11_opy_ = {bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗯ"): test_name, bstack1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᗰ"): error_message, bstack1l1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᗱ"): bstack1l1l1111_opy_}
        bstack1lll11l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᗲ"))
        if os.path.exists(bstack1lll11l11ll_opy_):
            with open(bstack1lll11l11ll_opy_) as f:
                bstack1lll11llll1_opy_ = json.load(f)
        bstack1lll11llll1_opy_.append(bstack1lll11l11_opy_)
        with open(bstack1lll11l11ll_opy_, bstack1l1l1_opy_ (u"ࠬࡽࠧᗳ")) as f:
            json.dump(bstack1lll11llll1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᗴ") + str(e))
def bstack1lll11l111l_opy_(item, report, summary, bstack1lll1l1llll_opy_):
    if report.when in [bstack1l1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᗵ"), bstack1l1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᗶ")]:
        return
    if (str(bstack1lll1l1llll_opy_).lower() != bstack1l1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᗷ")):
        bstack11l1ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗸ")))
    bstack1l1ll1ll_opy_ = bstack1l1l1_opy_ (u"ࠦࠧᗹ")
    bstack1llllll1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᗺ").format(e)
                )
        try:
            if passed:
                bstack11l11l11_opy_(getattr(item, bstack1l1l1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᗻ"), None), bstack1l1l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᗼ"))
            else:
                error_message = bstack1l1l1_opy_ (u"ࠨࠩᗽ")
                if bstack1l1ll1ll_opy_:
                    bstack111l111l_opy_(item._page, str(bstack1l1ll1ll_opy_), bstack1l1l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᗾ"))
                    bstack11l11l11_opy_(getattr(item, bstack1l1l1_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᗿ"), None), bstack1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘀ"), str(bstack1l1ll1ll_opy_))
                    error_message = str(bstack1l1ll1ll_opy_)
                else:
                    bstack11l11l11_opy_(getattr(item, bstack1l1l1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘁ"), None), bstack1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᘂ"))
                bstack1lll11ll1l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᘃ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l1l1_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᘄ"), default=bstack1l1l1_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᘅ"), help=bstack1l1l1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᘆ"))
    parser.addoption(bstack1l1l1_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᘇ"), default=bstack1l1l1_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᘈ"), help=bstack1l1l1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᘉ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l1_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᘊ"), action=bstack1l1l1_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᘋ"), default=bstack1l1l1_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᘌ"),
                         help=bstack1l1l1_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᘍ"))
def bstack1l111lll1l_opy_(log):
    if not (log[bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘎ")] and log[bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘏ")].strip()):
        return
    active = bstack1l111l11ll_opy_()
    log = {
        bstack1l1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘐ"): log[bstack1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᘑ")],
        bstack1l1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᘒ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫᘓ"),
        bstack1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘔ"): log[bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘕ")],
    }
    if active:
        if active[bstack1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪᘖ")] == bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᘗ"):
            log[bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘘ")] = active[bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘙ")]
        elif active[bstack1l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᘚ")] == bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨᘛ"):
            log[bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘜ")] = active[bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘝ")]
    bstack1ll1l1l1l1_opy_.bstack111lllll1_opy_([log])
def bstack1l111l11ll_opy_():
    if len(store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘞ")]) > 0 and store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᘟ")][-1]:
        return {
            bstack1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘠ"): bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᘡ"),
            bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘢ"): store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᘣ")][-1]
        }
    if store.get(bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᘤ"), None):
        return {
            bstack1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᘥ"): bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬᘦ"),
            bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘧ"): store[bstack1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᘨ")]
        }
    return None
bstack1l111lllll_opy_ = bstack1l111111ll_opy_(bstack1l111lll1l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll11ll11l_opy_
        item._1lll11ll111_opy_ = True
        bstack1l1ll1lll_opy_ = bstack1l11lllll_opy_.bstack1l111111l_opy_(CONFIG, bstack111lll111l_opy_(item.own_markers))
        item._a11y_test_case = bstack1l1ll1lll_opy_
        if bstack1lll11ll11l_opy_:
            driver = getattr(item, bstack1l1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᘩ"), None)
            item._a11y_started = bstack1l11lllll_opy_.bstack1111111ll_opy_(driver, bstack1l1ll1lll_opy_)
        if not bstack1ll1l1l1l1_opy_.on() or bstack1lll11lll11_opy_ != bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᘪ"):
            return
        global current_test_uuid, bstack1l111lllll_opy_
        bstack1l111lllll_opy_.start()
        bstack11lll1ll1l_opy_ = {
            bstack1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᘫ"): uuid4().__str__(),
            bstack1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘬ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"࡛ࠧࠩᘭ")
        }
        current_test_uuid = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘮ")]
        store[bstack1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᘯ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘰ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111lll11_opy_[item.nodeid] = {**_1l111lll11_opy_[item.nodeid], **bstack11lll1ll1l_opy_}
        bstack1lll1ll111l_opy_(item, _1l111lll11_opy_[item.nodeid], bstack1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘱ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᘲ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l1lll1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l1111_opy_():
        atexit.register(bstack1l111lll_opy_)
        if not bstack1lll1l1lll1_opy_:
            try:
                bstack1lll11l1l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l111l1ll_opy_():
                    bstack1lll11l1l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11l1l1l_opy_:
                    signal.signal(s, bstack1lll1ll11l1_opy_)
                bstack1lll1l1lll1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢᘳ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llllll11ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᘴ")
    try:
        if not bstack1ll1l1l1l1_opy_.on():
            return
        bstack1l111lllll_opy_.start()
        uuid = uuid4().__str__()
        bstack11lll1ll1l_opy_ = {
            bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘵ"): uuid,
            bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘶ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠪ࡞ࠬᘷ"),
            bstack1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᘸ"): bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᘹ"),
            bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᘺ"): bstack1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᘻ"),
            bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᘼ"): bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᘽ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᘾ")] = item
        store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᘿ")] = [uuid]
        if not _1l111lll11_opy_.get(item.nodeid, None):
            _1l111lll11_opy_[item.nodeid] = {bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙀ"): [], bstack1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᙁ"): []}
        _1l111lll11_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙂ")].append(bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᙃ")])
        _1l111lll11_opy_[item.nodeid + bstack1l1l1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᙄ")] = bstack11lll1ll1l_opy_
        bstack1lll11ll1ll_opy_(item, bstack11lll1ll1l_opy_, bstack1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙅ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᙆ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll1111l1l_opy_
        if CONFIG.get(bstack1l1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᙇ"), False):
            if CONFIG.get(bstack1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᙈ"), bstack1l1l1_opy_ (u"ࠢࡢࡷࡷࡳࠧᙉ")) == bstack1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᙊ"):
                bstack1lll11lll1l_opy_ = bstack1l11ll1ll_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᙋ"), None)
                bstack1ll1lll11_opy_ = bstack1lll11lll1l_opy_ + bstack1l1l1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᙌ")
                driver = getattr(item, bstack1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᙍ"), None)
                PercySDK.screenshot(driver, bstack1ll1lll11_opy_)
        if getattr(item, bstack1l1l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᙎ"), False):
            bstack11l111ll1_opy_.bstack1l1111l1l_opy_(getattr(item, bstack1l1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᙏ"), None), bstack1ll1111l1l_opy_, logger, item)
        if not bstack1ll1l1l1l1_opy_.on():
            return
        bstack11lll1ll1l_opy_ = {
            bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙐ"): uuid4().__str__(),
            bstack1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙑ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫᙒ"),
            bstack1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨᙓ"): bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙔ"),
            bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙕ"): bstack1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᙖ"),
            bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᙗ"): bstack1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᙘ")
        }
        _1l111lll11_opy_[item.nodeid + bstack1l1l1_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᙙ")] = bstack11lll1ll1l_opy_
        bstack1lll11ll1ll_opy_(item, bstack11lll1ll1l_opy_, bstack1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙚ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᙛ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1l1l1l1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lllllll1ll_opy_(fixturedef.argname):
        store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᙜ")] = request.node
    elif bstack1llllll1ll1_opy_(fixturedef.argname):
        store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᙝ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᙞ"): fixturedef.argname,
            bstack1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙟ"): bstack11l11l1lll_opy_(outcome),
            bstack1l1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᙠ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᙡ")]
        if not _1l111lll11_opy_.get(current_test_item.nodeid, None):
            _1l111lll11_opy_[current_test_item.nodeid] = {bstack1l1l1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙢ"): []}
        _1l111lll11_opy_[current_test_item.nodeid][bstack1l1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙣ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᙤ"), str(err))
if bstack1l11l1l1_opy_() and bstack1ll1l1l1l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111lll11_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙥ")].bstack1llll11lll1_opy_(id(step))
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᙦ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111lll11_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙧ")].bstack11llllll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᙨ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11llllll1l_opy_: bstack1l1111ll1l_opy_ = _1l111lll11_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᙩ")]
            bstack11llllll1l_opy_.bstack11llllll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᙪ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11lll11_opy_
        try:
            if not bstack1ll1l1l1l1_opy_.on() or bstack1lll11lll11_opy_ != bstack1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᙫ"):
                return
            global bstack1l111lllll_opy_
            bstack1l111lllll_opy_.start()
            driver = bstack1l11ll1ll_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᙬ"), None)
            if not _1l111lll11_opy_.get(request.node.nodeid, None):
                _1l111lll11_opy_[request.node.nodeid] = {}
            bstack11llllll1l_opy_ = bstack1l1111ll1l_opy_.bstack1llll1l11l1_opy_(
                scenario, feature, request.node,
                name=bstack1lllllll1l1_opy_(request.node, scenario),
                bstack11llll1l1l_opy_=bstack1lll1l1ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ᙭"),
                tags=bstack1llllll1111_opy_(feature, scenario),
                bstack11lllllll1_opy_=bstack1ll1l1l1l1_opy_.bstack1l1111ll11_opy_(driver) if driver and driver.session_id else {}
            )
            _1l111lll11_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ᙮")] = bstack11llllll1l_opy_
            bstack1lll1l1ll11_opy_(bstack11llllll1l_opy_.uuid)
            bstack1ll1l1l1l1_opy_.bstack1l11111lll_opy_(bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙯ"), bstack11llllll1l_opy_)
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᙰ"), str(err))
def bstack1lll1l1ll1l_opy_(bstack1lll1l1l111_opy_):
    if bstack1lll1l1l111_opy_ in store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙱ")]:
        store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᙲ")].remove(bstack1lll1l1l111_opy_)
def bstack1lll1l1ll11_opy_(bstack1lll1l1111l_opy_):
    store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᙳ")] = bstack1lll1l1111l_opy_
    threading.current_thread().current_test_uuid = bstack1lll1l1111l_opy_
@bstack1ll1l1l1l1_opy_.bstack1llll111ll1_opy_
def bstack1lll11lllll_opy_(item, call, report):
    global bstack1lll11lll11_opy_
    bstack1ll11ll1l1_opy_ = bstack1lll1l1ll1_opy_()
    if hasattr(report, bstack1l1l1_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᙴ")):
        bstack1ll11ll1l1_opy_ = bstack111llllll1_opy_(report.stop)
    if hasattr(report, bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᙵ")):
        bstack1ll11ll1l1_opy_ = bstack111llllll1_opy_(report.start)
    try:
        if getattr(report, bstack1l1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᙶ"), bstack1l1l1_opy_ (u"ࠫࠬᙷ")) == bstack1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᙸ"):
            bstack1l111lllll_opy_.reset()
        if getattr(report, bstack1l1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫᙹ"), bstack1l1l1_opy_ (u"ࠧࠨᙺ")) == bstack1l1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᙻ"):
            if bstack1lll11lll11_opy_ == bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᙼ"):
                _1l111lll11_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙽ")] = bstack1ll11ll1l1_opy_
                bstack1lll1ll111l_opy_(item, _1l111lll11_opy_[item.nodeid], bstack1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᙾ"), report, call)
                store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᙿ")] = None
            elif bstack1lll11lll11_opy_ == bstack1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ "):
                bstack11llllll1l_opy_ = _1l111lll11_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚁ")]
                bstack11llllll1l_opy_.set(hooks=_1l111lll11_opy_[item.nodeid].get(bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚂ"), []))
                exception, bstack1l111llll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l111llll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l1_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨᚃ"), bstack1l1l1_opy_ (u"ࠪࠫᚄ"))]
                bstack11llllll1l_opy_.stop(time=bstack1ll11ll1l1_opy_, result=Result(result=getattr(report, bstack1l1l1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᚅ"), bstack1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᚆ")), exception=exception, bstack1l111llll1_opy_=bstack1l111llll1_opy_))
                bstack1ll1l1l1l1_opy_.bstack1l11111lll_opy_(bstack1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᚇ"), _1l111lll11_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚈ")])
        elif getattr(report, bstack1l1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚉ"), bstack1l1l1_opy_ (u"ࠩࠪᚊ")) in [bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚋ"), bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᚌ")]:
            bstack1l11l11ll1_opy_ = item.nodeid + bstack1l1l1_opy_ (u"ࠬ࠳ࠧᚍ") + getattr(report, bstack1l1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫᚎ"), bstack1l1l1_opy_ (u"ࠧࠨᚏ"))
            if getattr(report, bstack1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᚐ"), False):
                hook_type = bstack1l1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᚑ") if getattr(report, bstack1l1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᚒ"), bstack1l1l1_opy_ (u"ࠫࠬᚓ")) == bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᚔ") else bstack1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᚕ")
                _1l111lll11_opy_[bstack1l11l11ll1_opy_] = {
                    bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚖ"): uuid4().__str__(),
                    bstack1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚗ"): bstack1ll11ll1l1_opy_,
                    bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᚘ"): hook_type
                }
            _1l111lll11_opy_[bstack1l11l11ll1_opy_][bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚙ")] = bstack1ll11ll1l1_opy_
            bstack1lll1l1ll1l_opy_(_1l111lll11_opy_[bstack1l11l11ll1_opy_][bstack1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᚚ")])
            bstack1lll11ll1ll_opy_(item, _1l111lll11_opy_[bstack1l11l11ll1_opy_], bstack1l1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᚛"), report, call)
            if getattr(report, bstack1l1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ᚜"), bstack1l1l1_opy_ (u"ࠧࠨ᚝")) == bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ᚞"):
                if getattr(report, bstack1l1l1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ᚟"), bstack1l1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚠ")) == bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚡ"):
                    bstack11lll1ll1l_opy_ = {
                        bstack1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᚢ"): uuid4().__str__(),
                        bstack1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚣ"): bstack1lll1l1ll1_opy_(),
                        bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚤ"): bstack1lll1l1ll1_opy_()
                    }
                    _1l111lll11_opy_[item.nodeid] = {**_1l111lll11_opy_[item.nodeid], **bstack11lll1ll1l_opy_}
                    bstack1lll1ll111l_opy_(item, _1l111lll11_opy_[item.nodeid], bstack1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᚥ"))
                    bstack1lll1ll111l_opy_(item, _1l111lll11_opy_[item.nodeid], bstack1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚦ"), report, call)
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᚧ"), str(err))
def bstack1lll11l11l1_opy_(test, bstack11lll1ll1l_opy_, result=None, call=None, bstack1lll1ll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11llllll1l_opy_ = {
        bstack1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᚨ"): bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᚩ")],
        bstack1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᚪ"): bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬᚫ"),
        bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚬ"): test.name,
        bstack1l1l1_opy_ (u"ࠩࡥࡳࡩࡿࠧᚭ"): {
            bstack1l1l1_opy_ (u"ࠪࡰࡦࡴࡧࠨᚮ"): bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᚯ"),
            bstack1l1l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᚰ"): inspect.getsource(test.obj)
        },
        bstack1l1l1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚱ"): test.name,
        bstack1l1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᚲ"): test.name,
        bstack1l1l1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᚳ"): bstack1ll1l1l1l1_opy_.bstack1l11l11111_opy_(test),
        bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᚴ"): file_path,
        bstack1l1l1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᚵ"): file_path,
        bstack1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᚶ"): bstack1l1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᚷ"),
        bstack1l1l1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᚸ"): file_path,
        bstack1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚹ"): bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚺ")],
        bstack1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᚻ"): bstack1l1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᚼ"),
        bstack1l1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᚽ"): {
            bstack1l1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᚾ"): test.nodeid
        },
        bstack1l1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫᚿ"): bstack111lll111l_opy_(test.own_markers)
    }
    if bstack1lll1ll111_opy_ in [bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᛀ"), bstack1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᛁ")]:
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠩࡰࡩࡹࡧࠧᛂ")] = {
            bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᛃ"): bstack11lll1ll1l_opy_.get(bstack1l1l1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᛄ"), [])
        }
    if bstack1lll1ll111_opy_ == bstack1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᛅ"):
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛆ")] = bstack1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛇ")
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛈ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛉ")]
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛊ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛋ")]
    if result:
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛌ")] = result.outcome
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᛍ")] = result.duration * 1000
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛎ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛏ")]
        if result.failed:
            bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᛐ")] = bstack1ll1l1l1l1_opy_.bstack11ll1l1ll1_opy_(call.excinfo.typename)
            bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᛑ")] = bstack1ll1l1l1l1_opy_.bstack1lll1ll1lll_opy_(call.excinfo, result)
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛒ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᛓ")]
    if outcome:
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛔ")] = bstack11l11l1lll_opy_(outcome)
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᛕ")] = 0
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛖ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛗ")]
        if bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛘ")] == bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛙ"):
            bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᛚ")] = bstack1l1l1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᛛ")  # bstack1lll11l1lll_opy_
            bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᛜ")] = [{bstack1l1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᛝ"): [bstack1l1l1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᛞ")]}]
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛟ")] = bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛠ")]
    return bstack11llllll1l_opy_
def bstack1lll1l111l1_opy_(test, bstack1l111l1ll1_opy_, bstack1lll1ll111_opy_, result, call, outcome, bstack1lll11l1ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᛡ")]
    hook_name = bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᛢ")]
    hook_data = {
        bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛣ"): bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᛤ")],
        bstack1l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᛥ"): bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᛦ"),
        bstack1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᛧ"): bstack1l1l1_opy_ (u"ࠬࢁࡽࠨᛨ").format(bstack1lllll1llll_opy_(hook_name)),
        bstack1l1l1_opy_ (u"࠭ࡢࡰࡦࡼࠫᛩ"): {
            bstack1l1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᛪ"): bstack1l1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᛫"),
            bstack1l1l1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ᛬"): None
        },
        bstack1l1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ᛭"): test.name,
        bstack1l1l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᛮ"): bstack1ll1l1l1l1_opy_.bstack1l11l11111_opy_(test, hook_name),
        bstack1l1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᛯ"): file_path,
        bstack1l1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᛰ"): file_path,
        bstack1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛱ"): bstack1l1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᛲ"),
        bstack1l1l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᛳ"): file_path,
        bstack1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᛴ"): bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᛵ")],
        bstack1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᛶ"): bstack1l1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᛷ") if bstack1lll11lll11_opy_ == bstack1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᛸ") else bstack1l1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ᛹"),
        bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᛺"): hook_type
    }
    bstack1lll1l1l1ll_opy_ = bstack11llll11ll_opy_(_1l111lll11_opy_.get(test.nodeid, None))
    if bstack1lll1l1l1ll_opy_:
        hook_data[bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ᛻")] = bstack1lll1l1l1ll_opy_
    if result:
        hook_data[bstack1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᛼")] = result.outcome
        hook_data[bstack1l1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᛽")] = result.duration * 1000
        hook_data[bstack1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᛾")] = bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᛿")]
        if result.failed:
            hook_data[bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᜀ")] = bstack1ll1l1l1l1_opy_.bstack11ll1l1ll1_opy_(call.excinfo.typename)
            hook_data[bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᜁ")] = bstack1ll1l1l1l1_opy_.bstack1lll1ll1lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜂ")] = bstack11l11l1lll_opy_(outcome)
        hook_data[bstack1l1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᜃ")] = 100
        hook_data[bstack1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜄ")] = bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜅ")]
        if hook_data[bstack1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᜆ")] == bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜇ"):
            hook_data[bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᜈ")] = bstack1l1l1_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᜉ")  # bstack1lll11l1lll_opy_
            hook_data[bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜊ")] = [{bstack1l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᜋ"): [bstack1l1l1_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᜌ")]}]
    if bstack1lll11l1ll1_opy_:
        hook_data[bstack1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᜍ")] = bstack1lll11l1ll1_opy_.result
        hook_data[bstack1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᜎ")] = bstack11l11l1l11_opy_(bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜏ")], bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜐ")])
        hook_data[bstack1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜑ")] = bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜒ")]
        if hook_data[bstack1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜓ")] == bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ᜔ࠧ"):
            hook_data[bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫᜕ࠧ")] = bstack1ll1l1l1l1_opy_.bstack11ll1l1ll1_opy_(bstack1lll11l1ll1_opy_.exception_type)
            hook_data[bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᜖")] = [{bstack1l1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᜗"): bstack111ll1lll1_opy_(bstack1lll11l1ll1_opy_.exception)}]
    return hook_data
def bstack1lll1ll111l_opy_(test, bstack11lll1ll1l_opy_, bstack1lll1ll111_opy_, result=None, call=None, outcome=None):
    bstack11llllll1l_opy_ = bstack1lll11l11l1_opy_(test, bstack11lll1ll1l_opy_, result, call, bstack1lll1ll111_opy_, outcome)
    driver = getattr(test, bstack1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᜘"), None)
    if bstack1lll1ll111_opy_ == bstack1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᜙") and driver:
        bstack11llllll1l_opy_[bstack1l1l1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ᜚")] = bstack1ll1l1l1l1_opy_.bstack1l1111ll11_opy_(driver)
    if bstack1lll1ll111_opy_ == bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ᜛"):
        bstack1lll1ll111_opy_ = bstack1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᜜")
    bstack1l111l1111_opy_ = {
        bstack1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜝"): bstack1lll1ll111_opy_,
        bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᜞"): bstack11llllll1l_opy_
    }
    bstack1ll1l1l1l1_opy_.bstack1l111ll1l1_opy_(bstack1l111l1111_opy_)
def bstack1lll11ll1ll_opy_(test, bstack11lll1ll1l_opy_, bstack1lll1ll111_opy_, result=None, call=None, outcome=None, bstack1lll11l1ll1_opy_=None):
    hook_data = bstack1lll1l111l1_opy_(test, bstack11lll1ll1l_opy_, bstack1lll1ll111_opy_, result, call, outcome, bstack1lll11l1ll1_opy_)
    bstack1l111l1111_opy_ = {
        bstack1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜟ"): bstack1lll1ll111_opy_,
        bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᜠ"): hook_data
    }
    bstack1ll1l1l1l1_opy_.bstack1l111ll1l1_opy_(bstack1l111l1111_opy_)
def bstack11llll11ll_opy_(bstack11lll1ll1l_opy_):
    if not bstack11lll1ll1l_opy_:
        return None
    if bstack11lll1ll1l_opy_.get(bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᜡ"), None):
        return getattr(bstack11lll1ll1l_opy_[bstack1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᜢ")], bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᜣ"), None)
    return bstack11lll1ll1l_opy_.get(bstack1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜤ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1l1l1l1_opy_.on():
            return
        places = [bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᜥ"), bstack1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᜦ"), bstack1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᜧ")]
        bstack1l111l1l11_opy_ = []
        for bstack1lll1l11111_opy_ in places:
            records = caplog.get_records(bstack1lll1l11111_opy_)
            bstack1lll1l11ll1_opy_ = bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜨ") if bstack1lll1l11111_opy_ == bstack1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᜩ") else bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜪ")
            bstack1lll1l1l1l1_opy_ = request.node.nodeid + (bstack1l1l1_opy_ (u"ࠩࠪᜫ") if bstack1lll1l11111_opy_ == bstack1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᜬ") else bstack1l1l1_opy_ (u"ࠫ࠲࠭ᜭ") + bstack1lll1l11111_opy_)
            bstack1lll1l1111l_opy_ = bstack11llll11ll_opy_(_1l111lll11_opy_.get(bstack1lll1l1l1l1_opy_, None))
            if not bstack1lll1l1111l_opy_:
                continue
            for record in records:
                if bstack11l1111111_opy_(record.message):
                    continue
                bstack1l111l1l11_opy_.append({
                    bstack1l1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᜮ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1l1l1_opy_ (u"࡚࠭ࠨᜯ"),
                    bstack1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᜰ"): record.levelname,
                    bstack1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜱ"): record.message,
                    bstack1lll1l11ll1_opy_: bstack1lll1l1111l_opy_
                })
        if len(bstack1l111l1l11_opy_) > 0:
            bstack1ll1l1l1l1_opy_.bstack111lllll1_opy_(bstack1l111l1l11_opy_)
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ᜲ"), str(err))
def bstack111ll1lll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1lll1llll1_opy_
    bstack1l11111ll_opy_ = bstack1l11ll1ll_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᜳ"), None) and bstack1l11ll1ll_opy_(
            threading.current_thread(), bstack1l1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯᜴ࠪ"), None)
    bstack1l1l1l11l1_opy_ = getattr(driver, bstack1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ᜵"), None) != None and getattr(driver, bstack1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭᜶"), None) == True
    if sequence == bstack1l1l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ᜷") and driver != None:
      if not bstack1lll1llll1_opy_ and bstack11l111llll_opy_() and bstack1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜸") in CONFIG and CONFIG[bstack1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᜹")] == True and bstack11111111_opy_.bstack1lll11ll11_opy_(driver_command) and (bstack1l1l1l11l1_opy_ or bstack1l11111ll_opy_) and not bstack11l11l111_opy_(args):
        try:
          bstack1lll1llll1_opy_ = True
          logger.debug(bstack1l1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ᜺").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ᜻").format(str(err)))
        bstack1lll1llll1_opy_ = False
    if sequence == bstack1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᜼"):
        if driver_command == bstack1l1l1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ᜽"):
            bstack1ll1l1l1l1_opy_.bstack1l1l111l11_opy_({
                bstack1l1l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭᜾"): response[bstack1l1l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ᜿")],
                bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᝀ"): store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᝁ")]
            })
def bstack1l111lll_opy_():
    global bstack1lllll1l1_opy_
    bstack1lllll111l_opy_.bstack11l1l111l_opy_()
    logging.shutdown()
    bstack1ll1l1l1l1_opy_.bstack11lllll11l_opy_()
    for driver in bstack1lllll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1ll11l1_opy_(*args):
    global bstack1lllll1l1_opy_
    bstack1ll1l1l1l1_opy_.bstack11lllll11l_opy_()
    for driver in bstack1lllll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1111ll1_opy_(self, *args, **kwargs):
    bstack1ll11lllll_opy_ = bstack1ll1l1l1l_opy_(self, *args, **kwargs)
    bstack1ll1l1l1l1_opy_.bstack11l1l11l_opy_(self)
    return bstack1ll11lllll_opy_
def bstack1ll1llll1_opy_(framework_name):
    global bstack1lll1ll1l_opy_
    global bstack11ll11111_opy_
    bstack1lll1ll1l_opy_ = framework_name
    logger.info(bstack1lllll11l1_opy_.format(bstack1lll1ll1l_opy_.split(bstack1l1l1_opy_ (u"ࠫ࠲࠭ᝂ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l111llll_opy_():
            Service.start = bstack1l11l11l1_opy_
            Service.stop = bstack1ll1111l11_opy_
            webdriver.Remote.__init__ = bstack1ll111l1_opy_
            webdriver.Remote.get = bstack111l1l11l_opy_
            if not isinstance(os.getenv(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᝃ")), str):
                return
            WebDriver.close = bstack1l11l1l11l_opy_
            WebDriver.quit = bstack1llll1lll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11l111llll_opy_() and bstack1ll1l1l1l1_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1111ll1_opy_
        bstack11ll11111_opy_ = True
    except Exception as e:
        pass
    bstack1ll111l1l_opy_()
    if os.environ.get(bstack1l1l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᝄ")):
        bstack11ll11111_opy_ = eval(os.environ.get(bstack1l1l1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᝅ")))
    if not bstack11ll11111_opy_:
        bstack1ll1lll111_opy_(bstack1l1l1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᝆ"), bstack1111l1l1l_opy_)
    if bstack11l1ll11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11ll1ll1l_opy_
        except Exception as e:
            logger.error(bstack111ll1l11_opy_.format(str(e)))
    if bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᝇ") in str(framework_name).lower():
        if not bstack11l111llll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11l11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll11llll_opy_
            Config.getoption = bstack111l1l111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll1l111_opy_
        except Exception as e:
            pass
def bstack1llll1lll_opy_(self):
    global bstack1lll1ll1l_opy_
    global bstack1ll1lll1_opy_
    global bstack1llll111l_opy_
    try:
        if bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᝈ") in bstack1lll1ll1l_opy_ and self.session_id != None and bstack1l11ll1ll_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᝉ"), bstack1l1l1_opy_ (u"ࠬ࠭ᝊ")) != bstack1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᝋ"):
            bstack11llll1ll_opy_ = bstack1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᝌ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᝍ")
            bstack1l1llll1_opy_(logger, True)
            if self != None:
                bstack1lllllll1_opy_(self, bstack11llll1ll_opy_, bstack1l1l1_opy_ (u"ࠩ࠯ࠤࠬᝎ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᝏ"), None)
        if item is not None and bstack1lll11ll11l_opy_:
            bstack11l111ll1_opy_.bstack1l1111l1l_opy_(self, bstack1ll1111l1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l1_opy_ (u"ࠫࠬᝐ")
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᝑ") + str(e))
    bstack1llll111l_opy_(self)
    self.session_id = None
def bstack1ll111l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1lll1_opy_
    global bstack111l1ll1_opy_
    global bstack111llllll_opy_
    global bstack1lll1ll1l_opy_
    global bstack1ll1l1l1l_opy_
    global bstack1lllll1l1_opy_
    global bstack1l1ll11l_opy_
    global bstack11l1lll1l_opy_
    global bstack1lll11ll11l_opy_
    global bstack1ll1111l1l_opy_
    CONFIG[bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᝒ")] = str(bstack1lll1ll1l_opy_) + str(__version__)
    command_executor = bstack1l1lll1lll_opy_(bstack1l1ll11l_opy_)
    logger.debug(bstack1lll1ll1l1_opy_.format(command_executor))
    proxy = bstack11lllll11_opy_(CONFIG, proxy)
    bstack1l1l1111_opy_ = 0
    try:
        if bstack111llllll_opy_ is True:
            bstack1l1l1111_opy_ = int(os.environ.get(bstack1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᝓ")))
    except:
        bstack1l1l1111_opy_ = 0
    bstack1lll1l11l_opy_ = bstack1l1ll11l1_opy_(CONFIG, bstack1l1l1111_opy_)
    logger.debug(bstack111l11ll1_opy_.format(str(bstack1lll1l11l_opy_)))
    bstack1ll1111l1l_opy_ = CONFIG.get(bstack1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᝔"))[bstack1l1l1111_opy_]
    if bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᝕") in CONFIG and CONFIG[bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᝖")]:
        bstack1ll1ll1ll1_opy_(bstack1lll1l11l_opy_, bstack11l1lll1l_opy_)
    if bstack1l11lllll_opy_.bstack11l11l1l_opy_(CONFIG, bstack1l1l1111_opy_) and bstack1l11lllll_opy_.bstack1l1l11llll_opy_(bstack1lll1l11l_opy_, options):
        bstack1lll11ll11l_opy_ = True
        bstack1l11lllll_opy_.set_capabilities(bstack1lll1l11l_opy_, CONFIG)
    if desired_capabilities:
        bstack1111l1ll_opy_ = bstack11l1l1l1_opy_(desired_capabilities)
        bstack1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᝗")] = bstack1ll1lll1ll_opy_(CONFIG)
        bstack1l1ll11l1l_opy_ = bstack1l1ll11l1_opy_(bstack1111l1ll_opy_)
        if bstack1l1ll11l1l_opy_:
            bstack1lll1l11l_opy_ = update(bstack1l1ll11l1l_opy_, bstack1lll1l11l_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1l1ll_opy_(options, bstack1lll1l11l_opy_)
    if not options:
        options = bstack1llll11l1l_opy_(bstack1lll1l11l_opy_)
    if proxy and bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ᝘")):
        options.proxy(proxy)
    if options and bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ᝙")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1111111l1_opy_() < version.parse(bstack1l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭᝚")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll1l11l_opy_)
    logger.info(bstack1l11ll11l1_opy_)
    if bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᝛")):
        bstack1ll1l1l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᝜")):
        bstack1ll1l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ᝝")):
        bstack1ll1l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1ll1l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1l1l1_opy_ = bstack1l1l1_opy_ (u"ࠫࠬ᝞")
        if bstack1111111l1_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭᝟")):
            bstack1llll1l1l1_opy_ = self.caps.get(bstack1l1l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᝠ"))
        else:
            bstack1llll1l1l1_opy_ = self.capabilities.get(bstack1l1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᝡ"))
        if bstack1llll1l1l1_opy_:
            bstack11ll1lll1_opy_(bstack1llll1l1l1_opy_)
            if bstack1111111l1_opy_() <= version.parse(bstack1l1l1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᝢ")):
                self.command_executor._url = bstack1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᝣ") + bstack1l1ll11l_opy_ + bstack1l1l1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᝤ")
            else:
                self.command_executor._url = bstack1l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᝥ") + bstack1llll1l1l1_opy_ + bstack1l1l1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᝦ")
            logger.debug(bstack1lll11ll1_opy_.format(bstack1llll1l1l1_opy_))
        else:
            logger.debug(bstack1lll1lll_opy_.format(bstack1l1l1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᝧ")))
    except Exception as e:
        logger.debug(bstack1lll1lll_opy_.format(e))
    bstack1ll1lll1_opy_ = self.session_id
    if bstack1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᝨ") in bstack1lll1ll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᝩ"), None)
        if item:
            bstack1lll1ll11ll_opy_ = getattr(item, bstack1l1l1_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧᝪ"), False)
            if not getattr(item, bstack1l1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᝫ"), None) and bstack1lll1ll11ll_opy_:
                setattr(store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᝬ")], bstack1l1l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᝭"), self)
        bstack1ll1l1l1l1_opy_.bstack11l1l11l_opy_(self)
    bstack1lllll1l1_opy_.append(self)
    if bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᝮ") in CONFIG and bstack1l1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᝯ") in CONFIG[bstack1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᝰ")][bstack1l1l1111_opy_]:
        bstack111l1ll1_opy_ = CONFIG[bstack1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᝱")][bstack1l1l1111_opy_][bstack1l1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᝲ")]
    logger.debug(bstack1l11l1l1l1_opy_.format(bstack1ll1lll1_opy_))
def bstack111l1l11l_opy_(self, url):
    global bstack1llll11l_opy_
    global CONFIG
    try:
        bstack1l1lll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll11111_opy_.format(str(err)))
    try:
        bstack1llll11l_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll11111l_opy_ = str(e)
            if any(err_msg in bstack1ll11111l_opy_ for err_msg in bstack1lll11lll_opy_):
                bstack1l1lll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll11111_opy_.format(str(err)))
        raise e
def bstack1l1l11111_opy_(item, when):
    global bstack1l1lll1111_opy_
    try:
        bstack1l1lll1111_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l111_opy_(item, call, rep):
    global bstack1llll1ll_opy_
    global bstack1lllll1l1_opy_
    name = bstack1l1l1_opy_ (u"ࠫࠬᝳ")
    try:
        if rep.when == bstack1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᝴"):
            bstack1ll1lll1_opy_ = threading.current_thread().bstackSessionId
            bstack1lll1l1llll_opy_ = item.config.getoption(bstack1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᝵"))
            try:
                if (str(bstack1lll1l1llll_opy_).lower() != bstack1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ᝶")):
                    name = str(rep.nodeid)
                    bstack1l1l111lll_opy_ = bstack1l11l1l11_opy_(bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᝷"), name, bstack1l1l1_opy_ (u"ࠩࠪ᝸"), bstack1l1l1_opy_ (u"ࠪࠫ᝹"), bstack1l1l1_opy_ (u"ࠫࠬ᝺"), bstack1l1l1_opy_ (u"ࠬ࠭᝻"))
                    os.environ[bstack1l1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ᝼")] = name
                    for driver in bstack1lllll1l1_opy_:
                        if bstack1ll1lll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l111lll_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ᝽").format(str(e)))
            try:
                bstack1lll1ll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᝾"):
                    status = bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᝿") if rep.outcome.lower() == bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪក") else bstack1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫខ")
                    reason = bstack1l1l1_opy_ (u"ࠬ࠭គ")
                    if status == bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ឃ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬង") if status == bstack1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨច") else bstack1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨឆ")
                    data = name + bstack1l1l1_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬជ") if status == bstack1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫឈ") else name + bstack1l1l1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨញ") + reason
                    bstack1ll11ll111_opy_ = bstack1l11l1l11_opy_(bstack1l1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨដ"), bstack1l1l1_opy_ (u"ࠧࠨឋ"), bstack1l1l1_opy_ (u"ࠨࠩឌ"), bstack1l1l1_opy_ (u"ࠩࠪឍ"), level, data)
                    for driver in bstack1lllll1l1_opy_:
                        if bstack1ll1lll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11ll111_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧណ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨត").format(str(e)))
    bstack1llll1ll_opy_(item, call, rep)
notset = Notset()
def bstack111l1l111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll1l11_opy_
    if str(name).lower() == bstack1l1l1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬថ"):
        return bstack1l1l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧទ")
    else:
        return bstack1llll1l11_opy_(self, name, default, skip)
def bstack11ll1ll1l_opy_(self):
    global CONFIG
    global bstack11l11111l_opy_
    try:
        proxy = bstack1l1lll1l1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬធ")):
                proxies = bstack1lll1ll1ll_opy_(proxy, bstack1l1lll1lll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll11111l_opy_ = proxies.popitem()
                    if bstack1l1l1_opy_ (u"ࠣ࠼࠲࠳ࠧន") in bstack1lll11111l_opy_:
                        return bstack1lll11111l_opy_
                    else:
                        return bstack1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥប") + bstack1lll11111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢផ").format(str(e)))
    return bstack11l11111l_opy_(self)
def bstack11l1ll11l_opy_():
    return (bstack1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧព") in CONFIG or bstack1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩភ") in CONFIG) and bstack1ll1111l_opy_() and bstack1111111l1_opy_() >= version.parse(
        bstack11l11l1l1_opy_)
def bstack1ll1llll1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack111l1ll1_opy_
    global bstack111llllll_opy_
    global bstack1lll1ll1l_opy_
    CONFIG[bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨម")] = str(bstack1lll1ll1l_opy_) + str(__version__)
    bstack1l1l1111_opy_ = 0
    try:
        if bstack111llllll_opy_ is True:
            bstack1l1l1111_opy_ = int(os.environ.get(bstack1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧយ")))
    except:
        bstack1l1l1111_opy_ = 0
    CONFIG[bstack1l1l1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢរ")] = True
    bstack1lll1l11l_opy_ = bstack1l1ll11l1_opy_(CONFIG, bstack1l1l1111_opy_)
    logger.debug(bstack111l11ll1_opy_.format(str(bstack1lll1l11l_opy_)))
    if CONFIG.get(bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ល")):
        bstack1ll1ll1ll1_opy_(bstack1lll1l11l_opy_, bstack11l1lll1l_opy_)
    if bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭វ") in CONFIG and bstack1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩឝ") in CONFIG[bstack1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឞ")][bstack1l1l1111_opy_]:
        bstack111l1ll1_opy_ = CONFIG[bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩស")][bstack1l1l1111_opy_][bstack1l1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬហ")]
    import urllib
    import json
    bstack1ll1l1111_opy_ = bstack1l1l1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪឡ") + urllib.parse.quote(json.dumps(bstack1lll1l11l_opy_))
    browser = self.connect(bstack1ll1l1111_opy_)
    return browser
def bstack1ll111l1l_opy_():
    global bstack11ll11111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1llll1l_opy_
        bstack11ll11111_opy_ = True
    except Exception as e:
        pass
def bstack1lll1l1l11l_opy_():
    global CONFIG
    global bstack11l11ll1l_opy_
    global bstack1l1ll11l_opy_
    global bstack11l1lll1l_opy_
    global bstack111llllll_opy_
    global bstack1llll11ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨអ")))
    bstack11l11ll1l_opy_ = eval(os.environ.get(bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫឣ")))
    bstack1l1ll11l_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫឤ"))
    bstack11l1ll111_opy_(CONFIG, bstack11l11ll1l_opy_)
    bstack1llll11ll1_opy_ = bstack1lllll111l_opy_.bstack11l11ll11_opy_(CONFIG, bstack1llll11ll1_opy_)
    global bstack1ll1l1l1l_opy_
    global bstack1llll111l_opy_
    global bstack11llllll1_opy_
    global bstack1llll1l1l_opy_
    global bstack1l1llll1l1_opy_
    global bstack1ll11ll1ll_opy_
    global bstack1llllllll1_opy_
    global bstack1llll11l_opy_
    global bstack11l11111l_opy_
    global bstack1llll1l11_opy_
    global bstack1l1lll1111_opy_
    global bstack1llll1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll1l1l1l_opy_ = webdriver.Remote.__init__
        bstack1llll111l_opy_ = WebDriver.quit
        bstack1llllllll1_opy_ = WebDriver.close
        bstack1llll11l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨឥ") in CONFIG or bstack1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪឦ") in CONFIG) and bstack1ll1111l_opy_():
        if bstack1111111l1_opy_() < version.parse(bstack11l11l1l1_opy_):
            logger.error(bstack1llll1ll1_opy_.format(bstack1111111l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11l11111l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack111ll1l11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll1l11_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1lll1111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111l1111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨឧ"))
    bstack11l1lll1l_opy_ = CONFIG.get(bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬឨ"), {}).get(bstack1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫឩ"))
    bstack111llllll_opy_ = True
    bstack1ll1llll1_opy_(bstack11ll111ll_opy_)
if (bstack11l11l1111_opy_()):
    bstack1lll1l1l11l_opy_()
@bstack1l1111l1ll_opy_(class_method=False)
def bstack1lll11l1l11_opy_(hook_name, event, bstack1lll1l111ll_opy_=None):
    if hook_name not in [bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫឪ"), bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨឫ"), bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឬ"), bstack1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨឭ"), bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬឮ"), bstack1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩឯ"), bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨឰ"), bstack1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬឱ")]:
        return
    node = store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨឲ")]
    if hook_name in [bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឳ"), bstack1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ឴")]:
        node = store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭឵")]
    elif hook_name in [bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ា"), bstack1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪិ")]:
        node = store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨី")]
    if event == bstack1l1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫឹ"):
        hook_type = bstack1llllllll11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l111l1ll1_opy_ = {
            bstack1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪឺ"): uuid,
            bstack1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪុ"): bstack1lll1l1ll1_opy_(),
            bstack1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬូ"): bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ួ"),
            bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬើ"): hook_type,
            bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ឿ"): hook_name
        }
        store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨៀ")].append(uuid)
        bstack1lll1ll1111_opy_ = node.nodeid
        if hook_type == bstack1l1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪេ"):
            if not _1l111lll11_opy_.get(bstack1lll1ll1111_opy_, None):
                _1l111lll11_opy_[bstack1lll1ll1111_opy_] = {bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬែ"): []}
            _1l111lll11_opy_[bstack1lll1ll1111_opy_][bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ៃ")].append(bstack1l111l1ll1_opy_[bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ោ")])
        _1l111lll11_opy_[bstack1lll1ll1111_opy_ + bstack1l1l1_opy_ (u"ࠩ࠰ࠫៅ") + hook_name] = bstack1l111l1ll1_opy_
        bstack1lll11ll1ll_opy_(node, bstack1l111l1ll1_opy_, bstack1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫំ"))
    elif event == bstack1l1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪះ"):
        bstack1l11l11ll1_opy_ = node.nodeid + bstack1l1l1_opy_ (u"ࠬ࠳ࠧៈ") + hook_name
        _1l111lll11_opy_[bstack1l11l11ll1_opy_][bstack1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ៉")] = bstack1lll1l1ll1_opy_()
        bstack1lll1l1ll1l_opy_(_1l111lll11_opy_[bstack1l11l11ll1_opy_][bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៊")])
        bstack1lll11ll1ll_opy_(node, _1l111lll11_opy_[bstack1l11l11ll1_opy_], bstack1l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ់"), bstack1lll11l1ll1_opy_=bstack1lll1l111ll_opy_)
def bstack1lll1l11l11_opy_():
    global bstack1lll11lll11_opy_
    if bstack1l11l1l1_opy_():
        bstack1lll11lll11_opy_ = bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭៌")
    else:
        bstack1lll11lll11_opy_ = bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ៍")
@bstack1ll1l1l1l1_opy_.bstack1llll111ll1_opy_
def bstack1lll1l11l1l_opy_():
    bstack1lll1l11l11_opy_()
    if bstack1ll1111l_opy_():
        bstack111l111l1_opy_(bstack111ll1lll_opy_)
    bstack111l1llll1_opy_ = bstack111ll1111l_opy_(bstack1lll11l1l11_opy_)
bstack1lll1l11l1l_opy_()