import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from trivechaind import TrivechainDaemon
from trivechain_config import TrivechainConfig


def test_trivechaind():
    config_text = TrivechainConfig.slurp_config_file(config.trivechain_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000008ad295e16d2a5456aef65cb1c28139835aba6a340d0be0fb8ca2b2e9e26'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000288fe5535c740c1418c70a6da3affa7c858ea6de8852a568ed24d5328d5'

    creds = TrivechainConfig.get_rpc_creds(config_text, network)
    trivechaind = TrivechainDaemon(**creds)
    assert trivechaind.rpc_command is not None

    assert hasattr(trivechaind, 'rpc_connection')

    # Trivechain testnet block 0 hash == 00000288fe5535c740c1418c70a6da3affa7c858ea6de8852a568ed24d5328d5
    # test commands without arguments
    info = trivechaind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert trivechaind.rpc_command('getblockhash', 0) == genesis_hash
