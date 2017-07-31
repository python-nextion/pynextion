
import sys
import traceback
import time
import serial
import logging
from .pages import Page
from .components import Text, Number, Button, Gauge, Component

# pylint: disable=C0330,C0111

class Nextion(object):
	BAUD_VALUES = {
			2400,
			4800,
			9600,
			19200,
			38400,
			57600,
			115200,
		}

	ERRORS = {
		0x00 : "Invalid instruction",
		# 0x01 : "Successful execution of instruction",
		0x02 : "Component ID invalid",
		0x03 : "Page ID invalid",
		0x04 : "Picture ID invalid",
		0x05 : "Font ID invalid",
		0x11 : "Baud rate setting invalid",
		0x12 : "Curve control ID number or channel number is invalid",
		0x1A : "Variable name invalid",
		0x1B : "Variable operation invalid",
		0x1C : "Failed to assign",
		0x1D : "Operate EEPROM failed",
		0x1E : "Parameter quantity invalid",
		0x1F : "IO operation failed",
		0x20 : "Undefined escape characters",
		0x23 : "Too long variable name",

	}

	MESSAGES = {
		0x65 : "Touch event return data",
		0x66 : "Current page ID number returns"
	}

	RED    = 63488
	BLUE   =    31
	GRAY   = 33840
	BLACK  =     0
	WHITE  = 65535
	GREEN  =  2016
	BROWN  = 48192
	YELLOW = 65504

	def __init__(self, device_path, page_definitions=None, timeout=None):
		self.pages = []
		self.debug = False

		self.ser = serial.Serial(device_path, 9600, timeout=timeout)
		self.ser.flushOutput()

		if timeout is None:
			self.read_timeout = 0.1
		else:
			self.read_timeout = timeout

		self.log = logging.getLogger("Main.Nex.Protocol")
		self.probe_set_baud()

		while True:
			try:
				self.set_cmd_response_mode(3)
				break
			except Exception as err:
				traceback.print_exc()
				self.log.info("Trying to probe device")
				time.sleep(1)

		if page_definitions is not None:
			for page_definition in page_definitions:
				self.pages.append(Page.new_page_by_definition(self, page_definition))

	def _autobaud(self):
		for baudrate in self.BAUD_VALUES:
			self.log.info("Autobaud: Probing with baudrate: %s", baudrate)
			self.ser.baudrate = baudrate
			for __ in range(2):
				try:
					self.ser.flush()
					self.set_cmd_response_mode(3)
					self.log.info("Autobaud: Connected to display with baudrate %s", baudrate)
					return

				except Exception:
					traceback.print_exc()
					pass


	def probe_set_baud(self):
		self._autobaud()
		self.set_baud(115200, save=True)
		self._autobaud()


	def show_page_by_name(self, name):
		result = None
		for page in self.pages:
			if page.name == name:
				result = page
				break
		return result

	def page_reference(self, page_id):
		if len(self.pages) > page_id:
			return self.pages[page_id]

		page = Page(self, page_id)
		self.pages.append(page)
		return page

	def set_debug(self, debug):
		self.debug = debug

	def set_cmd_response_mode(self, value):
		self.set('bkcmd', value)

	def set_dim(self, value, save=False):
		self.set('dim' + 's' if save else '', value)

	def set_baud(self, baud, save=False):

		self.log.info("Setting display baudrate to %s", baud)
		if baud not in self.BAUD_VALUES:
			raise ValueError("Baud rate not supported: %s" % baud)

		self.set('baud' + ('s' if save else ''), baud)

	def set_page(self, value):
		self.nx_write('page ' + str(value))

	def get_page(self):
		self.ser.flushOutput()
		ret = self.nx_write('sendme')
		if ret[0] == 0x66:
			if ret[1] == 0xff:
				ret[1] = 0x00
			return ret[1]

		raise ValueError(Nextion.get_nx_error_message(0x00))

###############################

	def refresh(self, comp_id="0"):
		self.nx_write('ref %s' % comp_id)

	def get_text(self, comp_id):
		self.nx_write('get %s.txt' % comp_id)
		ret = self.nx_read()
		return ret


	def get_value(self, comp_id):
		self.nx_write('get %s.val' % comp_id)

###############################

	def set_value(self, comp_id, value):
		print(comp_id + '.val="' + str(value) + '"')
		self.nx_write(comp_id + '.val=' + str(value))

	def set_text(self, comp_id, value):
		self.nx_write(comp_id + '.txt="' + str(value) + '"')

	def clear(self, color):
		self.nx_write('cls %s' % color)

	def drawPicture(self, x, y, pic, w=None, h=None):
		if w is None or h is None:
			self.nx_write('pic %s,%s,%s' % (x, y, pic))
		else:
			self.nx_write('picq %s,%s,%s,%s,%s' % (x, y, w, h, pic))

	def drawString(self, x1, y1, x2, y2, fontid, fontcolor, backcolor, xcenter,
				   ycenter, sta, string):
		self.nx_write('xstr %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %
						 (x1, y1, x2 - x1, y2 - y1, fontid, fontcolor,
						  backcolor, xcenter, ycenter, sta, string))

	def drawLine(self, x1, y1, x2, y2, color):
		self.nx_write('line %s,%s,%s,%s,%s' % (x1, y1, x2, y2, color))

	def drawRectangle(self, x1, y1, x2, y2, color):
		self.nx_write('draw %s,%s,%s,%s,%s' % (x1, y1, x2, y2, color))

	def drawBox(self, x1, y1, x2, y2, color):
		self.nx_write('fill %s,%s,%s,%s,%s' % (x1, y1, x2 - x1, y2 - y1, color))

	def drawCircle(self, x, y, r, color):
		self.nx_write('cir %s,%s,%s,%s' % (x, y, r, color))

