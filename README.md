# Doc Doctor

Streamlit tools for preparing academic career documents (CVs, etc.).

## Tools

| Tool | What it does |
|------|-------------|
| **Reverse Section Numbering** | Renumbers CV sections so the oldest entry is #1 (true chronological order) |
| **Add Section Prefixes** | Adds section codes to numbered entries (e.g. `RJA2.` for journal articles) |

## Running locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo.
3. Set **Main file path** to `Home.py`.
4. Deploy.

## File structure

```
doc-doctor/
├── Home.py                      # Landing page
├── pages/
│   ├── 1_Reverse_Numbering.py   # Streamlit app
│   └── 2_Add_Prefixes.py        # Streamlit app
├── core/
│   ├── docx_numbering.py        # Reverse-numbering logic
│   └── docx_prefixes.py         # Prefix logic + default mappings
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Notes

- Only `.docx` files are supported. Convert `.doc` files via Word or Google Docs first.
- For **Add Section Prefixes**, run **Reverse Section Numbering** on your file first.
- Files are processed in-memory and are never stored on the server.
