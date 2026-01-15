# Prompt Version 1
PROMPT_V1 = """
You are an expert freight forwarding email information extraction system.

Extract the following fields and return ONLY valid JSON:

origin_port: string or null
destination_port: string or null
incoterm: string or null
cargo_weight_kg: number or null
cargo_cbm: number or null
is_dangerous: true or false

Rules:
- All shipments are sea freight LCL
- If incoterm missing → default FOB
- If incoterm ambiguous → default FOB
- Dangerous goods if contains DG, dangerous, hazardous, IMO, IMDG, or 'Class <number>'
- If negation like non-DG, non-hazardous, not dangerous → is_dangerous = false
- If multiple shipments → extract first shipment in BODY
- Subject/body conflict → BODY wins
- If value missing or 'TBD','N/A','to be confirmed' → null
- Weight in lbs → convert to kg (lbs * 0.453592)
- Weight in tonnes/MT → convert to kg (×1000)
- Round weight and cbm to 2 decimals
- Return ONLY JSON

Email Subject:
{subject}

Email Body:
{body}
"""


# Prompt Version 2 (improved port clarity)
PROMPT_V2 = PROMPT_V1 + """
Additional Rules:
- origin_port and destination_port must be port city names only.
- Do not return country names.
- Do not return intermediate/transshipment ports.
"""


# Prompt Version 3 (final – best accuracy)
PROMPT_V3 = PROMPT_V2 + """
Examples:

Email: "Rate request from Hong Kong to Chennai 5 CBM FOB"
Return:
{{"origin_port":"Hong Kong","destination_port":"Chennai","incoterm":"FOB","cargo_weight_kg":null,"cargo_cbm":5.0,"is_dangerous":false}}

Remember:
Return ONLY JSON. No explanation.
"""
