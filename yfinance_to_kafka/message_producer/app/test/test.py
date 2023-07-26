import unittest
from ..yfinance_producer import YFinanceProducer
import yfinance as yf
class TestYFinanceProducer(unittest.TestCase):
    def test_initialize_class(self):
        self.assertIsInstance(YFinanceProducer(bootstrap_servers="kafka:29092"), YFinanceProducer, "Failed to initialize YFinanceProducer")

    def test_yfinance(self):
        yf_producer = YFinanceProducer(bootstrap_servers="kafka:29092")
        self.assertEqual(yf_producer._download_data())

if __name__ == '__main__':
    unittest.main()