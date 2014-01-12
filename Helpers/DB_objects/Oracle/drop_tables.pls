-- Drop all tables in schema.
declare 
  c_perform_ddl constant boolean := False;    -- Perform DDL or just print it
  s varchar2(1000);
begin 
  for r in (select table_name name from user_tables where table_name!= 'DIM_DATE' order by 1) loop
    s := 'drop table ' || r.name || ' purge';
    dbms_output.put_line(s);
    if c_perform_ddl then
      execute immediate s;
    end if;
  end loop;
end;
/