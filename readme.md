Struktura:

    `main.py`: zažene aplikacijo.

    `api/`: si API endpointi

    `core/`: jedrno logika

    `models/`: Definicije Pydantic modelov

    `data/`: Mapa, kamor vržeš svoje dokumente za učenje.

---

Zagon:


1. Kaj rabiš:

    Python 3.9+

    OpenAI API ključ

2. Namestitev:

Najprej v `kms-rag-service` naredi virtualno okolje:
```bash

python -m venv venv
source venv/bin/activate  # na windows je `venv\Scripts\activate`


pip install -r requirements.txt
```

3. Nastavitve (.env):

V tej naredi `.env` datoteko in notri prilepi svoj OpenAI ključ

.env
```env


OPENAI_API_KEY="sk-..."

OSTALO LAHKO PUSTIŠ, ČE TI JE VŠEČ PRIVZETO

OPENAI_MODEL_NAME="gpt-4o"

```

4. Zagon 

POMEMBNO: Ker ta servis sodeluje s `kms-db-service`, ga moraš zagnati iz mape, kjer sta obe mapi.

```bash
uvicorn kms_rag_service.main:app --reload
```
Strežnik bo runnal na `http://127.0.0.1:8000`.

API:

Ko zaženeš, lahko greš na `http://127.0.0.1:8000/docs` in tam vidiš vse lepo interaktivno opisano (thx to FastAPI).

    `POST /api/v1/query/non-stream`: Pošlješ vprašanje, returna JSON odgovor naenkrat.

    `POST /api/v1/query/stream`: Za streamanje (frontend)

    `GET /api/v1/health`: preveriš, če servis dela.

Ce zelis dodat file, samo daj v mapo data. 
