from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import json
import uvicorn
from wellix_backend_fastapi import check_drug_interaction

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load drug interactions from list.json file
with open("list.json", "r") as file:
  drug_interactions = json.load(file)


# # Function to check drug interactions
# def check_drug_interaction(drug1, drug2):
#   for interaction in drug_interactions:
#     drugs = [drug.lower() for drug in interaction["interaction"]]
#     if (drugs[0] == drug1.lower() and drugs[1] == drug2.lower()) or (
#             drugs[0] == drug2.lower() and drugs[1] == drug1.lower()):
#       return interaction
#   return None


# Request body model
class DrugRequest(BaseModel):
  drugs: List[str]


# Route to check drug interactions
@app.post("/check-interactions")
async def check_interactions(drug_request: DrugRequest):
  interactions = []
  drugs = drug_request.drugs
  for i in range(len(drugs)):
    for j in range(i + 1, len(drugs)):
      drug1 = drugs[i]
      drug2 = drugs[j]
      interaction = check_drug_interaction(
          drug1, drug2, drug_interactions)
      if interaction:
        interactions.append({
            "between":
            f"Interaction found between {drugs[i]} and {drugs[j]}",
            "mechanism": interaction["mechanism"],
            "desc": interaction["description"],
        })
  print(interactions)
  return {"interactions": interactions}

# Run server
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
