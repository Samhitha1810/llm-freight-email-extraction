import json, time, os
from groq import Groq
from schemas import ShipmentExtraction
from prompts import PROMPT_V3
from port_loader import load_ports, normalize_port
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"

load_dotenv(".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("GROQ_API_KEY loaded =", os.getenv("GROQ_API_KEY"))


name_to_code, code_to_name = load_ports()


def call_llm(prompt):
    for attempt in range(3):
        try:
            res = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return res.choices[0].message.content
        except Exception:
            time.sleep(2 ** attempt)
    return None


def post_process(email_id, raw_json):
    try:
        data = json.loads(raw_json)
    except:
        data = {}

    o_code, o_name = normalize_port(data.get("origin_port"), name_to_code, code_to_name)
    d_code, d_name = normalize_port(data.get("destination_port"), name_to_code, code_to_name)

    incoterm = data.get("incoterm") or "FOB"
    incoterm = incoterm.upper()

    # product line rule
    product_line = None
    if d_code and d_code.startswith("IN"):
        product_line = "pl_sea_import_lcl"
    elif o_code and o_code.startswith("IN"):
        product_line = "pl_sea_export_lcl"

    # numeric rounding
    weight = data.get("cargo_weight_kg")
    cbm = data.get("cargo_cbm")

    if isinstance(weight, (int, float)):
        weight = round(weight, 2)
    else:
        weight = None

    if isinstance(cbm, (int, float)):
        cbm = round(cbm, 2)
    else:
        cbm = None

    is_dangerous = bool(data.get("is_dangerous", False))

    return ShipmentExtraction(
        id=email_id,
        product_line=product_line,
        origin_port_code=o_code,
        origin_port_name=o_name,
        destination_port_code=d_code,
        destination_port_name=d_name,
        incoterm=incoterm,
        cargo_weight_kg=weight,
        cargo_cbm=cbm,
        is_dangerous=is_dangerous
    )


def process_email(email):
    prompt = PROMPT_V3.format(subject=email["subject"], body=email["body"])
    raw = call_llm(prompt)

    if raw is None:
        return ShipmentExtraction(
            id=email["id"],
            product_line=None,
            origin_port_code=None,
            origin_port_name=None,
            destination_port_code=None,
            destination_port_name=None,
            incoterm=None,
            cargo_weight_kg=None,
            cargo_cbm=None,
            is_dangerous=False
        )

    return post_process(email["id"], raw)


def main():
    emails = json.load(open("emails_input.json", encoding="utf-8"))
    results = []

    for e in emails:
        result = process_email(e)
        results.append(result.model_dump())

    json.dump(results, open("output.json", "w", encoding="utf-8"), indent=2)
    print("Extraction complete. Saved output.json")


if __name__ == "__main__":
    main()
