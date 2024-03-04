from image_diversity import ClipMetrics

TEST_DIR = "../db_stdiff/results/gpt_variants/canoe/unusual"

clip_metrics = ClipMetrics()


class TestClipLocal:
    def test_tcd_negis(self):
        assert clip_metrics.tce(TEST_DIR) > 0
