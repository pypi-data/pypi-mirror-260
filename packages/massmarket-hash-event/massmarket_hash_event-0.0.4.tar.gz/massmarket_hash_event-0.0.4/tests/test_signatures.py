import pytest
from binascii import hexlify
import random
random.seed("massmarket-testing")

from massmarket_hash_event import Hasher, schema_pb2

def hex(b: bytes) -> str:
  return hexlify(b).decode('utf-8')

def test_correct_contract_addr():
  with pytest.raises(Exception) as ex:
    Hasher(123, "aaa")
  assert str(ex.value) == "Invalid contract address: aaa"
  with pytest.raises(Exception) as ex:
    Hasher(123, "0xabc")
  assert str(ex.value) == 'Odd-length string'
  with pytest.raises(Exception) as ex:
    Hasher(123, "0xabcd")
  assert str(ex.value) == "Invalid contract address: 0xabcd"
  h = Hasher(123, "0x1234567890123456789012345678901234567890")
  assert h is not None

def test_hash_empty_event():
  h = Hasher(2342, "0x0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a")
  events = [
    (schema_pb2.Event(store_manifest=schema_pb2.StoreManifest()),
     "dac52d2e56bf05359c3a6e1c212436e0a5a646f9b432205d38a198b5cb01c347"),
    
    (schema_pb2.Event(update_manifest=schema_pb2.UpdateManifest(field=schema_pb2.UpdateManifest.MANIFEST_FIELD_DOMAIN)),
      "62628d6acbfad2a1c7e277e5abffb9d610fad21716d0d2806e1b1af0aa697883"),

    (schema_pb2.Event(create_item=schema_pb2.CreateItem()),
      "576f9417b9e439e83a7e3a80eabdce8a45dbeba9cb213397127a0a8bfa61341c"),
    
    (schema_pb2.Event(update_item=schema_pb2.UpdateItem(field=schema_pb2.UpdateItem.ITEM_FIELD_PRICE)),
      "049fc336a0d459548b1c1c98463021f1abb0f6edc993fee3d04c635277307097"),
   
    (schema_pb2.Event(create_tag=schema_pb2.CreateTag()),
      "12e0397815025a95d0bf6ff873eb7d51202ec5e9b74742a54d9c8ebf644522de"),
    
    (schema_pb2.Event(add_to_tag=schema_pb2.AddToTag()),
      "9cb2a74cc627908b03d739c17a7d6d76715bf8f148b9d3b8a0f9569fa59bfb35"),

    (schema_pb2.Event(remove_from_tag=schema_pb2.RemoveFromTag()),
      "ab8b0cd75c8e4669b50b319160aa3502bfd5389e6710683e0452337f1ebbbf27"),

    (schema_pb2.Event(rename_tag=schema_pb2.RenameTag()),
      "f96b46f5497d77864a25edb5e1127ec4fe97593febded4fc815b3939b76442d4"),

    (schema_pb2.Event(delete_tag=schema_pb2.DeleteTag()),
      "f93388cdafcaf592618f8875d2daef4504b024e971998528907057cece256e62"),

    (schema_pb2.Event(create_cart=schema_pb2.CreateCart()),
      "4f2db3a3657184f702c3aeba27ebe166f7d38f3fcdf73716e9c2c1dd945c8e70"),

    (schema_pb2.Event(change_cart=schema_pb2.ChangeCart()),
      "4e81d5c053f0de9fcd7e5129395ed005a03fcdc451deea4f0a3afdeedc4da8bb"),

    (schema_pb2.Event(change_stock=schema_pb2.ChangeStock()),
      "0452202c63d46c60f99610ea50a510ac872fe24fab3c543f0a4b68db48f7e117"),

    (schema_pb2.Event(new_key_card=schema_pb2.NewKeyCard(user_wallet_addr=random.randbytes(20))),
      "4f7f2e29020009900078320f4b590b484f68448c5978583cddaea9bd78d8b038")
  ]
  for idx, (evt, expected) in enumerate(events):
    data = h.hash_event(evt)
    assert hex(data.body) == expected, f"Failed on event {idx}"



import json
from web3 import Account, Web3

# check that the test vectors we generated are valid
def test_verify_vector_file():
  with open("../testVectors.json") as f:
    vector = json.load(f)
  assert len(vector['events']) == 16
  assert "signatures" in vector
  vec_sigs = vector['signatures']
  signer = vec_sigs['signer_address']
  assert signer == "0x27B369BDD9b49C322D13e7E91d83cFD47d465713"
  h = Hasher(vec_sigs['chain_id'], vec_sigs['contract_address'])
  for idx, evt in enumerate(vector['events']):
    parsed = schema_pb2.Event()
    parsed.ParseFromString(bytes.fromhex(evt['encoded']))
    assert len(parsed.signature) == 65, f"invalid signature on event {idx}"
    encoded_data = h.hash_event(parsed)
    pub_key = Account.recover_message(encoded_data, signature=parsed.signature)
    their_addr = Web3.to_checksum_address(pub_key)
    assert their_addr == signer, f"invalid signer on event {idx}"
