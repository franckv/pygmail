from mailbox import mbox
from email.generator import Generator
from optparse import OptionParser
import os.path

parser = OptionParser()
parser.add_option("-f", dest="filename")

(options, args) = parser.parse_args()

if options.filename == None:
    exit()

mails = mbox(options.filename)

for mail in mails:
    outfilename = mail.get('X-UIDL')
    if outfilename == None:
        continue
    if os.path.exists(outfilename):
        continue
    outfile = open(outfilename, 'w')
    g = Generator(outfile, mangle_from_=False, maxheaderlen=60)
    g.flatten(mail, True)
    outfile.close()

