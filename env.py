
import os
import sys
import dill
import json as JSON
import re

command_identifier = ';'
command_dir: str = './commands/'
commands_file: str = './commands.json'
sys.path.append(command_dir)

def set_bytes(var: bytes, idx: int, val: bytes, **kwargs):
	if idx%len(var) + len(val) >= len(var) and not kwargs.get('append_extra', False):
		e = IndexError('Setting bytes overflow. To append extra bytes instead, set append_extra=True.')
		raise(IndexError)
	elif idx%len(var) + len(val) >= len(var):
		return var[0:idx] + val
	return var[0:idx] + val + var[len(val)+idx:]

def insert_bytes(var: bytes, idx: int, val: bytes):
	return var[0:idx] + val + var[idx:]

def remove_bytes(var: bytes, idx: int, amount: int):
	if idx%len(var) + amount >= len(var):
		print("Tried to remove more bytes than there are left in the input.")
		return var[0:idx]
	return var[0:idx] + var[amount + idx:]

def hexdump(var: bytes, addr_len: int = 16):
	for i in range(len(var)):
		if i%addr_len == addr_len - 1:
			print("%02x" % var[i] + " ")
		else:
			print("%02x" % var[i] + " ", end='')
	print('\n')

def flip_digits(var: bytes):
	flipped = b''
	for byte in var:
		flipped += (0x10*(byte%0x10) + byte//0x10).to_bytes()
	return flipped

def bytes_to_decimal(var: bytes, byteorder: str = 'big', digit_order: str = 'big', signed: bool = False):
	match digit_order:
		case 'big':
			pass
		case 'small':
			var = flip_digits(var)
		case _:
			raise(ValueError)
	return int.from_bytes(var, byteorder=byteorder, signed=signed)

def dump_method(method):
	dump = dill.dumps(method, recurse = True, byref = False)
	replacement_bytes = b'\x00'*len(method.__code__.co_filename)
	replaced_dump = re.sub(bytes(r'\??' + method.__code__.co_filename, 'latin'), replacement_bytes, dump)
	return set_bytes(replaced_dump, 3, (len(replaced_dump) - 11).to_bytes(8, 'little'))