import hashlib
import hmac


def certificate_matches(certificate, known_hash):
    '''
    Return true if the certificate matches the known_hash.

    :param certificate: certificate
    :param known_hash: known hash
    :return: true if the certificate matches the known_hash
    '''
    if isinstance(certificate, str):
        certificate = certificate.encode('utf-8')

    certificate_hash = hashlib.sha256(certificate).hexdigest()

    return hmac.compare_digest(certificate_hash, known_hash)
