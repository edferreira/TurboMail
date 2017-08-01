# encoding: utf-8

"""On-demand threaded queue manager.

Worker threads are spawned based on demand at the time a message is added to the queue."""


import copy
import logging
import math

from Queue import Queue, Empty
from threading import Event, Thread

from turbomail.api import Manager
from turbomail.exceptions import TransportExhaustedException
from turbomail.control import interface


__all__ = ['load']

log = logging.getLogger("turbomail.manager")
debuglog = logging.getLogger("turbomail.debug")



def load():
    return DemandManager()


class DemandManager(Manager):
    name = "demand"

    def __init__(self):
        log.info("Demand manager starting up.")
        super(DemandManager, self).__init__()

        self.pool = 0
        self.queue = Queue()
        self.finished = Event()

        self.threads = interface.config.get("mail.demand.threads", 4) # Maximum number of threads to create.
        self.divisor = interface.config.get("mail.demand.divisor", 10) # Estimate the number of required threads by dividing the queue size by this.
        self.timeout = interface.config.get("mail.demand.timeout", 60)

        debuglog.debug("DemandManager started with: %s threads, %s divisor, %s timeout" % (self.threads, self.divisor, self.timeout))
        log.info("Demand manager ready.")

    def stop(self):
        log.info("Demand manager shutting down.")
        debuglog.debug("Stop DemandManager")
        self.finished.set()

    def spawn(self):
        thread = Thread(target=self.wrapper)
        thread.start()
        self.pool += 1
        debuglog.debug("Spawn Demand manager. %s threads" % self.pool)

    def deliver(self, message):
        log.info("Adding message %s to the queue for background delivery." % message.id)
        self.queue.put(copy.deepcopy(message))
        message._processed = True
        message._dirty = True

        if not self.queue.empty() and self.pool < self.optimum:
            tospawn = int(self.optimum - self.pool)
            log.debug("Spawning %d thread%s." % (tospawn, tospawn != 1 and "s" or ""))
            for i in range(tospawn):
                self.spawn()

        return True

    def wrapper(self):
        log.debug("Mail queue worker starting up.")

        try:
            self.worker()
        except:
            log.exception("Internal error in worker thread.")

        self.pool -= 1
        log.debug("Mail queue worker finished.")

    def worker(self):
        log.debug("Requesting new transport instance from.")
        transport = self.get_new_transport()

        debuglog.debug("Worker")
        while True:
            try:
                debuglog.debug("Worker try to deliver message")
                message = self.queue.get(True, self.timeout)
                transport.deliver(message)

            except Empty:
                debuglog.debug("Worker Empty Message")
                log.debug("Worker death from starvation.")
                break

            except TransportExhaustedException:
                debuglog.debug("Worker TransportExhaustedException")
                log.debug("Worker death from transport exhaustion - spawning child.")
                self.deliver(message)
                self.spawn()
                break

            except:
                debuglog.debug("Worker generic exception")
                log.exception("Delivery of message %s failed." % message.id)
                break

            else:
                log.info("Delivery of message %s successful or deferred." % message.id)
        transport.stop()

    def optimum(self):
        min_thread = min(self.threads, math.ceil(self.queue.qsize() / float(self.divisor)))
        debuglog.debug("DemandManager optimum = %s" % min_thread)
        return min_thread

    optimum = property(optimum)
