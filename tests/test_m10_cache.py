import time

from app.storage.cache import ChunkCache
from app.storage.db import Database


def test_cache_cleanup_removes_oldest_but_keeps_protected(tmp_path):
    db = Database(tmp_path / "c.db")
    cache = ChunkCache(db, tmp_path / "cache")
    src = tmp_path / "x.wav"
    src.write_bytes(b"\0" * 1000)
    ids = [f"{i:064x}" for i in range(5)]
    for cid in ids:
        cache.put(cid, src)
        time.sleep(1.05)  # ISO másodperces időbélyeg: eltérő last_used_at
    cache.touch(ids[0])  # a legelső friss használat lett
    assert cache.total_bytes() == 5000
    removed = cache.cleanup(max_bytes=2500, protected=[ids[1]])
    # a legrégebben használt, nem védett bejegyzések mennek, amíg a méret a korlát alá nem kerül:
    # 2, 3, 4 (az 1-es védett, a 0-s friss használat miatt a sor végére került)
    assert removed == [ids[2], ids[3], ids[4]]
    assert cache.total_bytes() == 2000
    assert cache.has(ids[1]) and cache.has(ids[0]) and not cache.path_for(ids[2]).exists()
    assert cache.cleanup(max_bytes=10_000) == []
