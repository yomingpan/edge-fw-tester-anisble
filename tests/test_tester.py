
from edge_fw_tester.tester import run_tests

def test_dummy():
    targets = [ {'host':'localhost','port':1,'proto':'tcp'} ]
    res = run_tests(targets)
    assert len(res)==1
