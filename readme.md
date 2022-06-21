# WhatsappExportParser
parses structured whatsapp chat exports that are used to document working hours and returns data monthwise in CSV.

# Data/channel structure
following keywords need to be used:

| keyword | purpose|
----------|-----------
| kommen | start of work/ check in |
| gehen | end of work / check out |
| pause | start of break |
| ende | end of break |

if you missed to check in, you can give the correct time with the according keyword in this format: "kommen 8:45". 
Otherwise the Timestamp of the Message is used for the documentation.
This Version includes only one possible break during the shift.
