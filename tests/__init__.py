import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_dir, os.path.pardir))

os.environ["DJANGO_SETTINGS_MODULE"] = 'tests.settings'
