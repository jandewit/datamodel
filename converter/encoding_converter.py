import os
import codecs

class EncodingConverter:

    @staticmethod
    def convert(input_filename):
        # First check if it is not already UTF-8
		
        try:
            f = codecs.open(input_filename, encoding='utf-8', errors='strict')
            for line in f:
                pass
            print "Valid utf-8"
		
        except UnicodeDecodeError:
            f.close()
            print "invalid utf-8"

            #sourceEncoding = "iso-8859-1"
            sourceEncoding = "windows-1252"
            targetEncoding = "utf-8"
            source = open(input_filename, "rb")
            target = open(input_filename + '_utf8', "wb")

            target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))

            source.close()
            target.close()

            os.remove(input_filename)
            os.rename(input_filename + '_utf8', input_filename)