set -ex
CERTS_DIR="/app/certificate"

function createcerts()
{
  mkdir -p /data/ca/certsdb
  touch /data/ca/index.txt
  openssl req -new -newkey rsa:4096 -config certificate/ca.cnf -keyout /data/ca.key -out /data/careq.pem
  openssl ca -create_serial -batch -out /data/ca.pem -days 397 -keyfile /data/ca.key -selfsign -extensions v3_req_ca -config certificate/ca.cnf -infiles /data/careq.pem
  openssl genrsa -out "/data/pianorecorder.key" 4096
  openssl req -new -key /data/pianorecorder.key -out /data/pianorecorder.csr -config certificate/openssl.cnf
  openssl x509 -req -sha256 -days 365 -in /data/pianorecorder.csr -CA /data/ca.pem -CAkey /data/ca.key -CAcreateserial -extensions v3_req -extfile certificate/openssl.cnf -out /data/pianorecorder.pem
  openssl x509 -inform PEM -outform DER -in /data/ca.pem -out /data/ca.crt
}

[[ -f "/data/pianorecorder.pem" && -f "/data/pianorecorder.key" && -f "/data/ca.crt" ]] || {
  createcerts
}
ln -sf /data/ca.crt static/ca.crt
#openssl pkcs12 -export -in pianorecorder.pem -inkey pianorecorder.key -out pianorecorder.p12
