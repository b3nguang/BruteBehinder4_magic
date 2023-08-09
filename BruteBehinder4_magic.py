import base64
import hashlib
import re

from Crypto.Cipher import AES


class AESCracker:
    def __init__(self, encrypted_data):
        self.encrypted_data = encrypted_data

    @staticmethod
    def decrypt(key, data):
        magic_num = int(key[:2], 16) % 16
        data = data[:len(data) - magic_num]

        cipher = AES.new(key, AES.MODE_ECB)
        decoded_bytes = base64.b64decode(data)
        return cipher.decrypt(decoded_bytes).decode('utf-8')

    def key_brute(self):
        with open(r"D:\CTF\Misc\Byxs20\CTF_Script\BruteForceAES\wordlists\Byxs20_top2w5.txt", 'rb') as f:
            plain = [i.strip() for i in f.readlines()]
        for key_candidate in plain:
            md5_enc = hashlib.md5(key_candidate).hexdigest()
            try:
                key = md5_enc[:16].encode()
                decrypted_data = self.decrypt(key, self.encrypted_data)
                cmd = re.findall(r'\$cmd="(.*?)"', decrypted_data)
                if cmd:
                    print('[*] Crack Success!!!' + '\n' + '[*] Key: ' + key_candidate.decode(
                        'utf-8') + '\n[*] Webshell Key: ' + md5_enc[:16])
                    payload = base64.b64decode(cmd[0]).decode('utf-8')
                    print('[*] Payload: ' + payload)
                break
            except Exception as e:
                print('[-] Crack Failed')

    def main(self, key=None):
        if key:
            try:
                decrypted_data = self.decrypt(key.encode(), self.encrypted_data)
                print('[*] Decrypted Data:\n' + decrypted_data)
            except Exception as e:
                print('[-] Decryption Failed')
        else:
            self.key_brute()


if __name__ == '__main__':
    encrypted_data = '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····A······'
    aes_cracker = AESCracker(encrypted_data)
    aes_cracker.main('fb59891768280222')  # Provide the key here
