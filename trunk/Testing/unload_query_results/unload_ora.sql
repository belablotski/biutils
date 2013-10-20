set feedback off
set term off
set linesize 4000
--set colsep ,
--set colsep '","'
set trimspool on
set underline off
set heading off
--set headsep $
set newpage none


spool "res_ora.txt"

SELECT ...

spool off