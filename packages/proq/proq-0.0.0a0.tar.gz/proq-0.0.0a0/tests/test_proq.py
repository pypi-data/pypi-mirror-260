import proq


def test_proq_create_collect():
    assert proq.create([1, 2, 3, 4, 5]).collect() == [1, 2, 3, 4, 5]


def test_proq_queue_empty():
    proq_queue = proq.ProqQueue()
    proq_queue.close()
    assert proq_queue.collect() == []
