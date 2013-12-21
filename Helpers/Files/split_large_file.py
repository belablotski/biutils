"""Split large file into smaller chunks."""

def split_file(fname, chunk_size):
	"""Splits file and returns list of chunks."""
	result = []
	F = open(fname, "rb")
	n = 0
	try:
		while True:
			buf = F.read(chunk_size)
			if not buf:
				break
			fname_out = "%s.%03d" % (fname, n)
			print "Writing %s" % fname_out
			FF = open(fname_out, "wb")
			try:
				FF.write(buf)
				del buf
			finally:
				FF.close()
			n += 1
			result.append(fname_out)
	finally:
		F.close()
	print
	print "Join files (Linux/Windows):"
	print "cat %s > %s" % (" ".join(result), fname)
	print "copy /b %s %s" % ("+".join(result), fname)
	return result

split_file("Oracle_Developer_Day.ova", 2**30)
