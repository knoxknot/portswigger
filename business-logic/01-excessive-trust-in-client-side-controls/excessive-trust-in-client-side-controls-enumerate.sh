base_url="https://0a1f00410450ba6680aa8a200085007a.web-security-academy.net"
paths=$(curl -s "$base_url" | grep -oE '(src|href)="[^"]*"' | cut -d'"' -f2)
for path in $paths; do
  echo "$(curl -sk -x 127.0.0.1:8080 -o /dev/null "${base_url}${path}")"
done