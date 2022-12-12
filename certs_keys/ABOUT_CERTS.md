# CA - Certificate Authority
It's an organization that uses digital certificates to validates identities of entities and bind them with cryptographic key.

To gain this digital certificate, applicant has to generate **Certificate Signing Request (CSR)** containing his public key and identyfing information.  
Then the CA validates it and if everything's okay, generates the certificate and sends it to applicant. 

## **Chain of trust**
It helps provide security and standards compliance. It's divided into 3 parts:
1) **Trust anchor** - it's just the CA that gives out the certificates
2) **Intermediary certificate** - this is isolation of trust anchor for safety measures. All administrative things happens by using these certificates.
3) **End-entity certificate** - this is the certificate that I was talking about earlier and  in fact confirms identity.

You can generate self-signed certificate for testing purpose on IP address 127.0.1.1, by using this cheet sheet:  
https://github.com/ChristianLempa/cheat-sheets/blob/main/misc/ssl-certs.md

Notice that:
1) Common name should be `127.0.1.1`,
2) You has to specify `"SubjectAltName=IP:127.0.1.1"`