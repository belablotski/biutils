"""
Translate SQL code into SAP BODS sql() function calls.
Script splits SQL statements from input file by ';' symbol at the end of line.
Then each statement is wrapped into BODS sql() function call.
"""

import sys, re, os.path

class SqlToBodsTranslator(object):
    def __init__(self, filename):
        self.sql = None
        F = open(filename, "rt")
        try:
            self.sql = F.read()
            self.__parse()
        finally:
            F.close()
            
    def __parse(self):
        self.statements = re.split("(?m);\\s*$", self.sql)
        
    def gen_bods_code(self, bods_datastore):
        res = ""
        for stat in self.statements:
            if len(stat.strip()) == 0:
                continue
            lines = stat.split('\n')
            res += "sql('%s', ''\n" % bods_datastore
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                res += "  || '%s '\n" % line.replace("'", "\\'")
            res += ");\n\n"
        return res
    
            
#sqlt = SqlToBodsTranslator("deploy_landing_objects.sql")
#sqlt = SqlToBodsTranslator("VEOL-BID_1.1.0.1_hotfix_1.sql")
#sqlt = SqlToBodsTranslator("test1.sql")
#print sqlt.gen_bods_code("ds_HRLand")

if len(sys.argv) not in (3, 4):
    print __doc__
    print "Usage: %s bods_datastore_name input_file [output_file]" % os.path.split(sys.argv[0])[1]
    print "If output_file is missed, the STDOUT is used instead."
else:
    datastore_name = sys.argv[1].strip()
    input_file_name = sys.argv[2].strip()
    if len(sys.argv) == 4:
        Fout = open(sys.argv[3].strip(), "wt")
    else:
        Fout = sys.stdout
    sqlt = SqlToBodsTranslator(input_file_name)
    Fout.write(sqlt.gen_bods_code(datastore_name))
    Fout.close()