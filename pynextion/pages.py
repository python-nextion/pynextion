
from . import components

# pylint: disable=C0330,C0111

class Page(object):
	def __init__(self, nextion, comp_id):
		self.components = []
		self.comp_id = comp_id
		self.name = None
		self.nextion = nextion

	@staticmethod
	def new_page_by_definition(nextion, page_definition):
		page = Page(nextion, page_definition['id'])
		page.name = page_definition['name']
		if page_definition['components'] is not None:
			for component_definition in page_definition['components']:
				page.components.append(components.Component \
					.new_component_by_definition(page, component_definition))
		return page

	def component_by_name(self, name):
		result = None
		for component in self.components:
			if name == component.name:
				result = component
				break
		return result

	def hook_text(self, comp_id, value=None):
		component = components.Text(self, comp_id, value)
		self.components.append(component)
		return component

	def show(self):
		self.nextion.set_page(self.comp_id)
