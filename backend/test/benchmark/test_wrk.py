from os.path import join, dirname, realpath
from fabric.api import local
from unittest import TestCase
from time import sleep
from web.util import get_logger

log = get_logger(__name__)


class TestWrk(TestCase):
    def setUp(self):
        log.info('Test wrk start...')

    def flush_output(self, content):
        """
        Flush content to file
        """
        log.info('Flush content to file: \n%s', content)
        out_file = join(dirname(realpath(__file__)), 'test_wrk_out.csv')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def handle_row(self, out_put, result):
        for line in out_put.split('\n'):
            line = line.strip()
            if line.startswith('Latency'):  # Average latency for requests
                latency = line.split()[1]
                if latency.endswith('ms'):
                    result += ', ' + latency.replace('ms', '')
                else:
                    result += ', ' + str(float(latency.replace('s', '')) * 1000)
            elif line.startswith('Req/Sec'):        # Request throughput for a single thread
                result += ', ' + line.split()[1]
            elif line.startswith('Requests/sec'):   # Total request throughput
                result += ', ' + line.split()[1]
            elif line.startswith('Transfer/sec'):   # Total throughput in KB
                through = line.split()[1]
                if through.endswith('MB'):
                    result += ', ' + str(float(through.replace('MB', '')) * 1000)
                elif through.endswith('KB'):
                    result += ', ' + str(float(through.replace('KB', '')))
        return result

    def test_handle_report(self):
        """
        处理wrk的输出.
        Test in command line: python3 -m unittest -v test.benchmark.test_wrk.TestWrk.test_handle_report
        More info about wrk, please refere to: https://github.com/wg/wrk
        """
        result = 'Concurrency, Latency(ms), Req/Sec, Requests/sec, Transfer/sec(KB)\n'
        for i in range(20):
            concurrency = 100 * (i + 1)
            # Test case1: evaluate the performance of JVM and nodejs
            cmd = 'wrk -c%s -t%s -d60s http://localhost:8000' % (concurrency, concurrency)
            # Test case2: evaluate the whole performance after adding the NGINX cache.
            # cmd = 'wrk -c%s -t%s -d60s http://localhost:8001' % (concurrency, concurrency)
            log.info('Fabric execute local: %s', cmd)
            out_put = local(cmd, capture=True)
            log.info('out_put: %s', out_put)
            result += str(concurrency)
            result = self.handle_row(out_put, result)
            result += '\n'
            self.flush_output(result)
            log.info('Sleep for a while....')
            sleep(5)
