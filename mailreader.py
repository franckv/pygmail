from mailbox import mbox
from email import utils
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-f", dest="filename")
    parser.add_option("-i", dest="idx")

    (options, args) = parser.parse_args()

    if options.filename == None:
	return

    mails = mbox(options.filename)

    print("#")
    for mail in mails:
	for header in mail.keys():
	    print(header + ": " + mail.get(header))
	print("")
	print(mail.preamble)
	print("")
	for part in mail.walk():
	    content_type = part.get_content_type()
	    print(content_type)
	    print(part.get_content_charset())
	    if content_type.startswith("text/"):
		decode=True
	    else:
		decode=False
	    print(part.get_payload(decode=decode))
	    print("")

	print(mail.defects)

main()
