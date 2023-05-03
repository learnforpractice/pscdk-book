# Prerequisite Knowledge

## What are Smart Contracts?

Smart contracts are codes that can be executed on the blockchain.

## What are Python Smart Contracts?

Python smart contracts are codes written in the Python language that can be executed on the blockchain. Taking EOS network as an example, the code of Python smart contracts is compiled into a binary file called WebAssembly, and can be published on the network and executed to achieve a certain desired effect.

## What is EOS?

EOS is a blockchain network based on Delegated Proof of Stake (DPOS) consensus algorithm. The mainnet was launched on June 8, 2018. The mainnet of EOS is controlled by 21 block producers (BP), abbreviated as BP, which are selected through voting and are responsible for packaging transactions into blocks.

## Account

On the EOS blockchain, each entity in a transaction is represented by an account. The name of the account is a name structure, which will be discussed in the next section. The structure of the account in C++ code is relatively complex.

Below is a summary of the information contained in the account, obtained through the `get_account`RPC interface in EOS:

```json
{
 "account_name": "testaccount",
 "head_block_num": 301601062,
 "head_block_time": "2023-03-28T06:19:09.500",
 "privileged": false,
 "last_code_update": "1970-01-01T00:00:00.000",
 "created": "2018-06-13T04:43:18.000",
 "core_liquid_balance": "0.0001 EOS",
 "ram_quota": 3052,
 "net_weight": 0,
 "cpu_weight": 0,
 "net_limit": {
  "used": 0,
  "available": 0,
  "max": 0,
  "last_usage_update_time": "2018-06-13T04:43:18.000",
  "current_used": 0
 },
 "cpu_limit": {
  "used": 0,
  "available": 0,
  "max": 0,
  "last_usage_update_time": "2018-06-13T04:43:18.000",
  "current_used": 0
 },
 "ram_usage": 2996,
 "permissions": [
  {
   "perm_name": "active",
   "parent": "owner",
   "required_auth": {
    "threshold": 1,
    "keys": [
     {
      "key": "EOS5eCkKszJt22****Y2YampuDDD8q95w2mF",
      "weight": 1
     }
    ],
    "accounts": [],
    "waits": []
   },
   "linked_actions": []
  },
  {
   "perm_name": "owner",
   "parent": "",
   "required_auth": {
    "threshold": 1,
    "keys": [
     {
      "key": "EOS5eCkKszJ****q95w2mF",
      "weight": 1
     }
    ],
    "accounts": [],
    "waits": []
   },
   "linked_actions": []
  }
 ],
 "total_resources": {
  "owner": "helloworld11",
  "net_weight": "0.0000 EOS",
  "cpu_weight": "0.0000 EOS",
  "ram_bytes": 3052
 },
 "self_delegated_bandwidth": null,
 "refund_request": null,
 "voter_info": null,
 "rex_info": null,
 "subjective_cpu_bill_limit": {
  "used": 0,
  "available": 0,
  "max": 0,
  "last_usage_update_time": "2000-01-01T00:00:00.000",
  "current_used": 0
 },
 "eosio_any_linked_actions": []
}
```

Here's a brief description of the main fields:

- `account_name`: the name of the account, the rules for which will be explained in the next section.
- `privileged`: `true` indicates that the account is a privileged account, such as `eosio`. `false` indicates a regular account.
- `last_code_update`: the time of the last update to the smart contract in the account.
- `created`: the creation time of the account.
- `core_liquid_balance`: the available balance in the account.
- `ram_quota`: the total amount of memory allocated to the account. Because EOS's database is a memory database, all on-chain data needs to be stored in memory, and memory is limited, so memory is allocated as a resource to accounts.
- `net_weight`: the weight of the network resources allocated to the account.
- `cpu_weight`: the weight of the CPU resources allocated to the account.
- `net_limit`: the usage of network resources by the account.
- `cpu_limit`: the usage of CPU resources by the account.
- `ram_usage`: the amount of memory already used.
- `permissions`: the permissions of the account, which include one or more public keys or account information. Each public key and account permission carries a certain weight, and when a transaction is sent, it must be signed with the private key corresponding to the public key, and the weight must be greater than or equal to the `threshold` before the transaction can be recognized by the BP. When the account permission includes information inherited from another account instead of a public key, the public key information will be extracted from the permission information of the account when signing, which is implemented through C++ algorithms. The EOS RPC interface also has a `get_required_keys` interface to obtain the public key information of the signature.
- `total_resources`: specifies the information of the NET, CPU, RAM and other resources allocated to the group account.

## Name structure
Name is one of the most basic data structures in EOS, represented by a 64-bit unsigned integer (`uint64_t`) at the lowest level.

Here is the C++ definition.

