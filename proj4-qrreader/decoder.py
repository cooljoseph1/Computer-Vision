"""
This file was written to help decode a QR code.  It utilizes the zxing.org API to do the trick. 
The zxing.org API returns an HTML page with a table in it to display results.
In order to parse this table and extract the message, the library beautifulsoup was used.
You will need to install this via the command: conda install beautifulsoup4.
"""
from bs4 import BeautifulSoup
import json
import os
import requests
import matplotlib.pyplot as plt


def decode(arr):
    """
    Function: decode
    ----------------
    decodes a numpy arrayified QR code

    Parameters:
    -----------
    arr: the numpy array

    Returns:
    --------
    the parsed message
    """
    plt.imsave('tmp.png', arr)
    with open("tmp.png", "rb") as f:
        response = requests.post('https://zxing.org/w/decode', files=dict(f=f), timeout=1)
    
    os.remove("tmp.png")
    html = response.text
    table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(html, 'html.parser')("tr")]
    with open("output.txt", 'w') as f:
        f.write("\n".join(" ".join(row) for row in table_data))
    obj = dict(table_data)
    return obj['Parsed Result']
