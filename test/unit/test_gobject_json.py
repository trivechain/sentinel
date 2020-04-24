import pytest
import sys
import os
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import trivechainlib
import gobject_json

@pytest.fixture
def proposal_hex_new():
    return "7b22656e645f65706f6368223a313538363830343735332c226e616d65223a226275696c642d74726976652d676f7665726e616e6365222c227061796d656e745f61646472657373223a2254526258744e6f714e5650394151327631556f74664d37424a39505863415a783942222c227061796d656e745f616d6f756e74223a3130303030302c2273746172745f65706f6368223a313538343038333135332c2274797065223a312c2275726c223a2268747470733a2f2f676f762e7472697665636861696e2e636f6d2f70726f706f73616c2f6275696c642d74726976652d676f7665726e616e6365227d"

@pytest.fixture
def trigger_hex_new():
    return "7b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a20227443613772444d5873314b657161716d63466f5878584d6d77543965713972376f4b7c7437524b54424e5a7354626a77416f585966735373545377696d787a444b68354675222c20227061796d656e745f616d6f756e7473223a2022357c33222c202270726f706f73616c5f686173686573223a2022653861303035373931346132653139363461653861393435633437323334393163616165323037376139306130306132616162656532326234303038316138377c64316365373335323764376364366632323138663863613839333939306263376435633662393333343739316365373937336266613232663135356638323665222c202274797065223a20327d"


def test_valid_json():
    import binascii

    # test some valid JSON
    assert gobject_json.valid_json("{}") is True
    assert gobject_json.valid_json("null") is True
    assert gobject_json.valid_json("true") is True
    assert gobject_json.valid_json("false") is True
    assert gobject_json.valid_json("\"rubbish\"") is True
    assert gobject_json.valid_json(
        binascii.unhexlify(proposal_hex_new())
    ) is True
    assert gobject_json.valid_json(
        binascii.unhexlify(trigger_hex_new())
    ) is True

    # test some invalid/bad/not JSON
    assert gobject_json.valid_json("False") is False
    assert gobject_json.valid_json("True") is False
    assert gobject_json.valid_json("Null") is False
    assert gobject_json.valid_json("NULL") is False
    assert gobject_json.valid_json("nil") is False
    assert gobject_json.valid_json("rubbish") is False
    assert gobject_json.valid_json("{{}") is False
    assert gobject_json.valid_json("") is False

    poorly_formatted = trigger_hex_new() + "7d"
    assert gobject_json.valid_json(
        binascii.unhexlify(poorly_formatted)
    ) is False


def test_extract_object():
    from decimal import Decimal
    import binascii

    expected = {
        'type': 1,
        'name': 'build-trive-governance',
        'url': 'https://gov.trivechain.com/proposal/build-trive-governance',
        'start_epoch': 1584083153,
        'end_epoch': 1586804753,
        'payment_address': 'TRbXtNoqNVP9AQ2v1UotfM7BJ9PXcAZx9B',
        'payment_amount': Decimal('100000'),
    }

    # test proposal format
    json_str = binascii.unhexlify(proposal_hex_new()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected

    # same expected trigger data
    expected = {
        'type': 2,
        'event_block_height': 62500,
        'payment_addresses': 'tCa7rDMXs1KeqaqmcFoXxXMmwT9eq9r7oK|t7RKTBNZsTbjwAoXYfsSsTSwimxzDKh5Fu',
        'payment_amounts': '5|3',
        'proposal_hashes': 'e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e'
    }

    # test trigger format
    json_str = binascii.unhexlify(trigger_hex_new()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected
