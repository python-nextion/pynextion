
# pylint: disable=C0330,C0111

class Component(object):
	def __init__(self, page, comp_id, name):
		self.page = page
		self.comp_id = comp_id
		self.name = name

	def refresh(self):
		self.page.nextion.refresh(self.comp_id)
	def update_value(self):
		pass


	@staticmethod
	def new_component_by_definition(page, componentDefinition):
		comp_type = componentDefinition['type']
		comp_id = componentDefinition['id']
		name = None
		name = componentDefinition['name']
		value = None
		try:
			value = componentDefinition['value']
		except KeyError:
			pass

		if "text" in comp_type:
			return Text(page, comp_id, name, value)
		elif "number" in comp_type:
			return Number(page, comp_id, name, value)
		elif "button" in comp_type:
			return Button(page, comp_id, name, value)
		elif "gauge" in comp_type:
			return Gauge(page, comp_id, name, value)
		elif "hotspot" in comp_type:
			return HotSpot(page, comp_id, name)
		elif "waveform" in comp_type:
			return WaveForm(page, comp_id, name)

		return None


class Text(Component):
	def __init__(self, page, comp_id, name=None, value=None):
		super(Text, self).__init__(page, comp_id, name)

		if value is not None:
			self.page.nextion.set_text(self.comp_id, value)
		else:
			self.val_buf = self.get()

	def update_value(self):
		self.page.nextion.set_text(self.comp_id, self.val_buf)

	def get(self):
		return self.page.nextion.get_text(self.comp_id)

	def set(self, value):
		# Cache writes
		if value != self.val_buf:
			self.val_buf = value
			self.page.nextion.set_text(self.comp_id, value)


class Number(Component):
	def __init__(self, page, comp_id, name=None, value=None):
		super(Number, self).__init__(page, comp_id, name)
		if value is not None:
			self.page.nextion.set_value(self.comp_id, value)

	def get(self):
		return self.page.nextion.get_value(self.comp_id)

	def set(self, value):
		self.page.nextion.set_value(self.comp_id, value)


class Button(Component):
	def __init__(self, page, comp_id, name=None, value=None):
		super(Button, self).__init__(page, comp_id, name)
		if value is not None:
			self.page.nextion.set_text(self.comp_id, value)

	def get(self):
		return self.page.nextion.get_text(self.comp_id)

	def set(self, value):
		self.page.nextion.set_text(self.comp_id, value)


class HotSpot(Component):
	pass

class WaveForm(Component):
	def add(self, channel, value):
		print(str(self.comp_id) + ":" + str(channel) + " => " + str(value))
		self.page.nextion.nx_write("add " + self.comp_id + "," + channel + "," + value)


class Gauge(Component):
	def __init__(self, page, comp_id, name=None, value=None):
		super(Gauge, self).__init__(page, comp_id, name)
		if value is not None:
			self.page.nextion.set_value(self.comp_id, value)

	def get(self):
		return self.page.nextion.get_value(self.comp_id)

	def set(self, value):
		self.page.nextion.set_value(self.comp_id, value)
