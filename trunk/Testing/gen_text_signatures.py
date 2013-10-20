"""
Parse Oracle and Microsoft SQL Server columns metadata and generate queries for calculating text signatures.
Typically there signatures are used for testing purposes to compate Source and Target data.

TODO: Add TEXT/CLOB fields. May be use substring from the beginning/ending of text + length.
TODO: Code is now mostly duplicated for SQL Server and Oracle - do refactoring (generalization).
"""

NULL_SIGNATURE = "<*~NuLL*~>"                                    # NULLs marker
FIELD_DELIMETER = "=~|*="                                           # Fields separator
TEXT_SIGNATURE_FIELD_NAME = "TEXT_SIGNATURE"           # Name for field with text signature 


# In CRDN_SRC field names are unique across whole database.
# TODO: add schema/table name here (exclude fields more specifically)

# List of ignored (mostly system or not-supported fields.
FIELDS_IGNORE_LIST = ["DW_PROCESS_WID", "DW_SOURCE_WID", "DW_CREATE_DTM",  # DWH system fields
    # timestamp from CRDN_SRC - not used
    "BbUpsize_ts", 
    
    # TEXT/CLOB
    "BbCode",
    "BbWizard",
    "BBCODE",
    "BBWIZARD",
]

FLOAT_FIELDS_LIST = [
    # MS
    "BbPerPayDivisor",
    
    # Ora
    "BBPERPAYDIVISOR",
]

# List of varchar columns which should be converted to NULL if they contain Empty sting in MS Sql Server
# Be aware - this affects Sql Server analyzer - so it's case sensitive,
NULL_IF_EMPTY_LIST = [
    # BenBase
    "BbAdvanced", 
    "BbArchive", 
    "BbDescrip", 
    "BbElectionSet", 
    "BbEquivGroup", 
    "BbKind", 
    "BbPrintDescrip", 
    "BbRecType", 
    "BbTax", 
    "BbType", 
    "BbUserName", 
]
assert len(NULL_IF_EMPTY_LIST) == len(set(NULL_IF_EMPTY_LIST))


def error(msg):
    # TODO: switch to assert False, msg
    print "ERROR: %s" % msg


