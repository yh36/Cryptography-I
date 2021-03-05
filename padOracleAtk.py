"""
1. Run from the end first to figure out the number of padding bytes
2. Modify code to skip the padding bytes; otherwise, the first padding byte has
   no error return which breaks the logic
"""
#import urllib2
import urllib.request
import urllib.error
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def __init__(self, q):
        self.q = bytearray.fromhex(q)

    def _query(self, q):
        target = TARGET + urllib.request.quote(q)    # Create query URL
        req = urllib.request.Request(target)         # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)          # Wait for response
        #except urllib2.HTTPError, e:
        except urllib.error.HTTPError as e:
            #print("We got: %d" % e.code)      # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

    def decrypt(self):
        res = [0] * (len(self.q)-16)
        #print(self.q.hex())
        for i in range(len(self.q)-1, 15, -1):
            if i % 16 == 15:
                cipherMsg = self.q[:i+1]
            if i > 54:
                # Skip the padding part. One interesting case is when we guess
                # the first padding byte. It won't return the error as it is
                # a legal request.
                res[i-16] = 9
                continue
            pad = 16 - (i % 16)
            #print(pad)
            # XOR all guessed characters with the correct padding number
            print(f'\n###{i}-{pad}###')
            for di in range(1, pad):
                #print(i-16+di, self.q[i-16+di], res[i-16+di], pad)
                cipherMsg[i-16+di] = self.q[i-16+di]^res[i-16+di]^pad
            cI = cipherMsg[i-16]
            #print(self.q[13])
            #print(cipherMsg[:48].hex())
            for g in range(256):
                cipherMsg[i-16] = cI^g^pad
                if self._query(cipherMsg.hex()):
                    #print(g)
                    res[i-16] = g
                    break
            #assert False
        return res

if __name__ == "__main__":
    #a = [84, 104, 101, 32, 77, 97, 103, 105, 99, 32, 87, 111, 114, 100, 115, 32]
    #print(''.join([chr(_) for _ in a]))
    #assert False
    po = PaddingOracle(sys.argv[1])
    res = po.decrypt()       # Issue HTTP query with the given argument
    print(res)
    print(''.join([chr(_) for _ in res]))