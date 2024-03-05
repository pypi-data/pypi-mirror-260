from concurrent.futures import ThreadPoolExecutor

DEFAULT_IO_EXECUTOR = ThreadPoolExecutor(
    max_workers=32,
    thread_name_prefix="chalk-io-",
)