##############################

	def set(self, key, value, check_return=True):
		self.ser.flushOutput()
		message = key + '=' + str(value)
		self.nx_write(message)
		ret = self.nx_read(check_return=True)

	@staticmethod
	def get_nx_error_message(err_code_char):
		return Nextion.ERRORS[int(err_code_char)]

	def nx_write(self, message):
		message = message.encode("ISO-8859-1")
		message += b"\xFF\xFF\xFF"

		self.log.debug("Transmitting: %s", format(message))
		self.ser.write(message)

	def _read_internal(self, cmax, timeout):

		if timeout is None:
			timeout = self.read_timeout
		bytes_buf = []

		count = 0
		time_now = time.time()
		while timeout == 0 or (time.time() - time_now) < timeout:
			read_byte = self.ser.read()
			if read_byte is None or read_byte == b"":
				continue


			read_char = read_byte[0]

			if read_char == 0xff and not bytes_buf:
				continue

			if read_char != 0x00:
				self.log.debug("Rx: %02x, %s, %s", read_char, len(bytes_buf), count)

				bytes_buf.append(read_char)
				if len(bytes_buf) == cmax:
					return bytes_buf
				if read_char == 0xff:
					count = count + 1
					if count == 3:
						if self.debug is True:
							print("Complete. Returning")
						return bytes_buf
				else:
					count = 0
		return bytes_buf

	def nx_read(self, cmax=0, timeout=None, check_return=True):
		bytes_buf = self._read_internal(cmax, timeout)

		self.log.debug("Read response: %s", format(bytes_buf))

		if not bytes_buf:
			raise ValueError("No response from hardware!")

		if not check_return:
			return bytes_buf
		# 0X65	Touch event return data
		# 0X66	Current page ID number returns
		# 0X67	Touch coordinate data returns
		# 0X68	Touch Event in sleep mode
		# 0X70	String variable data returns
		# 0X71	Numeric variable data returns
		# 0X86	Device automatically enters into sleep mode
		# 0X87	Device automatically wake up
		# 0X88	System successful start up
		# 0X89	Start SD card upgrade
		# 0XFD	Data transparent transmit finished

		fbyte = bytes_buf[0]
		if fbyte in self.ERRORS:
			raise ValueError("Response Error: {} -> {}".format(
				Nextion.get_nx_error_message(fbyte),
				bytes_buf
				))
		expected_postfix = [255, 255, 255]
		if bytes_buf[-3:] != expected_postfix:
			raise ValueError("Response missing trailing bytes: {} -> {} != {}".format(
				bytes_buf, bytes_buf[-3:], expected_postfix))

		# Truncate the type and postfix
		bytes_buf = bytes_buf[1:-3]

		if fbyte == 0x01:
			return bytes_buf
		elif fbyte == 0x65:  # Touch event return data
			pass
		elif fbyte == 0x66:  # Current page ID number returns
			pass
		elif fbyte == 0x67:  # Touch coordinate data returns
			pass
		elif fbyte == 0x68:  # Touch Event in sleep mode
			pass
		elif fbyte == 0x70:  # String variable data returns
			strb = "".join([chr(b) for b in bytes_buf])
			return strb
		elif fbyte == 0x71:  # Numeric variable data returns
			print("Numeric data:", bytes_buf)
			pass
		elif fbyte == 0x86:  # Device automatically enters into sleep mode
			pass
		elif fbyte == 0x87:  # Device automatically wake up
			pass
		elif fbyte == 0x88:  # System successful start up
			pass
		elif fbyte == 0x89:  # Start SD card upgrade
			pass
		elif fbyte == 0xfd:  # Data transparent transmit finished
			pass
		else:
			raise ValueError("Response Error with unknown code: {}".format(bytes_buf))



if __name__ == "__main__":
	#ser=serial.Serial('/dev/ttyMCC',9600,timeout=0)
	port = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600, timeout=0)
	port.flushOutput()
	nextion = Nextion(port)
	print('Serial connected')
	#nextion.set_dim(50)
	#for p in range(0,3):
	#  nextion.set_page(p)
	#  nextion.set_text('t0',"Fede<3")
	#  print(nextion.get_page())
	#nextion.set_dim(100)

	pageBoatSpeed = nextion.page_reference(0)
	pageHeading = nextion.page_reference(1)
	pageWindSpeed = nextion.page_reference(2)

	txtBoatSpeedValue = pageBoatSpeed.hook_text("t1")
	txtBoatSpeedAttr = pageBoatSpeed.hook_text("t2")
	txtBoatSpeedUnit = pageBoatSpeed.hook_text("t3")

	txtHeadingValue = pageBoatSpeed.hook_text("t1")
	txtHeadingTrueMag = pageBoatSpeed.hook_text("t3")

	txtWindSpeedValue = pageWindSpeed.hook_text("t1")
	txtWindSpeedTrueApp = pageWindSpeed.hook_text("t2")
	txtWindSpeedUnit = pageWindSpeed.hook_text("t3")

	pageBoatSpeed.show()
	txtBoatSpeedValue.set(2.2)
	pageHeading.show()
	txtHeadingValue.set(300)
	pageWindSpeed.show()
	txtWindSpeedValue.set(3.75)

	nextion.clear(Nextion.RED)
	nextion.drawBox(0, 0, 100, 100, Nextion.BLUE)
	nextion.drawRectangle(0, 0, 100, 100, Nextion.YELLOW)
	nextion.drawLine(0, 0, 100, 100, Nextion.GREEN)
	nextion.drawCircle(100, 100, 50, Nextion.BROWN)
	#nextion.drawString(0,0,400,200,2,4096,3072,1,1,1,"*")

	pageBoatSpeed.show()
	txtBoatSpeedValue.set("Fede<3")
