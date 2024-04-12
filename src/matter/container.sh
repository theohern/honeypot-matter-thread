
echo "Time, CPU, RAM, Mem" > /usr/share/grafana/csv/matter-stat.csv
while true; do
  date "+%Y-%m-%d %H:%M:%S" | tr '\n' ',' > line ; docker stats addon_core_matter_server --no-stream | awk 'NR==2 { print $3 "," $4 "," $7 }' >> line
  cat line | sed 's/%//g; s/MiB//g' >> /usr/share/grafana/csv/matter-stat.csv
  sleep 1
done
