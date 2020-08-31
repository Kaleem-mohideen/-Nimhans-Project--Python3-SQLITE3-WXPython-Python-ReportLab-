rm nimhans.db; sqlite3 --echo nimhans.db < schema.sql 2> errSchema.txt; sqlite3 --echo nimhans.db < data.sql 2> errData.txt;
