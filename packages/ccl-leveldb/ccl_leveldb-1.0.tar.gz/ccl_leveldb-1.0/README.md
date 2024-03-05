# CCL Level DB
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

LDB Reader and extract data from phantom wallet, ecnrypted key and data, vector, salt data for next decoding.

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install ccl_leveldb
```
## Example code
example patch
###### C:\Users\root\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn

```python
import ccl_leveldb

def findldb(db_path):
	try:
		leveldb_records = ccl_leveldb.RawLevelDb(db_path)
		for record in leveldb_records.iterate_records_raw():
			try:
				encrypted_object = json.loads(record.value.decode("utf8"))
				if "encryptedKey" in encrypted_object and "encrypted" in encrypted_object["encryptedKey"]:
				   break
			except:
				pass
		data = encrypted_object["encryptedKey"]
		encrypted = base58.b58decode(data["encrypted"])
		nonce = base58.b58decode(data["nonce"])
		salt = base58.b58decode(data["salt"])
		result_object_2 = []
		leveldb_records = ccl_leveldb.RawLevelDb(db_path)
		for record in leveldb_records.iterate_records_raw():
			try:
				json_data = json.loads(record.value.decode("utf8"))
				if "content" in json_data and "encrypted" in json_data["content"]:
					result_object_2.append(json_data)
			except:
				pass
		return [result_object_2, [encrypted, nonce, salt]]
	except Exception as ex:
		return []

```
##Output:
```
[Encrypted, [data, vector, salt]]
```

For more information, see [docs.python-guide.org](http://docs.python-guide.org "docs.python-guide.org").

## License
MIT
>Decoder master project (c)