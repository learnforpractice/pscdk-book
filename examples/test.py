import os
import hashlib
import platform

from ipyeos import eos
from ipyeos import chaintester
from ipyeos.chaintester import ChainTester
from ipyeos import log

chaintester.chain_config['contracts_console'] = True
eos.set_log_level("default", 3)

logger = log.get_logger(__name__)

dir_name = os.path.dirname(os.path.abspath(__file__))

def update_auth(chain, account):
    a = {
        "account": account,
        "permission": "active",
        "parent": "owner",
        "auth": {
            "threshold": 1,
            "keys": [
                {
                    "key": 'EOS6AjF6hvF7GSuSd4sCgfPKq5uWaXvGM2aQtEUCwmEHygQaqxBSV',
                    "weight": 1
                }
            ],
            "accounts": [{"permission":{"actor":account,"permission": 'eosio.code'}, "weight":1}],
            "waits": []
        }
    }
    chain.push_action('eosio', 'updateauth', a, {account:'active'})

def init_test(contract_name):
    t = ChainTester(True)
    update_auth(t, 'hello')
    wasm_file = os.path.join(dir_name, f'{contract_name}.wasm')
    with open(wasm_file, 'rb') as f:
        code = f.read()

    abi_file = os.path.join(dir_name, f'{contract_name}.abi')
    with open(abi_file, 'r') as f:
        abi = f.read()

    t.deploy_contract('hello', code, abi)
    t.produce_block()
    eos.set_log_level("default", 1)
    return t

def test_example1():
    t = init_test('db_example1')
    ret = t.push_action('hello', 'test', "", {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

    # will raise exception
    ret = t.push_action('hello', 'test', "", {'hello': 'active'})
    t.produce_block()

def test_example2():
    t = init_test('db_example2')
    ret = t.push_action('hello', 'test', {'value': 'hello, bob'}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

    ret = t.push_action('hello', 'test', {'value': 'hello, alice'}, {'hello': 'active'})
    t.produce_block()

def test_example3():
    t = init_test('db_example3')
    ret = t.push_action('hello', 'test', {'value': 'hello, bob'}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

    ret = t.push_action('hello', 'test', {'value': 'hello, alice'}, {'hello': 'active'})
    t.produce_block()

def test_example4():
    t = init_test('db_example4')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

def test_example5():
    t = init_test('db_example5')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])
    rows = t.get_table_rows(True, 'hello', '', 'mytable', 1, '', 10)
    logger.info('++++++=rows: %s', rows)

def test_example6():
    t = init_test('db_example6')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

def test_example7():
    t = init_test('db_example7')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

def test_example8():
    t = init_test('db_example8')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])

def test_example9():
    t = init_test('db_example8')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s", ret['elapsed'])

    rows = t.get_table_rows(True, 'hello', '', 'mytable', 22, '', 10, 'i64', '2')
    logger.info("++++++++++%s", rows['rows'])
    assert rows['rows'][0]['b'] == 22

    rows = t.get_table_rows(True, 'hello', '', 'mytable', '3', '', 10, 'i128', '3')
    logger.info("++++++++++%s", rows['rows'])
    assert rows['rows'][0]['c'] == '3'

def test_action():
    t = init_test('action_example')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s", ret['elapsed'])
