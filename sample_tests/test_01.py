def test_merge_sources_dedupes():
    assert merge_sources(["a", "b"], ["b", "c"]) == ["a", "b", "c"]
