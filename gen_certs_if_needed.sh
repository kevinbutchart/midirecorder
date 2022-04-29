set -x
openssl req -new -newkey rsa:4096 -sha256 -days 3650 -nodes -x509 -subj "/C=US/ST=Oklahoma/L=Stillwater/O=My Company/OU=Engineering/CN=test.com" -keyout ca.key -out ca.crt
openssl genrsa -out "pianorecorder.key" 4096
openssl req -new -key pianorecorder.key -out pianorecorder.csr -config openssl.cnf
openssl x509 -req -sha256 -days 3650 -in pianorecorder.csr -CA rootCA.pem -CAkey rootCA-key.pem -CAcreateserial -extensions v3_req -extfile openssl.cnf -out pianorecorder.pem
openssl x509 -inform PEM -outform DER -in pianorecorder.pem -out pianorecorder.crt
#openssl pkcs12 -export -in pianorecorder.pem -inkey pianorecorder.key -out pianorecorder.p12
