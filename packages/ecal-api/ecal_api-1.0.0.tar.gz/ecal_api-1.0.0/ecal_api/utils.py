# utils.py

import hashlib

def m5_signature(params):
    """
    Calculates the MD5 signature for the given parameters.

    Args:
        params (dict): The parameters to be signed.

    Returns:
        str: The MD5 signature.
    """
    concatenated_params = ''.join([str(params[key]) for key in sorted(params)])
    return hashlib.md5(concatenated_params.encode()).hexdigest()
