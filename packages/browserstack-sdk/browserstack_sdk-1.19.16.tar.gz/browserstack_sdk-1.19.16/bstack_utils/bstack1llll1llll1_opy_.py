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
import threading
bstack1lllll11111_opy_ = 1000
bstack1llll1ll1ll_opy_ = 5
bstack1llll1lll11_opy_ = 30
bstack1lllll111l1_opy_ = 2
class bstack1llll1ll11l_opy_:
    def __init__(self, handler, bstack1llll1lllll_opy_=bstack1lllll11111_opy_, bstack1lllll111ll_opy_=bstack1llll1ll1ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llll1lllll_opy_ = bstack1llll1lllll_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1llll1ll111_opy_()
    def bstack1llll1ll111_opy_(self):
        self.timer = threading.Timer(self.bstack1lllll111ll_opy_, self.bstack1llll1ll1l1_opy_)
        self.timer.start()
    def bstack1lllll1111l_opy_(self):
        self.timer.cancel()
    def bstack1llll1lll1l_opy_(self):
        self.bstack1lllll1111l_opy_()
        self.bstack1llll1ll111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llll1lllll_opy_:
                t = threading.Thread(target=self.bstack1llll1ll1l1_opy_)
                t.start()
                self.bstack1llll1lll1l_opy_()
    def bstack1llll1ll1l1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1llll1lllll_opy_]
        del self.queue[:self.bstack1llll1lllll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lllll1111l_opy_()
        while len(self.queue) > 0:
            self.bstack1llll1ll1l1_opy_()