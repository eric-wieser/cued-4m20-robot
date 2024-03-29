from struct import Struct

class DecodeError(ValueError): pass

class Message(tuple):
	""" base class for all messages """

	@staticmethod
	def deserialize(data: bytes) -> 'Message':
		if len(data) < 1:
			raise DecodeError("Packet is empty!")

		header, rest = data[:1], data[1:]

		for m_type in Message.__subclasses__():
			if m_type.code == header:
				break
		else:
			raise DecodeError('Unrecognized message code {:c}'.format(data[0]))

		if len(rest) != m_type.fmt.size:
			raise DecodeError('Packet is of length {}, but {} is of length {}'.format(
				len(rest), m_type.__name__, m_type.fmt.size
			))

		fields = m_type.fmt.unpack(data[1:])
		return m_type(fields)

	def serialize(self) -> bytes:
		return self.code + self.fmt.pack(*self)

# these should match the definitions in messages.h

class ServoPulse(Message):
	code = b'C'
	fmt = Struct('<HHH')

class ServoForce(Message):
	code = b'F'
	fmt = Struct('<HHH')

class ServoPosition(Message):
	code = b'T'
	fmt = Struct('<HHH')

class JointConfig(Message):
	code = b'J'
	fmt = Struct('<HHHHHfff')

class Sensor(Message):
	code = b'S'
	fmt = Struct('<HHH')

class Ping(Message):
	code = b'P'
	fmt = Struct('')

class IMUScaled(Message):
	code = b'I'
	fmt = Struct('<fffffffff')

	acc  = property(lambda s: s[0:3])
	gyro = property(lambda s: s[3:6])
	mag  = property(lambda s: s[6:9])

if __name__ == '__main__':
	m = Sensor((1, 2, 3))
	s = m.serialize()

	m2 = Message.deserialize(s)
	assert m == m2


	x = JointConfig((550, 2300, 520, 527, 528, 3.5629741813333333, 3.5384019456, 3.4319222574222223))
	s = x.serialize()
	print(s, len(s), JointConfig.fmt.size)
	s = s[:-12] + s[-12:-8][::-1] + s[-8:-4][::-1] + s[-4:][::-1]
	print(Message.deserialize(s))