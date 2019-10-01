
import os
import uhashlib
import ubinascii

class FirmwareHasher:
    def calculate():
        files = os.listdir()

        allFilesHash = "";
        hasher = uhashlib.md5(".")
        files.sort()
        for file in files:
            if file.endswith('.py'):
                f = open(file, 'r')
                contents = f.read()
                hasher.update(contents);
                f.close()

        return ubinascii.hexlify(hasher.digest())
