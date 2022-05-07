set -ex
CERTS_DIR="/app/certificate"
DEST_DIR="/data"

function createcerts()
{
  mkdir -p "$DEST_DIR"/ca/certsdb
  touch "$DEST_DIR"/ca/index.txt
  openssl req -new -newkey rsa:4096 -config certificate/ca.cnf -keyout "$DEST_DIR"/ca.key -out $DEST_DIR/careq.pem
  openssl ca -create_serial -batch -out "$DEST_DIR"/ca.pem -days 397 -keyfile $DEST_DIR/ca.key -selfsign -extensions v3_req -config certificate/ca.cnf -infiles $DEST_DIR/careq.pem
  openssl genrsa -out ""$DEST_DIR"/pianorecorder.key" 4096
  openssl req -new -key "$DEST_DIR"/pianorecorder.key -out $DEST_DIR/pianorecorder.csr -config certificate/openssl.cnf
  openssl x509 -req -sha256 -days 365 -in "$DEST_DIR"/pianorecorder.csr -CA $DEST_DIR/ca.pem -CAkey $DEST_DIR/ca.key -CAcreateserial -extensions v3_req -extfile certificate/openssl.cnf -out $DEST_DIR/pianorecorder.pem
  openssl x509 -inform PEM -outform DER -in "$DEST_DIR"/ca.pem -out $DEST_DIR/ca.crt
}

[[ -f ""$DEST_DIR"/pianorecorder.pem" && -f "$DEST_DIR/pianorecorder.key" && -f "$DEST_DIR/ca.crt" ]] || {
  createcerts
}
ln -sf "$DEST_DIR"/ca.crt static/ca.crt
#openssl pkcs12 -export -in pianorecorder.pem -inkey pianorecorder.key -out pianorecorder.p12
