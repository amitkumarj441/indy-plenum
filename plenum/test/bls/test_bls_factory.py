import os

import pytest
from crypto.bls.bls_bft import BlsBft
from crypto.bls.bls_crypto import BlsCrypto
from crypto.bls.bls_key_manager import LoadBLSKeyError
from plenum.bls.bls import BlsFactoryIndyCrypto
from plenum.bls.bls_store import BlsStore
from plenum.common.config_util import getConfig
from state.pruning_state import PruningState
from storage.kv_in_memory import KeyValueStorageInMemory

config = getConfig()


@pytest.fixture()
def pool_state():
    return PruningState(KeyValueStorageInMemory())


@pytest.fixture()
def bls_factory(tempdir):
    os.mkdir(os.path.join(tempdir, 'Node1'))
    data_dir = os.path.join(tempdir, 'data', 'nodes', 'Node1')
    os.makedirs(data_dir)
    return BlsFactoryIndyCrypto(tempdir, data_dir, 'Node1', config)


@pytest.fixture()
def bls_factory2(tempdir):
    os.mkdir(os.path.join(tempdir, 'Node2'))
    data_dir = os.path.join(tempdir, 'data', 'nodes', 'Node2')
    os.mkdir(data_dir)
    return BlsFactoryIndyCrypto(tempdir, data_dir, 'Node2', config)


def test_create_and_store_bls_keys(bls_factory):
    pk = bls_factory.generate_and_store_bls_keys()
    assert pk
    assert isinstance(pk, str)


def test_create_bls_keys(bls_factory):
    sk, pk = bls_factory.generate_bls_keys()
    assert pk
    assert sk
    assert isinstance(sk, str)
    assert isinstance(pk, str)


def test_create_and_store_bls_keys_multiple(bls_factory):
    pk1 = bls_factory.generate_and_store_bls_keys()
    pk2 = bls_factory.generate_and_store_bls_keys()
    pk3 = bls_factory.generate_and_store_bls_keys()
    assert pk1 != pk2 != pk3


def test_create_bls_keys_multiple(bls_factory):
    sk1, pk1 = bls_factory.generate_bls_keys()
    sk2, pk2 = bls_factory.generate_bls_keys()
    sk3, pk3 = bls_factory.generate_bls_keys()
    assert pk1 != pk2 != pk3
    assert sk1 != sk2 != sk3


def test_create_bls_crypto_no_keys(bls_factory):
    with pytest.raises(LoadBLSKeyError):
        bls_factory.create_bls_crypto_from_saved_keys()


def test_create_bls_crypto(bls_factory):
    pk = bls_factory.generate_and_store_bls_keys()
    bls_crypto = bls_factory.create_bls_crypto_from_saved_keys()
    assert bls_crypto
    assert isinstance(bls_crypto, BlsCrypto)
    assert bls_crypto._sk
    assert bls_crypto.pk
    assert pk == bls_crypto.pk


def test_create_bls_crypto_multiple_times(bls_factory):
    pk1 = bls_factory.generate_and_store_bls_keys()
    bls_crypto1 = bls_factory.create_bls_crypto_from_saved_keys()
    assert pk1 == bls_crypto1.pk

    pk2 = bls_factory.generate_and_store_bls_keys()
    bls_crypto2 = bls_factory.create_bls_crypto_from_saved_keys()
    assert pk2 == bls_crypto2.pk

    pk3 = bls_factory.generate_and_store_bls_keys()
    bls_crypto3 = bls_factory.create_bls_crypto_from_saved_keys()
    assert pk3 == bls_crypto3.pk


def test_bls_crypto_works(bls_factory, bls_factory2):
    # create bls for Node1
    bls_factory.generate_and_store_bls_keys()
    bls_crypto1 = bls_factory.create_bls_crypto_from_saved_keys()
    pk1 = bls_crypto1.pk

    # create bls for Node2
    bls_factory2.generate_and_store_bls_keys()
    bls_crypto2 = bls_factory2.create_bls_crypto_from_saved_keys()
    pk2 = bls_crypto2.pk

    # each node signs the message
    msg = 'Hello!'
    pks = [pk1, pk2]
    sigs = []
    sigs.append(bls_crypto1.sign(msg))
    sigs.append(bls_crypto2.sign(msg))

    # each node creates multi-sig
    multi_sig1 = bls_crypto1.create_multi_sig(sigs)
    multi_sig2 = bls_crypto2.create_multi_sig(sigs)

    # each node verifies multi-sigs
    assert bls_crypto1.verify_multi_sig(multi_sig1, msg, pks)
    assert bls_crypto1.verify_multi_sig(multi_sig2, msg, pks)
    assert bls_crypto2.verify_multi_sig(multi_sig1, msg, pks)
    assert bls_crypto2.verify_multi_sig(multi_sig2, msg, pks)


def test_create_bls_store(bls_factory):
    bls_store = bls_factory.create_bls_store()
    assert bls_store
    assert isinstance(bls_store, BlsStore)


def test_create_bls_bft(bls_factory, pool_state):
    bls_factory.generate_and_store_bls_keys()
    bls_store = bls_factory.create_bls_store()
    bls_bft = bls_factory.create_bls_bft(is_master=True,
                                         pool_state=pool_state,
                                         bls_store=bls_store)
    assert bls_bft
    assert isinstance(bls_bft, BlsBft)


def test_create_bls_bft_crypto_no_keys(bls_factory, pool_state):
    with pytest.raises(LoadBLSKeyError):
        bls_store = bls_factory.create_bls_store()
        bls_factory.create_bls_bft(is_master=False,
                                   pool_state=pool_state,
                                   bls_store=bls_store)