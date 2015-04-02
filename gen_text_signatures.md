# Introduction #
Parse Oracle and Microsoft SQL Server columns metadata and generate queries for calculating text signatures.

To generate record signature all fields are converted to strings and concatenated. Float fields are excluded, because they are imprecise. There is additional query is generated for floats - after that files should be compared with [fc\_float](fc_float.md) utility.

Typically there signatures are used for testing purposes to compate Source and Target data.

It's good idea to use hash instead of long strings, but in Oracle you should have right to execute function from sys.dbms\_obfuscation\_toolkit. In this case in't possible to use HASHBYTES in SQL Server. Unfortunately Oracle's STANDARD\_HASH is in 12c only and ORA\_HASH doesn't have equivalent in SQL Server.

# Demo #

## Queries to extract metadata ##
Metadata just copied form oracle SQL Developer output grid and stored into mssql\_tab\_cols.txt and oracle\_tab\_cols.txt

```
-- MS SQL Server
select table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision, character_set_catalog, character_set_schema, character_set_name, collation_catalog, collation_schema, collation_name, domain_catalog, domain_schema, domain_name
from information_schema.columns
where table_catalog = 'CRDN_SRC' and table_schema = 'dbo' and table_name in ('BenBase')
order by table_catalog, table_schema, table_name, upper(column_name);
```

```
-- ORACLE
select owner, table_name, column_name, data_type, data_type_mod, data_type_owner, data_length, data_precision, data_scale, nullable, column_id, default_length, data_default, character_set_name, char_col_decl_length, char_length, char_used, v80_fmt_image, data_upgraded, hidden_column, virtual_column, qualified_col_name
from all_tab_cols
where owner = 'DWH' and table_name in ('BENBASE')
order by owner, table_name, column_name;
```