[libraries/chain/include/eosio/chain/name.hpp](https://github.com/EOSIO/eos/blob/5082391c60b0fa5e68157c385cd402bf25aea934/libraries/chain/include/eosio/chain/name.hpp#L42)

```c++
   struct name {
      uint64_t value = 0;
      bool empty()const { return 0 == value; }
      bool good()const  { return !empty();   }

      name( const char* str )   { set(str);           } 
      name( const string& str ) { set( str.c_str() ); }
...
   }
```

However, in the application layer, name values are represented as strings and can only contain the following characters: ".12345abcdefghijklmnopqrstuvwxyz". There are a total of 32 characters which represent the numbers 0 to 31, and these strings can be seen as a 32-bit data. In a `uint64_t`, every 5 bits are converted into one of the aforementioned characters. As `uint64_t` has a maximum of 64 bits, the first 60 bits can represent up to 12 characters. The characters' scope can be expressed using regular expressions as `[.1-5a-z]`, whereas the highest 4 bits can only be represented by 16 characters, which are expressed within the range `[.1-5a-j]`.

It is not uncommon to make mistakes when creating accounts, such as making valid characters out of '6' to '9', '0' and uppercase letters, as well as not limiting the name to 12 characters.

In summary:

- In EOS, the name value is actually a `uint64_t` type at the underlying level, and it is represented as a string in the application layer, with the string having a maximum of 13 characters.
- The range of the 13th character is smaller than that of the previous 12 characters.
- When representing account names using the name structure, a maximum of 12 characters is allowed.
- Additionally, the name structure is also used to represent other types in the following C++ code:

[libraries/chain/include/eosio/chain/types.hpp](https://github.com/EOSIO/eos/blob/5082391c60b0fa5e68157c385cd402bf25aea934/libraries/chain/include/eosio/chain/types.hpp#L133)

```c++
   using account_name     = name;
   using action_name      = name;
   using scope_name       = name;
   using permission_name  = name;
   using table_name       = name;
```

In this C++ code, the name structure is also used to represent action, table names, and more. It should be noted that unlike account names, when representing these names as strings, they can have a maximum of 13 characters. However, for convenience, it is common practice to use a maximum of 12 characters to represent these names.                                                                                                    
## Transaction

On EOS, the basic data structure is called a transaction, which is responsible for collecting transactions within a period of time and packaging them into a block by the block producers (BP). Smart contract developers must fully understand the data structure of transactions.

[libraries/chain/include/eosio/chain/transaction.hpp](https://github.com/EOSIO/eos/blob/5082391c60b0fa5e68157c385cd402bf25aea934/libraries/chain/include/eosio/chain/transaction.hpp#L30)
```c++
struct transaction_header {
      time_point_sec         expiration;   ///< the time at which a transaction expires
      uint16_t               ref_block_num       = 0U; ///< specifies a block num in the last 2^16 blocks.
      uint32_t               ref_block_prefix    = 0UL; ///< specifies the lower 32 bits of the blockid at get_ref_blocknum
      fc::unsigned_int       max_net_usage_words = 0UL; /// upper limit on total network bandwidth (in 8 byte words) billed for this transaction
      uint8_t                max_cpu_usage_ms    = 0; /// upper limit on the total CPU time billed for this transaction
      fc::unsigned_int       delay_sec           = 0UL; /// number of seconds to delay this transaction for during which it may be canceled.

...
   };

   struct transaction : public transaction_header {
      vector<action>         context_free_actions;
      vector<action>         actions;
      extensions_type        transaction_extensions;
...
   };
```

Here's a brief explanation of some of the important fields:

- `expiration`: This sets the timeout period for the transaction to be put on the chain. Transactions that exceed their expiration time will be rejected from being included in the block.
- `ref_block_num` and `ref_block_prefix`: These two member variables are designed to prevent transactions from being included in blocks on forked chains.
- `actions`: This is an array structure of actions, which is a very important concept. Each action corresponds to a smart contract function on the chain, and when the BP includes the transaction in the block, they will call the corresponding smart contract function according to the action. This will be explained in more detail in the following section.
- `context_free_actions`: This is also an array of actions, but when the corresponding smart contract function is called, the code that is executed is not allowed to call the API related to the on-chain database.
                                                                                                    
## Action

The action structure is included in the transaction structure. The definition of an action structure in C++ code is as follows:

[libraries/chain/include/eosio/chain/action.hpp](https://github.com/EOSIO/eos/blob/5082391c60b0fa5e68157c385cd402bf25aea934/libraries/chain/include/eosio/chain/action.hpp#L60)

```c++
   struct action {
      account_name               account;
      action_name                name;
      vector<permission_level>   authorization;
      bytes                      data;
...
   }
```

Where [permission_level](https://github.com/EOSIO/eos/blob/5082391c60b0fa5e68157c385cd402bf25aea934/libraries/chain/include/eosio/chain/action.hpp#L12)的定义如下：

```C++
struct permission_level {
    account_name    actor;
    permission_name permission;
};
```
The meanings of the member variables in the structure are explained as follows:

- `account`: The account name of the smart contract to be called.
- `name`: The name of the action to be called.
- `authorization`: An array of permissions.
- `data`: The serialized raw data contained in the action, which will be deserialized into specific data structures when called by the smart contract.                                                                                                
## ABI(Application Binary Interface)

When developing smart contracts, during the compilation process of the smart contract code, an ABI file (.abi) is usually generated along with the binary code (.wasm) of each smart contract. However, it should be noted that this file is not necessary for calling smart contracts on the chain. Its purpose is to facilitate developers in obtaining information about relevant actions, in order to construct the corresponding Transaction data structure for interacting with the blockchain.

The content of an ABI file is in JSON format, like the following:

```json
{
    "version": "eosio::abi/1.2",
    "structs": [
        {
            "name": "A",
            "base": "",
            "fields": [
                {
                    "name": "a",
                    "type": "uint64"
                },
                {
                    "name": "b",
                    "type": "uint64"
                },
                {
                    "name": "c",
                    "type": "uint128"
                }
            ]
        },
        {
            "name": "test",
            "base": "",
            "fields": []
        }
    ],
    "actions": [
        {
            "name": "test",
            "type": "test",
            "ricardian_contract": ""
        }
    ],
    "tables": [
        {
            "name": "mytable",
            "type": "A",
            "index_type": "i64",
            "key_names": [],
            "key_types": []
        }
    ],
    "ricardian_clauses": []
}
```

- `version`: Specifies the version of the ABI.
- `structs`: Specifies the data structures that will be used in the `actions` and `tables` structures.
- `actions`: Describes the actions that can be performed in the smart contract, each of which corresponds to a smart contract function.
- `tables`: Describes information about tables so that your web application can query on-chain database information using the `get_table_rows` RPC API.