class SqlServerMetadataAnalyzer(object):
    """
    Parse columns metadata (result set of saved into text file):
    
    select table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision, character_set_catalog, character_set_schema, character_set_name, collation_catalog, collation_schema, collation_name, domain_catalog, domain_schema, domain_name
    from information_schema.columns
    where table_catalog = 'xxx' and table_schema = 'dbo' and table_name in ('xxx')
    order by table_catalog, table_schema, table_name, upper(column_name);
    
    Generate query which produces text-based signature for each table row.
    """

    class ColMetadata(object):
        def __init__(self, table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision, character_set_catalog, character_set_schema, character_set_name, collation_catalog, collation_schema, collation_name, domain_catalog, domain_schema, domain_name):
            self.table_catalog = table_catalog
            self.table_schema = table_schema
            self.table_name = table_name
            self.column_name = column_name
            self.ordinal_position = int(ordinal_position)
            self.column_default = column_default
            assert is_nullable in ('YES', 'NO')
            self.is_nullable = (is_nullable == 'YES');
            self.data_type = data_type
            if len(character_maximum_length) == 0:
                self.character_maximum_length = None
            else:
                self.character_maximum_length = int(character_maximum_length)
            self.character_octet_length = character_octet_length
            if len(numeric_precision) == 0:
                self.numeric_precision = None
            else:
                self.numeric_precision = int(numeric_precision)
            if len(numeric_precision_radix) == 0:
                self.numeric_precision_radix = None
            else:
                self.numeric_precision_radix = int(numeric_precision_radix)
            if len(numeric_scale) == 0:
                self.numeric_scale = None
            else:
                self.numeric_scale = int(numeric_scale)
            self.datetime_precision = datetime_precision
            self.character_set_catalog = character_set_catalog
            self.character_set_schema = character_set_schema
            self.character_set_name = character_set_name
            self.collation_catalog = collation_catalog
            self.collation_schema = collation_schema
            self.collation_name = collation_name
            self.domain_catalog = domain_catalog
            self.domain_schema = domain_schema
            self.domain_name = domain_name
            
        def __str__(self):
            return str(self.__dict__)
            
        def get_text_signature(self):
            res = ""
            if self.data_type in ('int'):
                assert self.numeric_precision_radix == 10
                res = "cast([%s] as varchar(%d))" % (self.column_name, max(self.numeric_precision+1, len(NULL_SIGNATURE)))
            elif self.data_type in ('numeric'):
                assert self.numeric_precision_radix == 10
                res = "cast([%s] as varchar(%d))" % (self.column_name, max(self.numeric_precision+2, len(NULL_SIGNATURE)))
            elif self.data_type in ('money'):
                assert self.numeric_precision_radix == 10
                #error("Placeholder for MONEY type (in %s.%s.%s.%s)." % (self.table_catalog, self.table_schema, self.table_name, self.column_name))
                res = "cast(cast([%s] as decimal(%d, %d)) as varchar(%d))" % (self.column_name, self.numeric_precision, self.numeric_scale, max(self.numeric_precision+2, len(NULL_SIGNATURE)))
            elif self.data_type in ('float'):
                #t = "replace(ltrim(rtrim(replace(str([%s], 38, 12), '0',  ' '))), ' ', '0')" % self.column_name
                #t = "(case when left(%s, 1) = '.' then '0' else '' end) + %s + (case when right(%s, 1) = '.' then '0' else '' end)" % (t, t, t)
                ## BODS-specific issue: truncates after 16 digit (BODS double type used in datastore)
                #nn = 16+1   # 16 digits + dot
                #res = "case when len(%s) >= %d then substring((%s), 1, %d) else (%s) end" % (t, nn, t, nn-1, t)
                t = "replace(ltrim(rtrim(replace(str([%s], 38, 15), '0',  ' '))), ' ', '0')" % self.column_name
                res = "(case when left(%s, 1) = '.' then '0' else '' end) + %s + (case when right(%s, 1) = '.' then '0' else '' end)" % (t, t, t)
            elif self.data_type in ('datetime'):
                res = "convert(varchar(23), [%s], 121)" % (self.column_name,)
            elif self.data_type in ('varchar'):
                res = "[%s]" % (self.column_name,)
                if self.column_name in NULL_IF_EMPTY_LIST:
                    res = "nullif(%s, '')" % res
                else:
                    res = "case when %s = '' then '|' else %s end" % (res, res)
                if self.is_nullable or self.column_name in NULL_IF_EMPTY_LIST:
                    assert self.character_maximum_length is not None
                    res = "cast(%s as varchar(%d))" % (res, max(len(NULL_SIGNATURE), self.character_maximum_length))
            elif self.data_type in ('text'):
                error("Placeholder for TEXT type (in %s.%s.%s.%s)." % (self.table_catalog, self.table_schema, self.table_name, self.column_name))
                res = "'@!@!@!'"
            elif self.data_type in ('timestamp'):
                res = "upper(sys.fn_varbintohexstr([%s]))" % (self.column_name,)
            else:
                error("Data type '%s' isn't supported (in %s.%s.%s.%s)." % (self.data_type, self.table_catalog, self.table_schema, self.table_name, self.column_name))
            if self.is_nullable and self.data_type not in ('float'):
                res = "isnull(%s, '%s')" % (res, NULL_SIGNATURE)
            return res

    
    def __init__(self, file_path):
        """
        Params:
            file_path - path to file with tables columns metadata.
        """
        self.cols = []
        F = open(file_path)
        try:
            lines = F.readlines()
            for line in lines:
                coldef = line.split('\t')
                colmeta = self.ColMetadata(*coldef)
                self.cols += [colmeta]
        finally:
            F.close()
    
    def get_table_list(self):
        """
        Return list of tables which metadata is loaded.
        Returns:
            list of tuples (catalog, schema, table)
        """
        return list(set([(c.table_catalog, c.table_schema, c.table_name) for c in self.cols]))
    
    def gen_text_signature_query(self, tables = None, concat_cols = True, concat_cols_row_number_sort = True, add_row_number = True):
        """
        Generate query for produce rows text signatures.
        Params:
            tables - list of tables for generating queries (each table us specified by tuple (catalog, schema, table)) or None - generate queries for all tables.
            concat_cols - concatenate all columns into one string
            concat_cols_row_number_sort - sort by row_number(), works if concat_cols is True only
            add_row_number - add row_numer() column
        """
        result = []
        if tables is None:
            tables = self.get_table_list()
        for table in tables:
            res = ""
            colsql = []
            if add_row_number:
                colsql += ["~~~SYSTEM_FIELDS_PLACEHOLDER~~~"]
            orderby = []
            ignored = []
            float_fields = []
            table_cols = [c for c in self.cols if c.table_catalog==table[0] and c.table_schema==table[1] and c.table_name==table[2]]
            for col in table_cols:
                if col.column_name not in FIELDS_IGNORE_LIST and col.column_name not in FLOAT_FIELDS_LIST:
                    colsql += [col.get_text_signature() + (concat_cols and " " or (" as " + col.column_name)).rstrip()]
                    orderby += [col]
                else:
                    if col.column_name in FLOAT_FIELDS_LIST:
                        float_fields += [col]
                    else:
                        ignored += [col]
            tabcols = (concat_cols and ("\r\n  + '%s' +" % FIELD_DELIMETER) or  "\r\n  , ").join(colsql)
            res += """SELECT %s\r\nFROM %s\r\n""" % (tabcols + (concat_cols and (" as " + TEXT_SIGNATURE_FIELD_NAME) or " ").rstrip(), ".".join(["[%s]" % t for t in table]))
            row_number_f = "ROW_NUMBER() OVER (ORDER BY %s)" % ("\r\n  , ".join(["%s collate Latin1_General_Bin" % c.get_text_signature() for c in orderby]))
            if concat_cols:
                res += """ORDER BY %s;\r\n""" % (concat_cols_row_number_sort and row_number_f or TEXT_SIGNATURE_FIELD_NAME + " collate Latin1_General_Bin", )
                row_number_f = "replicate('0', 10-len(%s)) + cast(%s as varchar(10))" % (row_number_f, row_number_f)
            else:
                res += """ORDER BY %s collate Latin1_General_Bin;\r\n""" % ("\r\n  , ".join(["%s" % c.column_name for c in orderby]))
            res = res.replace("~~~SYSTEM_FIELDS_PLACEHOLDER~~~", row_number_f)
            res = "/* IGNORED FIELDS: %s */\r\n%s" % (", ".join(["%s" % c.column_name for c in ignored]), res)
            res = "/* FLOAT FIELDS (EXCLUDED): %s */\r\n%s" % (", ".join(["%s" % c.column_name for c in float_fields]), res)
            res = "-- Table: %s\r\n%s" % (".".join(["[%s]" % t for t in table]), res)
            
            if len(float_fields) > 0:
                res += """\r\n-- Float fields contain imprecise data, compare they separately with fc_float utility."""
                res += """\r\nSELECT %s\r\nFROM %s\r\n""" % ("\r\n  , ".join(["%s as %s" % (f.get_text_signature(), f.column_name) for f in float_fields]), ".".join(["[%s]" % t for t in table]))
                res += """ORDER BY %s;\r\n""" % (row_number_f)
                
            result += [res + "\r\n"]
        return "\r\n".join(result)


