-- Calculate row counts for user's tables.

variable h_rc refcursor;

declare
  l_sql varchar2(4000) := null;
  l_tab_name varchar2(30);
begin
  for rec in (select * from user_tables) loop
    l_tab_name := rec.table_name;
    if l_sql is not null then
      l_sql := l_sql || ' union all ';
    end if;
    l_sql := l_sql || 'select ''' || l_tab_name || ''' as tbl_name, count(1) as row_cnt from ' || l_tab_name;
  end loop;
  dbms_output.put_line(l_sql);
  open :h_rc for l_sql;
end;
/

print h_rc
