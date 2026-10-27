# Multi-Agent Web Search Assistant

A terminal app that answers questions using live web results. A search agent queries Serper.dev, a fetch agent downloads and cleans the pages, and an answer agent writes an answer that cites only the fetched text.

## Setup (Windows PowerShell)

```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env     # then put your keys into .env
python config.py           # checks that the keys are loaded
```

See `DECISIONS.md` for the design log.
