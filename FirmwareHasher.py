
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
        firmware = os.uname()
        return os.uname().release + "." +ubinascii.hexlify(hasher.digest()).decode()[1:8]
