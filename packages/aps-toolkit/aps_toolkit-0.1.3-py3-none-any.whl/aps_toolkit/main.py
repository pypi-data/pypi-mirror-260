from Token import Token
from Auth import Auth
from ProDbReaderRevit import PropDbReaderRevit

auth = Auth()
token = auth.auth2leg()
urn = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLk9kOHR4RGJLU1NlbFRvVmcxb2MxVkE_dmVyc2lvbj0yNA"
prop_reader = PropDbReaderRevit(urn, token)
data = prop_reader.get_data_by_category("Windows")
print(data.head())