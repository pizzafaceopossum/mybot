
from mybot_globals import *

class Command(object):
	def __init__(self, **kwargs):
		self.name: str = kwargs['name']
		self.description: str = kwargs.get('description', 'No description.')
		self.synonyms: tuple[str] = tuple(sorted(set((command_identifier + ''.join(self.name.lower().split()), *[command_identifier + ''.join(synonym.lower().split()) for synonym in kwargs.get('synonyms', tuple())]))))
		self.fail_on_dedicated_keyword = kwargs.get('fail_on_dedicated_keyword', False)
	
	def __str__(self) -> str:
		syns: str = '('
		for synonym in self.synonyms:
			syns += synonym + ", "
		syns = syns[0:-2] + ')'
		return f'{self.name} {syns}: {self.description}\n'
	
	def effect(self, *args, **kwargs):
		pass