## Generated queries ##
```
Microsoft SQL Server Tables: CRDN_SRC.dbo.BenBase

-- Table: [CRDN_SRC].[dbo].[BenBase]
/* FLOAT FIELDS (EXCLUDED): BbPerPayDivisor */
/* IGNORED FIELDS: BbCode, BbUpsize_ts, BbWizard */
SELECT isnull(cast(case when [BbAccrualMethod] = '' then '|' else [BbAccrualMethod] end as varchar(30)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbAdvanced], '') as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbArchive], '') as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbBeneficiaryFlag] = '' then '|' else [BbBeneficiaryFlag] end as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbBillMthd] = '' then '|' else [BbBillMthd] end as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast([BbCRC] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateAdd], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateBeg], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateDel], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateEnd], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateMod], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateRBeg], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(convert(varchar(23), [BbDateREnd], 121), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbDepCovFlag] = '' then '|' else [BbDepCovFlag] end as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbDescrip], '') as varchar(30)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbDfltTier] = '' then '|' else [BbDfltTier] end as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +cast(nullif([BbElectionSet], '') as varchar(10))
  + '=~|*=' +cast(nullif([BbEquivGroup], '') as varchar(10))
  + '=~|*=' +cast([BbFlxID] as varchar(11))
  + '=~|*=' +isnull(cast([BbFlxIDBe] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast([BbFlxIDCf] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbGroup] = '' then '|' else [BbGroup] end as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbInfo1] = '' then '|' else [BbInfo1] end as varchar(30)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbKind], '') as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast([BbMagic] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast([BbNote] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbPrintDescrip], '') as varchar(30)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(case when [BbProperties] = '' then '|' else [BbProperties] end as varchar(20)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbRecType], '') as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast([BbSource] as varchar(11)), '<*~NuLL*~>')
  + '=~|*=' +isnull(cast(nullif([BbTax], '') as varchar(10)), '<*~NuLL*~>')
  + '=~|*=' +case when [BbTier] = '' then '|' else [BbTier] end
  + '=~|*=' +cast(nullif([BbType], '') as varchar(10))
  + '=~|*=' +isnull(cast(nullif([BbUserName], '') as varchar(20)), '<*~NuLL*~>') as TEXT_SIGNATURE
FROM [CRDN_SRC].[dbo].[BenBase]
ORDER BY ROW_NUMBER() OVER (ORDER BY isnull(cast(case when [BbAccrualMethod] = '' then '|' else [BbAccrualMethod] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbAdvanced], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbArchive], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBeneficiaryFlag] = '' then '|' else [BbBeneficiaryFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBillMthd] = '' then '|' else [BbBillMthd] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbCRC] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateAdd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateDel], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateEnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateMod], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateRBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateREnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDepCovFlag] = '' then '|' else [BbDepCovFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDfltTier] = '' then '|' else [BbDfltTier] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , cast(nullif([BbElectionSet], '') as varchar(10)) collate Latin1_General_Bin
  , cast(nullif([BbEquivGroup], '') as varchar(10)) collate Latin1_General_Bin
  , cast([BbFlxID] as varchar(11)) collate Latin1_General_Bin
  , isnull(cast([BbFlxIDBe] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbFlxIDCf] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbGroup] = '' then '|' else [BbGroup] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbInfo1] = '' then '|' else [BbInfo1] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbKind], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbMagic] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbNote] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbPrintDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbProperties] = '' then '|' else [BbProperties] end as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbRecType], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbSource] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbTax], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , case when [BbTier] = '' then '|' else [BbTier] end collate Latin1_General_Bin
  , cast(nullif([BbType], '') as varchar(10)) collate Latin1_General_Bin
  , isnull(cast(nullif([BbUserName], '') as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin);

-- Float fields contain imprecise data, compare they separately with fc_float utility.
SELECT (case when left(replace(ltrim(rtrim(replace(str([BbPerPayDivisor], 38, 15), '0',  ' '))), ' ', '0'), 1) = '.' then '0' else '' end) + replace(ltrim(rtrim(replace(str([BbPerPayDivisor], 38, 15), '0',  ' '))), ' ', '0') + (case when right(replace(ltrim(rtrim(replace(str([BbPerPayDivisor], 38, 15), '0',  ' '))), ' ', '0'), 1) = '.' then '0' else '' end) as BbPerPayDivisor
FROM [CRDN_SRC].[dbo].[BenBase]
ORDER BY replicate('0', 10-len(ROW_NUMBER() OVER (ORDER BY isnull(cast(case when [BbAccrualMethod] = '' then '|' else [BbAccrualMethod] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbAdvanced], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbArchive], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBeneficiaryFlag] = '' then '|' else [BbBeneficiaryFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBillMthd] = '' then '|' else [BbBillMthd] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbCRC] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateAdd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateDel], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateEnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateMod], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateRBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateREnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDepCovFlag] = '' then '|' else [BbDepCovFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDfltTier] = '' then '|' else [BbDfltTier] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , cast(nullif([BbElectionSet], '') as varchar(10)) collate Latin1_General_Bin
  , cast(nullif([BbEquivGroup], '') as varchar(10)) collate Latin1_General_Bin
  , cast([BbFlxID] as varchar(11)) collate Latin1_General_Bin
  , isnull(cast([BbFlxIDBe] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbFlxIDCf] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbGroup] = '' then '|' else [BbGroup] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbInfo1] = '' then '|' else [BbInfo1] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbKind], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbMagic] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbNote] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbPrintDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbProperties] = '' then '|' else [BbProperties] end as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbRecType], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbSource] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbTax], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , case when [BbTier] = '' then '|' else [BbTier] end collate Latin1_General_Bin
  , cast(nullif([BbType], '') as varchar(10)) collate Latin1_General_Bin
  , isnull(cast(nullif([BbUserName], '') as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin))) + cast(ROW_NUMBER() OVER (ORDER BY isnull(cast(case when [BbAccrualMethod] = '' then '|' else [BbAccrualMethod] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbAdvanced], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbArchive], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBeneficiaryFlag] = '' then '|' else [BbBeneficiaryFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbBillMthd] = '' then '|' else [BbBillMthd] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbCRC] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateAdd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateDel], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateEnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateMod], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateRBeg], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(convert(varchar(23), [BbDateREnd], 121), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDepCovFlag] = '' then '|' else [BbDepCovFlag] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbDfltTier] = '' then '|' else [BbDfltTier] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , cast(nullif([BbElectionSet], '') as varchar(10)) collate Latin1_General_Bin
  , cast(nullif([BbEquivGroup], '') as varchar(10)) collate Latin1_General_Bin
  , cast([BbFlxID] as varchar(11)) collate Latin1_General_Bin
  , isnull(cast([BbFlxIDBe] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbFlxIDCf] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbGroup] = '' then '|' else [BbGroup] end as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbInfo1] = '' then '|' else [BbInfo1] end as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbKind], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbMagic] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbNote] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbPrintDescrip], '') as varchar(30)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(case when [BbProperties] = '' then '|' else [BbProperties] end as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbRecType], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast([BbSource] as varchar(11)), '<*~NuLL*~>') collate Latin1_General_Bin
  , isnull(cast(nullif([BbTax], '') as varchar(10)), '<*~NuLL*~>') collate Latin1_General_Bin
  , case when [BbTier] = '' then '|' else [BbTier] end collate Latin1_General_Bin
  , cast(nullif([BbType], '') as varchar(10)) collate Latin1_General_Bin
  , isnull(cast(nullif([BbUserName], '') as varchar(20)), '<*~NuLL*~>') collate Latin1_General_Bin) as varchar(10));
```


