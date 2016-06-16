import pytest

#@pytest.fixture(scope="function")
class TestTest:

    def setup_class(self):
        print ("\n")
        print ("setup_class================>")

    def teardown_class(self):
        print ("teardown_class=============>")

    def teardown(self):
        print ("teardown_function=============>")

    def setup(self):
        print ("setup_function------>")

    def test_numbers_3_4(self):
        print 'test_numbers_3_4'
        assert 3*4 == 12

    def test_numbers_4_5(self):
        print 'test_numbers_4_5'
        assert 5*4 == 20