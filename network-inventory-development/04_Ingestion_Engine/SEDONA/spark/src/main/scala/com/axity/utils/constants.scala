package com.axity.utils

object constants {

   val ctl_sid = "ctl_sid"
   val ctl_tid = "ctl_tid"
   val ctl_eid = "ctl_eid"
   val ctl_rid = "ctl_rid"
   val ctl_rfp = "ctl_rfp"
   val ctl_source_name = "ctl_source_name"
   val ctl_table_name = "ctl_table_name"
   val ctl_file_date = "ctl_file_date"
   val ctl_file_name = "ctl_file_name"
   val ctl_ts = "ctl_ts"
   val ctl_year = "ctl_year"
   val ctl_month = "ctl_month"
   val ctl_day = "ctl_day"
   val concat_column = "concat_column"
   val year_month =s"$ctl_year,$ctl_month"
   val year_month_day = s"$ctl_year,$ctl_month,$ctl_day"
   val full_str = "full"
   val total = "total"
   val hash_format = "MD5"
   val lst_audit_cols = List(ctl_sid,ctl_tid,ctl_eid,ctl_rid,ctl_rfp,ctl_source_name,concat_column,
      ctl_table_name,ctl_file_date,ctl_file_name,ctl_ts,ctl_year,ctl_month,ctl_day)

   val error_args = "not enough arguments"
   val error_full = "error not full"
   val read_count = "READ_COUNT"
   val insert_count = "INSERT_COUNT"
}
