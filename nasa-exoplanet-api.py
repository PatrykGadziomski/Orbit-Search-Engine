import requests
import pandas as pd
from io import StringIO


url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

query = """
SELECT pl_name, hostname, pl_rade, pl_bmasse, pl_orbper, st_teff
FROM pscomppars
WHERE pl_rade IS NOT NULL
"""

params = {
    "query": query,
    "format": "csv"
}

response = requests.get(url, params=params)

# In DataFrame umwandeln
df = pd.read_csv(StringIO(response.text))

print(df)