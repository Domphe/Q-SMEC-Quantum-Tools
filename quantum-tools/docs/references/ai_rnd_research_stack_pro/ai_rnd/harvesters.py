import requests, datetime
from .db import get_conn
from .config import TIMEOUT, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}

def _ensure_program(conn, name, sponsor, iso_code, url):
    cur = conn.cursor()
    cur.execute("SELECT country_id FROM country WHERE iso_code=?", (iso_code,))
    c = cur.fetchone()
    if not c:
        cur.execute("INSERT INTO country(iso_code,name) VALUES(?,?)", (iso_code, iso_code))
        country_id = cur.lastrowid
    else:
        country_id = c[0]
    cur.execute("SELECT program_id FROM funding_program WHERE name=?", (name,))
    p = cur.fetchone()
    if p:
        return p[0]
    cur.execute("INSERT INTO funding_program(name,sponsor,country_id,url,notes) VALUES(?,?,?,?,?)",
                (name, sponsor, country_id, url, "auto-harvested"))
    conn.commit()
    return cur.lastrowid

def harvest_cordis(query:str, date_from:str=None, date_to:str=None, max_records:int=50):
    conn = get_conn()
    program_id = _ensure_program(conn,
        name="Horizon Europe / CORDIS",
        sponsor="European Commission",
        iso_code="EU",
        url="https://cordis.europa.eu/"
    )
    base_url = "https://cordis.europa.eu/search?q=" + requests.utils.quote(query)
    cur = conn.cursor()
    title = f"CORDIS search: {query}"
    cur.execute("""INSERT INTO grant_call(program_id, call_code, title, open_date, close_date, trl_min, trl_max, budget_eur, url, notes)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (program_id, None, title, date_from, date_to, None, None, None, base_url,
                 "Stub record created by harvester; replace with API-parsed fields in deployment."))
    conn.commit()
    return {"inserted": 1, "program_id": program_id, "note": "Use official CORDIS APIs for full metadata."}

def harvest_grants_gov(keyword:str, date_from:str=None, date_to:str=None, max_records:int=50):
    conn = get_conn()
    program_id = _ensure_program(conn,
        name="Grants.gov",
        sponsor="US Government",
        iso_code="US",
        url="https://www.grants.gov/"
    )
    params = []
    if keyword: params.append(f"keywords={requests.utils.quote(keyword)}")
    if date_from: params.append(f"startDate={date_from}")
    if date_to: params.append(f"endDate={date_to}")
    param_str = "&".join(params)
    search_url = "https://www.grants.gov/grantsws/rest/opportunities/search" + ("?" + param_str if param_str else "")
    cur = conn.cursor()
    title = f"Grants.gov search: {keyword}"
    cur.execute("""INSERT INTO grant_call(program_id, call_code, title, open_date, close_date, trl_min, trl_max, budget_eur, url, notes)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (program_id, None, title, date_from, date_to, None, None, None, search_url,
                 "Stub record created by harvester; replace with API-parsed fields in deployment."))
    conn.commit()
    return {"inserted": 1, "program_id": program_id, "note": "Use Grants.gov opportunities API for full metadata."}
