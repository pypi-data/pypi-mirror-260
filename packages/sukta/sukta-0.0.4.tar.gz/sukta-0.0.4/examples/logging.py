from sukta.logging import getLogger

log = getLogger("rich")

log.debug("test")
log.info("hello")
log.warning("world")
log.error("warming")
try:
    print(1 / 0)
except Exception:
    log.exception("unable print!")
