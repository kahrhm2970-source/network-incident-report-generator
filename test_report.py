import unittest
from report import read_results, render, cell

HEADER = 'id,test,expected,observed,status,evidence\n'


class ReportTests(unittest.TestCase):
    def test_pending_stays_pending(self):
        rows = read_results(HEADER + 'INC-1,Ping,Reply,,PENDING,\n')
        self.assertIn('PASS: 0 | FAIL: 0 | PENDING: 1', render(rows))

    def test_summary(self):
        rows = read_results(HEADER + '1,Ping,Reply,Reply,PASS,a\n2,Ping,Reply,Timeout,FAIL,b\n')
        self.assertIn('PASS: 1 | FAIL: 1 | PENDING: 0', render(rows))

    def test_observation_required(self):
        with self.assertRaises(ValueError):
            read_results(HEADER + '1,Ping,Reply,,PASS,\n')

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            read_results(HEADER + '1,Ping,Reply,,PENDING,\n1,Ping,Reply,,PENDING,\n')

    def test_invalid_inputs(self):
        for text in ['', HEADER, HEADER + '1,Ping,Reply,Reply,UNKNOWN,\n', HEADER + '1,Ping\n']:
            with self.assertRaises(ValueError):
                read_results(text)

    def test_escape_content(self):
        self.assertEqual(cell('<script>|[x]\n*'), '&lt;script&gt;&#124;&#91;x&#93;<br>&#42;')

    def test_bom_and_arabic(self):
        rows = read_results('\ufeff' + HEADER + '1,اختبار,نجاح,,pending,\n')
        self.assertEqual(rows[0]['status'], 'PENDING')
        self.assertIn('اختبار', render(rows))


if __name__ == '__main__':
    unittest.main()
