from xd.tool.main import main
from redirect import *

def test_main_no_args():
    main(['xd'])

def test_main_early_args():
    with stdchannels_redirected():
        main(['xd', '-d'])

