"""
Process text file in the specified lines range.
"""

class TextFileProcessor(object):
    TICK_EACH_N_LINES = 10000
    
    def __init__(self, in_file_path, out_file_path):
        self.in_file = open(in_file_path, "rt")
        self.out_file = open(out_file_path, "wt")
        
    def __warning(self, msg):
        print "Warning: " % msg
    
    def __process_line(self, line):
        if line.startswith('"'):
            if line.endswith('"'):
                self.out_file.write(line[1:-1])
            elif line.endswith('"\n'):
                self.out_file.write(line[1:-2] + '\n')
            else:
                self.out_file.write(line)
                #self.__warning("Invalid line structure (end).")
        else:
            self.out_file.write(line)
            #self.__warning("Invalid line structure (begin).")
    
    def process(self, from_line, to_line):
        line_no = 1
        try:
            line = self.in_file.readline()
            while len(line) > 0:
                if line_no >= from_line and line_no <= to_line:
                    self.__process_line(line)
                if line_no > to_line:
                    print "End of file has been skipped..."
                    break
                line = self.in_file.readline()
                line_no += 1
                if line_no % self.TICK_EACH_N_LINES == 0:
                    print "Lines processed: %d" % line_no
        finally:
            self.in_file.close()
            self.out_file.close()

files = ["CheckSumm_ms.txt", "CheckSumm_ora.LST"]
for file in files:
	print file
	tp = TextFileProcessor(file, file+".new")
	tp.process(1, 1e5)