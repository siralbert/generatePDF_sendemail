# generatePDF_sendemail

This Python script generates a PDF and sends it out via E-mail.

The current use case for this script is to:

 - summarize and process sales data into different categories, 
 - generate a PDF using Python
 - and finally, send the PDF report by email to recipients automatically 

The script requires an SMTP mail server installed on the machine it runs on in order to send out an email.
Otherwise, a Connection Refused error will occur:
`ConnectionRefusedError: [Errno 111] Connection refused`

Also, note that if the email is sent to a public email address **it will most likely be considered spam and be blocked or dropped.**

To download the Python script and files, install the required libraries, and run the script(`cars.py`), 
copy and paste the following into your terminal.  The last line opens the PDF report with a firefox browser.

    git clone https://github.com/siralbert/generatePDF_sendemail.git
    cd generatePDF_sendemail
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./cars.py 
    firefox /tmp/cars.pdf  

