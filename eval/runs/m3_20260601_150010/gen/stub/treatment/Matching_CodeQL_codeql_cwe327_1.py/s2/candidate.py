import hashlib


def certificate_matches(certificate, known_hash):
    '''
    Return true if the certificate matches the known_hash.

    :param certificate: certificate
    :param known_hash: known hash
    :return: true if the certificate matches the known_hash
    '''
    if not certificate or not known_hash:
        return False

    # Convert certificate to bytes if necessary
    if isinstance(certificate, str):
        certificate = certificate.encode('utf-8')

    # Compute the hash of the certificate using SHA256
    computed_hash = hashlib.sha256(certificate).hexdigest()

    # Compare the computed hash with the known hash
    return computed_hash == known_hash
