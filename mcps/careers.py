import json
from pathlib import Path
class CareerMCP:
    def fetch_all_jobs(self):
        c=json.loads((Path(__file__).parent.parent/'data'/'companies.json').read_text())
        return [{'company':x['company'],'role':'Java Intern','location':'Remote'} for x in c]
