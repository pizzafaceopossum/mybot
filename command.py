
from env import *

class Command(object):
	def __init__(self, **kwargs):
		self.name: str = kwargs['name']
		self.syns: tuple[str] = tuple(sorted(set((command_identifier + ''.join(self.name.lower().split()), *[command_identifier + ''.join(synonym.lower().split()) for synonym in kwargs.get('syns', tuple())]))))
		self.desc: str = kwargs.get('desc', 'No description.')
		self.priv: int = kwargs.get('priv', 0b00000001)
		self.fail_on_dedicated_keyword = kwargs.get('fail_on_dedicated_keyword', False)
		self.effect = kwargs.get('effect', self.effect)
	
	def __str__(self) -> str:
		syns: str = '('
		for synonym in self.syns:
			syns += synonym + ", "
		syns = syns[0:-2] + ')'
		return f'{self.name} {syns}: {self.desc}\n'
	
	def effect(self, *args, **kwargs):
		pass