```
ORACLE Tables: DWH.BENBASE

-- Table: DWH.BENBASE
/* FLOAT FIELDS (EXCLUDED): BBPERPAYDIVISOR */
/* IGNORED FIELDS: BBCODE, BBWIZARD, DW_CREATE_DTM, DW_PROCESS_WID, DW_SOURCE_WID */
SELECT nvl(BBACCRUALMETHOD, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBADVANCED, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBARCHIVE, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBBENEFICIARYFLAG, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBBILLMTHD, '<*~NuLL*~>')
  || '=~|*=' || nvl(rtrim(to_char(BBCRC, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEADD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEDEL, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEEND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEMOD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATERBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(to_char(BBDATEREND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>')
  || '=~|*=' || nvl(BBDEPCOVFLAG, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBDESCRIP, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBDFLTTIER, '<*~NuLL*~>')
  || '=~|*=' || BBELECTIONSET
  || '=~|*=' || BBEQUIVGROUP
  || '=~|*=' || rtrim(to_char(BBFLXID, 'FM9999999990.'), '.')
  || '=~|*=' || nvl(rtrim(to_char(BBFLXIDBE, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(rtrim(to_char(BBFLXIDCF, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(BBGROUP, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBINFO1, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBKIND, '<*~NuLL*~>')
  || '=~|*=' || nvl(rtrim(to_char(BBMAGIC, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(rtrim(to_char(BBNOTE, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(BBPRINTDESCRIP, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBPROPERTIES, '<*~NuLL*~>')
  || '=~|*=' || nvl(BBRECTYPE, '<*~NuLL*~>')
  || '=~|*=' || nvl(rtrim(to_char(BBSOURCE, 'FM9999999990.'), '.'), '<*~NuLL*~>')
  || '=~|*=' || nvl(BBTAX, '<*~NuLL*~>')
  || '=~|*=' || BBTIER
  || '=~|*=' || BBTYPE
  || '=~|*=' || nvl(BBUSERNAME, '<*~NuLL*~>') as TEXT_SIGNATURE
FROM DWH.BENBASE
ORDER BY ROW_NUMBER() OVER (ORDER BY nvl(BBACCRUALMETHOD, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBADVANCED, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBARCHIVE, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBBENEFICIARYFLAG, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBBILLMTHD, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBCRC, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEADD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEDEL, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEEND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEMOD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATERBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEREND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDEPCOVFLAG, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDESCRIP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDFLTTIER, '<*~NuLL*~>') NULLS FIRST
  , BBELECTIONSET NULLS FIRST
  , BBEQUIVGROUP NULLS FIRST
  , rtrim(to_char(BBFLXID, 'FM9999999990.'), '.') NULLS FIRST
  , nvl(rtrim(to_char(BBFLXIDBE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBFLXIDCF, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBGROUP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBINFO1, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBKIND, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBMAGIC, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBNOTE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBPRINTDESCRIP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBPROPERTIES, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBRECTYPE, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBSOURCE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBTAX, '<*~NuLL*~>') NULLS FIRST
  , BBTIER NULLS FIRST
  , BBTYPE NULLS FIRST
  , nvl(BBUSERNAME, '<*~NuLL*~>') NULLS FIRST);

-- Float fields contain imprecise data, compare they separately with fc_float utility.
SELECT rtrim(to_char(BBPERPAYDIVISOR, 'FM99999999999999999999999999999999999990.099999999999999999999999'), '.') as BBPERPAYDIVISOR
FROM DWH.BENBASE
ORDER BY to_char(ROW_NUMBER() OVER (ORDER BY nvl(BBACCRUALMETHOD, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBADVANCED, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBARCHIVE, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBBENEFICIARYFLAG, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBBILLMTHD, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBCRC, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEADD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEDEL, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEEND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEMOD, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATERBEG, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(to_char(BBDATEREND, 'YYYY-MM-DD HH24:MI:SS.FF3'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDEPCOVFLAG, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDESCRIP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBDFLTTIER, '<*~NuLL*~>') NULLS FIRST
  , BBELECTIONSET NULLS FIRST
  , BBEQUIVGROUP NULLS FIRST
  , rtrim(to_char(BBFLXID, 'FM9999999990.'), '.') NULLS FIRST
  , nvl(rtrim(to_char(BBFLXIDBE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBFLXIDCF, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBGROUP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBINFO1, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBKIND, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBMAGIC, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBNOTE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBPRINTDESCRIP, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBPROPERTIES, '<*~NuLL*~>') NULLS FIRST
  , nvl(BBRECTYPE, '<*~NuLL*~>') NULLS FIRST
  , nvl(rtrim(to_char(BBSOURCE, 'FM9999999990.'), '.'), '<*~NuLL*~>') NULLS FIRST
  , nvl(BBTAX, '<*~NuLL*~>') NULLS FIRST
  , BBTIER NULLS FIRST
  , BBTYPE NULLS FIRST
  , nvl(BBUSERNAME, '<*~NuLL*~>') NULLS FIRST), 'FM0000000000');
```