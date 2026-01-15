import json

pred = json.load(open("output.json"))
gt = json.load(open("ground_truth.json"))

fields = [
 "product_line","origin_port_code","origin_port_name",
 "destination_port_code","destination_port_name",
 "incoterm","cargo_weight_kg","cargo_cbm","is_dangerous"
]

total = 0
correct = 0
per_field = {f:0 for f in fields}

for p,g in zip(pred,gt):
    for f in fields:
        total += 1
        pv = p.get(f)
        gv = g.get(f)
        if pv == gv:
            correct += 1
            per_field[f]+=1

print("Overall Accuracy:", round(correct/total*100,2),"%")
for f in fields:
    print(f,":", round(per_field[f]/len(gt)*100,2),"%")
