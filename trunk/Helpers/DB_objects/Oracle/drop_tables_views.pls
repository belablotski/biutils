-- Drop all tables/views in schema.
declare 
  c_perform_ddl constant boolean := False;              -- Perform DDL or just print it
  c_process_tables constant varchar2(5) := 'False';     -- Drop tables (True/False)
  c_process_views constant varchar2(5) := 'True';       -- Drop views (True/False)
  s varchar2(4000);
begin 
  for r in (select 'table' obj_type, table_name name from user_tables where c_process_tables = 'True' and table_name!= 'DIM_DATE' union all
            select 'view' obj_type, view_name name from user_views where c_process_views = 'True' and view_name!= 'DIM_DATE' 
            order by 1) 
  loop
    s := 'drop ' || r.obj_type || ' ' || r.name;
    dbms_output.put_line(s);
    if c_perform_ddl then
      execute immediate s;
    end if;
  end loop;
end;
/