import unittest

from spec.testcases.base_client import BaseClientTestCase
from spec.testcases.koemei_client import KoemeiClientTestCase
from spec.testcases.model.media import MediaTestCase
from spec.testcases.model.process import ProcessTestCase

#suite = unittest.TestLoader().loadTestsFromTestCase(BaseClientTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(MediaTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

#suite = unittest.TestLoader().loadTestsFromTestCase(ProcessTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)

"""suite = unittest.TestLoader().loadTestsFromTestCase(KoemeiClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(ApiSerializableTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
"""