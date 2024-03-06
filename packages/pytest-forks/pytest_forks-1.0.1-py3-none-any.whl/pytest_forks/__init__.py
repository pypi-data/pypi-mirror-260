import os, pytest, sys, traceback

from typing import Any

class forks:
	def __enter__(self) -> None:
		self.pid = os.getpid()
		rfd, wfd = os.pipe()
		self.reader = os.fdopen(rfd, 'r')
		self.writer = os.fdopen(wfd, 'wb', buffering=0)
	def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
		if os.getpid() == self.pid:
			# in parent
			self.writer.close()
			# repeat logs without mixing them while also conserving memory
			childError = False
			buffer = ''
			for line in self.reader:
				childError = True
				buffer += line
				end = buffer.rfind('\n\n')
				if end >= 0:
					sys.stderr.write(buffer[:end + 2])
					buffer = buffer[end + 2:]
			if buffer:
				sys.stderr.write(buffer)
			# report if a child had an error
			if childError:
				pytest.fail('At least one forked child did not exit cleanly.')
		else: # pragma:nocover
			# in child
			try:
				self.reader.close()
				# warn parent
				if exc_type is None:
					self.writer.write('Forked child failed to call os._exit.\n'.encode('utf-8'))
				else:
					self.writer.write(b'Forked child exited with an error:\n' + b''.join(line.encode('utf-8') for line in traceback.format_exception(exc_type, exc_value, exc_traceback)) + b'\n')
			finally:
				# alway exit cleanly
				raise os._exit(1)
