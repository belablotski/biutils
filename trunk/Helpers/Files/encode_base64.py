import base64

with open(r"C:\Users\Aliaksei_Belablotski\demo.png", "rb") as src_file:
    encoded_string = base64.b64encode(src_file.read())
    print encoded_string
    print "<img src=\"data:image/gif;base64,%s\" alt=\"demonstation\" width=\"%d\" height=\"%d\" />" % (encoded_string, 100, 100)