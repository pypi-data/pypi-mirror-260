## Change log

### 0.3.1
+   Minor fixes and sync from 0.3.0

### 0.3.0
+   Add type hints for all the things
+   Rename `Address` method `is_address` to `has_address`
+   Move `convex_api.utils.is_address` to `Address` static method `is_address`
+   Move `convex_api.utils.to_address` to `Address` static method `to_address`
+   Move `convex_api.utils.is_public_key_hex` to `KeyPair` static method `is_public_key_hex`
+   Move `convex_api.utils.is_public_key` to `KeyPair` static method `is_public_key`
+   Move `convex_api.utils.to_public_key_checksum` to `KeyPair` static method `to_public_key_checksum`
+   Move `convex_api.utils.is_hexstr` to `KeyPair` static method `is_hexstr`
+   Move `convex_api.utils.add_0x_prefix` to `KeyPair` static method `add_0x_prefix`
+   Move `convex_api.utils.remove_0x_prefix` to `KeyPair` static method `remove_0x_prefix`
+   Move `convex_api.utils.to_bytes` to `KeyPair` static methods `to_bytes` for `data: bytes` argument use case and `to_` for `hexstr: string` argument use case
+   Move `convex_api.utils.to_hex` to `KeyPair` static method `to_hex`
+   Add pydantic dependency

### 0.2.6
+   Add cr, tab to contract text encoding

### 0.2.5
+   Rename contract 'register' to 'register_contract_name'

### 0.2.4
+   Add escape_string to Contract class, to escape string data

### 0.2.3
+   New Contract class, to allow for easier contract deployment and usage

### 0.2.2
+   Upgrade to use Alpha-RC4 Convex
+   Add all address fields to have a prefix of #
+   Fix registry conversion issues

### 0.2.1
+   Remove Convex Scrypt language

### 0.2.0
+   Add KeyPair class, now you have to pass a KeyPair object to the `create_account` method.
+   Rename ConvexAPI to API

### 0.1.4
+	Add address '#' identifier before each address number.

### 0.1.3
+   Add transfer_account, the ability to change your account public key for a given account address
+   Remove eth-utils library dependency
+   Improve CLI to do account create / topup / fund / balance / info / name registration / name resolve, query and submit

### 0.1.2
+   Improve registration of account names and resolving account names from the CNS registry

### 0.1.1
+   Incease minimum topup_account funds to 10,000,000
+   Allow to register and load accounts using a name

### 0.1.0
+   Now need to use ConvexAPI.create_account method to create a new account, and get the address number
+   Internal bug fixes, and name conventions for the API calls

### 0.0.8
+   Rebuild with new release

### 0.0.7
+   Rename Account create_new to create
+   Rename Account create_from_bytes to import_from_bytes

### 0.0.6
+   Add topup_account method to api

### 0.0.5
+   Add a 0x prefix to retuned addresses

### 0.0.4
+   Import/export account private keys as a word phrase
+   Convex Wallet tool

### 0.0.3
+   Pre-alpha release

### 0.0.2
+   Add retry sending a transcation during a SEQUENCE error

### 0.0.1
+   Initial Alpha Release
