import unittest

from spec.testcases.base_client import BaseClientTestCase
from spec.testcases.koemei_client import KoemeiClientTestCase
from spec.testcases.model.media import MediaTestCase
from spec.testcases.model.process import ProcessTestCase
from spec.testcases.model.transcript import TranscriptTestCase

"""
Models
"""

# Base client
suite = unittest.TestLoader().loadTestsFromTestCase(BaseClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

# Media
suite = unittest.TestLoader().loadTestsFromTestCase(MediaTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

# Process
suite = unittest.TestLoader().loadTestsFromTestCase(ProcessTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

# Transcript
suite = unittest.TestLoader().loadTestsFromTestCase(TranscriptTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)


suite = unittest.TestLoader().loadTestsFromTestCase(KoemeiClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)