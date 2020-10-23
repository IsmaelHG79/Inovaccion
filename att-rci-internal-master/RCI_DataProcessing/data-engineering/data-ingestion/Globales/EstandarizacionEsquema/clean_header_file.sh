
#!/bin/bash
 
`cat $1 | awk 'BEGIN {FS = "|"};NR==1  {for (i=1;i<=NF;i++) {if(gsub(/[^[:alnum:]]/, "", $i)) print salida="\x22prefix_"i"_"$i"\x22|"}}' | awk '{gsub(/[^\0-\177]/,"");print}' | awk 'NR{printf "%s",$0;next;}1' | awk '{print $1 "\r"}' | awk '{print substr($0, 1, length($0)-2)}'> $101.psv`

`cat $1 | awk '{if (NR!=1) {print}}' > $102.psv`

`cat $101.psv $102.psv > $1.psv`

`rm $101.psv $102.psv`
