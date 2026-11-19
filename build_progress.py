"""Progress for long-running catalogue builds, including redirected console output."""
from importlib import import_module
from time import monotonic


def stage(label, module, **kwargs):
    start = monotonic()
    print(f"[build] Starting {label}", flush=True)
    try:
        import_module(module).main(**kwargs)
    except Exception:
        print(f"[build] Failed during {label} after {monotonic() - start:.1f}s", flush=True)
        raise
    print(f"[build] Finished {label} in {monotonic() - start:.1f}s", flush=True)


def progress(items, label, name):
    start = monotonic()
    last = start
    total = len(items)
    for index, item in enumerate(items, 1):
        now = monotonic()
        if index == 1 or index == total or now - last >= 4:
            print(f"  {label} {index}/{total} ({now - start:.0f}s)  {name(item)}", flush=True)
            last = now
        yield item
