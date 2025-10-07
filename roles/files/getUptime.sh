uptime | sed 's/,//g' | tr -s ' ' | awk 'BEGIN{d=0;h=0;m=0}
          {
          for(i=1;i<=NF;i++){
              # Si el campo es únicamente dígitos y el siguiente campo es "day", "days" o "day(s)", se extrae el conteo de dias arriba
              if($i~/^[0-9]+$/ && i+1<=NF && $(i+1)~/^(day|days|day\(s\))$/){
              d=$i
              # Si los siguientes dos campos son HH:MM, luego lo divide en las variables
              if(i+2<=NF && $(i+2)~/^[0-9]+:[0-9]+$/){
                  split($(i+2), x, ":"); h=x[1]; m=x[2]
              }
                    # Si recién cumplió un nuevo día, tomar los minutos
              else if ( i+2 <= NF && $(i+2) ~ /^[0-9]+$/ && i+3 <= NF && ($(i+3) ~ /^(min|mins|min\(s\))$/) )
                  {
                  m = $(i+2)
              }
          
              }
              # Si el campo es "up" y el siguiente campo es HH:MM, extrae horas y minutos arriba
              else if($i=="up" && i+1<=NF && $(i+1)~/^[0-9]+:[0-9]+$/){
              split($(i+1), x, ":"); h=x[1]; m=x[2]
              }
              # Si el campo es "day", "days" o "day(s)" y el siguiente campo es HH:MM, extrae las horas y minutos arriba
              else if(($i=="day"||$i=="days"||$i=="day(s)") && i+1<=NF && $(i+1)~/^[0-9]+:[0-9]+$/){
              split($(i+1), x, ":"); h=x[1]; m=x[2]
              }
              # Manejar casos donde se haya reiniciado hace poco minutos
              else if ($i=="up" && i+1<=NF && $(i+1) ~ /^[0-9]+$/ && i+2<=NF && ($(i+2)=="min" || $(i+2)=="mins")) {
                m = $(i+1)          # Campo que contiene los valores de uptime en minutos.
              }
          }
          }
          END{
          printf "%d dias, %d horas, %d minutos\n", d, h, m
          }'