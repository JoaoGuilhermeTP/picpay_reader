import PyPDF2, re, pandas as pd

# set file path
filePath = "path_to_pdf_file"

# create a pdf file object
with open(filePath, 'rb') as pdfFileObj:
    # create a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    # create list which will contain the transactions as dictionaries
    transactions = []
    # create boolean variable to help keeping track of when transactions are found
    marker = False
    # iterate through pdf pages
    for page in pdfReader.pages:
        # get the text from page
        pageText = page.extract_text()
        # split text in lines (in the form of a list, where each item in the list is a line)
        pageText = pageText.split("\n")
        # iterate over lines in text
        for line in pageText:
            # identify lines that start with a date
            if re.match("\d*/\d*/\d*", line):
                # when found, set marker to True, create a new empty transactions as a dictionary and store date in a variable
                marker = True
                transaction = {}
                date = line
                # skip this line and continue for loop
                continue
            # identify lines that start with a time when marker is still True
            if re.match("\d*:\d*:\d*", line) and marker:
                # store date info into transaction
                transaction["date"] = date
                # store match object for time in string in a variable
                timeMatch = re.search("\d*:\d*:\d*", line)
                # get time info from match object
                time = timeMatch.group()
                # store time into transaction
                transaction["time"] = time
                # remove time from line
                line = line[timeMatch.end():]
                # modify money info pattern in line
                line = line.replace("- R$ ", "R$-").replace("R$ -", "R$-").replace("R$ ", "R$")
                # search for money info
                values = re.search("R\$.*", line)
                # get transaction description by slicing line up until money info and store in transaction
                description = line[:values.start()]
                transaction["description"] = description
                # split values string by white spaces
                values = values.group().split()
                # store money information into transaction
                transaction["value"] = values[0]
                transaction["balance"] = values[1]
                transaction["avaliable"] = values[2]
                # add this transaction to the list of transactions
                transactions.append(transaction)
            else:
                marker = False

# create pandas dataframe
df = pd.DataFrame(transactions)

# generate xlsx file from dataframe
df.to_excel("picpay.xlsx")