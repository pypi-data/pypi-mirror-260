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
import threading
bstack1lllll1ll1l_opy_ = 1000
bstack1lllll1l11l_opy_ = 5
bstack1lllll11lll_opy_ = 30
bstack1lllll1l111_opy_ = 2
class bstack1lllll11l1l_opy_:
    def __init__(self, handler, bstack1lllll1l1l1_opy_=bstack1lllll1ll1l_opy_, bstack1lllll1ll11_opy_=bstack1lllll1l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllll1l1l1_opy_ = bstack1lllll1l1l1_opy_
        self.bstack1lllll1ll11_opy_ = bstack1lllll1ll11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lllll11l11_opy_()
    def bstack1lllll11l11_opy_(self):
        self.timer = threading.Timer(self.bstack1lllll1ll11_opy_, self.bstack1lllll11ll1_opy_)
        self.timer.start()
    def bstack1lllll111ll_opy_(self):
        self.timer.cancel()
    def bstack1lllll1l1ll_opy_(self):
        self.bstack1lllll111ll_opy_()
        self.bstack1lllll11l11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllll1l1l1_opy_:
                t = threading.Thread(target=self.bstack1lllll11ll1_opy_)
                t.start()
                self.bstack1lllll1l1ll_opy_()
    def bstack1lllll11ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lllll1l1l1_opy_]
        del self.queue[:self.bstack1lllll1l1l1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lllll111ll_opy_()
        while len(self.queue) > 0:
            self.bstack1lllll11ll1_opy_()