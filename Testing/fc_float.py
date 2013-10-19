"""
Compare two text files which contain several tab-separated columns with float numbers.
The comparison based on maximum delta between two non-precise numbers which is 
calculated based on FLOAT_MAX_PRECISION_DIGITS constant.
Strings "NULL" treated as empty strings.
Process Exit code is 0 if no differences and 1 if there are some differences.
Usage: provide two command line arguments - paths for files for comparison.
"""

import sys

FLOAT_MAX_PRECISION_DIGITS = 15
TICK_EACH_N_LINES = 10000

def compare_lines_with_float_numbers(line1, line2):
    """Returns list with positions of different numbers. If list is empty - there are no differences."""
    def line_to_float(line):
        line = line.replace("NULL", "")
        c = [x.strip() for x in line.split('\t')]
        c = [None if len(x) == 0 else float(x) for x in c]
        return c
        
    def cmp_nullable_float(fl1, fl2):
        if fl1 is None and fl2 is None:
            return True
        elif fl1 is None and not(fl2 is None) or not(fl1 is None) and fl2 is None:
            return False
        else:
            il = max(len(str(int(fl1))), len(str(int(fl2))))
            assert FLOAT_MAX_PRECISION_DIGITS-il > 0, "Not tested with so big numbers"
            delta = 10**-(FLOAT_MAX_PRECISION_DIGITS-il)
            #print fl1, fl2, delta
            return abs(fl1 - fl2) < delta

    #print line_to_float(line1)
    #print line_to_float(line2)
    f1 = line_to_float(line1)
    f2 = line_to_float(line2) 
    assert len(f1) == len(f2), "Lines has different length %s and %s" % (f1, f2)
    cmp = [cmp_nullable_float(f1[i], f2[i]) for i in range(len(f1))]
    return [i for i in range(len(cmp)) if not cmp[i]]

def compare_files_with_float_numbers(f1, f2):
    def remove_unicode_mask(s):
        if s.startswith(chr(0xEF) + chr(0xBB) + chr(0xBF)):
            return s[3:]
        else:
            return s
    
    print "Comparing %s and %s..." % (f1, f2)
    F1 = open(f1, "rt")
    F2 = open(f2, "rt")
    line_no = 1
    diff_cnt = 0
    line1 = remove_unicode_mask(F1.readline())
    assert len(line1) > 0, "File %s is empty" % f1
    line2 = remove_unicode_mask(F2.readline())
    assert len(line2) > 0, "File %s is empty" % f2
    while len(line1) > 0 and len(line2) > 0:
        diff_positions = compare_lines_with_float_numbers(line1, line2)
        if (len(diff_positions) > 0):
            diff_cnt += 1
            print "Difference #%d in line %d column(s) %s" % (diff_cnt, line_no, ','.join([str(x) for x in diff_positions]))
            print line1
            print line2
        line1 = F1.readline()
        line2 = F2.readline()
        assert not (len(line1) > 0 and len(line2) == 0), "EOF has been reached in %s, but there are additional lines in file %s." % (f2, f1)
        assert not (len(line1) == 0 and len(line2) > 0), "EOF has been reached in %s, but there are additional lines in file %s." % (f1, f2)
        line_no += 1
        if line_no % TICK_EACH_N_LINES == 0:
            print "Lines processed: %d" % line_no

    if diff_cnt > 0:
        print "There are %d differences (float precision is %d digits)." % (diff_cnt, FLOAT_MAX_PRECISION_DIGITS)
    else:
        print "Float numbers in two files are identical (float precision is %d digits)." % FLOAT_MAX_PRECISION_DIGITS
            
    F1.close()
    F2.close()
    return diff_cnt == 0


if len(sys.argv) != 3:
    print __doc__
    print "Current FLOAT_MAX_PRECISION_DIGITS = %d\r\n" % FLOAT_MAX_PRECISION_DIGITS
    print "There is wrong number of command line arguments."
else:
    compare_files_with_float_numbers(sys.argv[1], sys.argv[2]) and exit(0) or exit(1)
