REM MS SQL Server
REM TODO: Strings are right-padded with spaces (remove or add in Oracle too)
sqlcmd -S serv_host -U ABELABLOTSKI -P xxx -i unload_ms.sql -o res_ms.txt -h-1

REM ORACLE
sqlplus ABELABLOTSKI/xxx@serv_host:1521/orcl @unload_ora.sql