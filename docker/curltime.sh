#!/usr/bin/bash

# Credit: Simon East (https://stackoverflow.com/a/22625150)
# CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/

curl -w @- -o /dev/null -s "$@" <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
   time_pretransfer:  %{time_pretransfer}\n
      time_redirect:  %{time_redirect}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
