from Crypto.Cipher import AES


def cbcDecrypt(key, ctxt):
    blksz = len(key)
    # Extract the IV
    iv = ctxt[:blksz]
    aesObj = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt chain for the rest of ciphertext
    ciphertext = ctxt[blksz:]
    ptxt = aesObj.decrypt(ciphertext)
    return ptxt
    """
    offset, ptxt = 0, ''
    while offset < len(txt):
        blk = txt[offset:(offset+blksz)]
        offset += blksz
        dblk = 
    """


if __name__ == '__main__':
    cbcKey1 = '140b41b22a29beb4061bda66b6747e14'
    ciphertext1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'

    print(cbcDecrypt(cbcKey1, ciphertext1))