class OracleMetadataAnalyzer(object):
    """
    Parse columns metadata (result set of saved into text file):
    
    select owner, table_name, column_name, data_type, data_type_mod, data_type_owner, data_length, data_precision, data_scale, nullable, column_id, default_length, data_default, character_set_name, char_col_decl_length, char_length, char_used, v80_fmt_image, data_upgraded, hidden_column, virtual_column, qualified_col_name
    from all_tab_cols
    where owner = 'xxx' and table_name in ('xxx')
    order by owner, table_name, column_name;
    
    Generate query which produces text-based signature for each table row.
    """

    class ColMetadata(object):
        def __init__(self, owner, table_name, column_name, data_type, data_type_mod, data_type_owner, data_length, data_precision, data_scale, nullable, column_id, default_length, data_default, character_set_name, char_col_decl_length, char_length, char_used, v80_fmt_image, data_upgraded, hidden_column, virtual_column, qualified_col_name):
            self.owner = owner
            self.table_name = table_name
            self.column_name = column_name
            self.data_type = data_type
            self.data_type_mod = data_type_mod
            self.data_type_owner = data_type_owner
            self.data_length = int(data_length)
            if len(data_precision) == 0:
                self.data_precision = None
            else:
                self.data_precision = int(data_precision)
            if len(data_scale) == 0:
                if self.data_precision is None:
                    self.data_scale = None
                else:
                    self.data_scale = 0         #  If no scale is specified, the scale is zero.
            else:
                self.data_scale = int(data_scale)
            assert nullable in ('Y', 'N')
            self.nullable = (nullable=='Y')
            self.column_id = int(column_id)
            self.default_length = default_length
            self.data_default = data_default
            self.character_set_name = character_set_name
            self.char_col_decl_length = char_col_decl_length
            self.char_length = char_length
            self.char_used = char_used
            self.v80_fmt_image = v80_fmt_image
            self.data_upgraded = data_upgraded
            self.hidden_column = hidden_column
            self.virtual_column = virtual_column
            self.qualified_col_name = qualified_col_name
            
        def __str__(self):
            return str(self.__dict__)
            
        def get_text_signature(self):
            res = ""
            if self.data_type in ("NUMBER"):
                #print (self.column_name, self.data_type, self.data_precision, self.data_scale)
                if self.data_precision is None:
                    fmt_mask = 'FM' + ('9' * 37) + '0.0' + ('9' * 23)
                else:
                    fmt_mask = 'FM' + ('9' * (self.data_precision-1)) + '0.' + ('0' * self.data_scale)
                res = "rtrim(to_char(%s, '%s'), '.')" % (self.column_name, fmt_mask)
            elif self.data_type in ("DATE"):
                res = "to_char(%s, 'YYYY-MM-DD HH24:MI:SS')" % (self.column_name, )
            elif self.data_type.startswith("TIMESTAMP"):
                res = "to_char(%s, 'YYYY-MM-DD HH24:MI:SS.FF%s')" % (self.column_name, self.data_scale)
            elif self.data_type in ("VARCHAR2"):
                res = "%s" % (self.column_name, )
            elif self.data_type in ("CLOB"):
                error("Placeholder for CLOB type")
                res = "'@!@!@!'"
            else:
                error("Data type '%s' isn't supported (in %s.%s.%s)." % (self.data_type, self.owner, self.table_name, self.column_name))
            if self.nullable and self.column_name not in FLOAT_FIELDS_LIST:
                res = "nvl(%s, '%s')" % (res, NULL_SIGNATURE)
            return res

    
    def __init__(self, file_path):
        """
        Params:
            file_path - path to file with tables columns metadata.
        """
        self.cols = []
        F = open(file_path)
        try:
            lines = F.readlines()
            for line in lines:
                coldef = line.split('\t')
                colmeta = self.ColMetadata(*coldef)
                self.cols += [colmeta]
        finally:
            F.close()
    
    def get_table_list(self):
        """
        Return list of tables which metadata is loaded.
        Returns:
            list of tuples (schema, table)
        """
        return list(set([(c.owner, c.table_name) for c in self.cols]))
    
    def gen_text_signature_query(self, tables = None, concat_cols = True, concat_cols_row_number_sort = True, add_row_number = True):
        """
        Generate query for produce rows text signatures.
        Params:
            tables - list of tables for generating queries (each table us specified by tuple (schema, table)) or None - generate queries for all tables.
            concat_cols - concatenate all columns into one string
            concat_cols_row_number_sort - sort by row_number(), works if concat_cols is True only
            add_row_number - add row_numer() column
        """
        result = []
        if tables is None:
            tables = self.get_table_list()
        for table in tables:
            res = ""
            colsql = []
            if add_row_number:
                colsql += ["~~~SYSTEM_FIELDS_PLACEHOLDER~~~"]
            orderby = []
            ignored = []
            float_fields = []
            table_cols = [c for c in self.cols if c.owner==table[0] and c.table_name==table[1]]
            for col in table_cols:
                if col.column_name not in FIELDS_IGNORE_LIST and col.column_name not in FLOAT_FIELDS_LIST:
                    colsql += [col.get_text_signature() + (concat_cols and " " or (" as " + col.column_name)).rstrip()]
                    orderby += [col]
                else:
                    if col.column_name in FLOAT_FIELDS_LIST:
                        float_fields += [col]
                    else:
                        ignored += [col]
            tabcols = (concat_cols and ("\r\n  || '%s' || " % FIELD_DELIMETER) or  "\r\n  , ").join(colsql)
            res += """SELECT %s\r\nFROM %s\r\n""" % (tabcols + (concat_cols and (" as " + TEXT_SIGNATURE_FIELD_NAME) or " ").rstrip(), ".".join(["%s" % t for t in table]))
            row_number_f = "ROW_NUMBER() OVER (ORDER BY %s)" % ("\r\n  , ".join(["%s NULLS FIRST" % c.get_text_signature() for c in orderby]))
            if concat_cols:
                res += """ORDER BY %s;\r\n""" % (concat_cols_row_number_sort and row_number_f or TEXT_SIGNATURE_FIELD_NAME, )
                row_number_f = "to_char(%s, 'FM0000000000')" % row_number_f
            else:
                res += """ORDER BY %s;\r\n""" % ("\r\n  , ".join(["%s NULLS FIRST" % c.column_name for c in orderby]))
            res = res.replace("~~~SYSTEM_FIELDS_PLACEHOLDER~~~", row_number_f)
            res = "/* IGNORED FIELDS: %s */\r\n%s" % (", ".join(["%s" % c.column_name for c in ignored]), res)
            res = "/* FLOAT FIELDS (EXCLUDED): %s */\r\n%s" % (", ".join(["%s" % c.column_name for c in float_fields]), res)
            res = "-- Table: %s\r\n%s" % (".".join(["%s" % t for t in table]), res)
            
            if len(float_fields) > 0:
                res += """\r\n-- Float fields contain imprecise data, compare they separately with fc_float utility."""
                res += """\r\nSELECT %s\r\nFROM %s\r\n""" % ("\r\n  , ".join(["%s as %s" % (f.get_text_signature(), f.column_name) for f in float_fields]), ".".join(["%s" % t for t in table]))
                res += """ORDER BY %s;\r\n""" % (row_number_f)
            
            result += [res + "\r\n"]
        return "\r\n".join(result)


sqlservanalyzer = SqlServerMetadataAnalyzer("unittests/gen_text_signatures/mssql_tab_cols.txt")
print "Microsoft SQL Server Tables: %s\r\n" % (", ".join(["%s.%s.%s" % tuple(x) for x in sqlservanalyzer.get_table_list()]))
print sqlservanalyzer.gen_text_signature_query(concat_cols =  True, concat_cols_row_number_sort = True, add_row_number = False)

oracleanalyzer = OracleMetadataAnalyzer("unittests/gen_text_signatures/oracle_tab_cols.txt")
print "ORACLE Tables: %s\r\n" % (", ".join(["%s.%s" % tuple(x) for x in oracleanalyzer.get_table_list()]))
print oracleanalyzer.gen_text_signature_query(concat_cols =  True, concat_cols_row_number_sort = True, add_row_number = False)
