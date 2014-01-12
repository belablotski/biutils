-- Convert views to tables (first two letters will be changed to XX).
declare 
  c_perform_ddl constant boolean := False;    -- Perform DDL or just print it
  s varchar2(1000);
begin 
  for r in (select view_name name from user_views order by 1) loop
    s := 'create table XX' || substr(r.name, 3) || ' as select * from ' || r.name;
    dbms_output.put_line(s);
    if c_perform_ddl then
      execute immediate s;
    end if;
  end loop;
end;
/


-- Drop views and Rename tables started with XX... to HR...
declare 
  c_perform_ddl constant boolean := False;    -- Perform DDL or just print it
  s varchar2(1000);
begin 
  for r in (select view_name name from user_views order by 1) loop
    s := 'drop view ' || r.name;
    dbms_output.put_line(s);
    if c_perform_ddl then
      execute immediate s;
    end if;
  end loop;

  for r in (select table_name name from user_tables order by 1) loop
    s := 'rename ' || r.name || ' to ' || 'HR' || substr(r.name, 3);
    dbms_output.put_line(s);
    if c_perform_ddl then
      execute immediate s;
    end if;
  end loop;
end;
/
