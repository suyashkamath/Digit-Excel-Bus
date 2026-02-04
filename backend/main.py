# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import pandas as pd
# import io
# import base64
# from typing import Optional

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------- FORMULA DATA -------------------
# FORMULA_DATA = [
#     {"LOB": "TW", "SEGMENT": "1+5", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "PO": "90% of Payin", "REMARKS": "NIL"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 20%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 30%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 40%"},
#     {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
#     {"LOB": "BUS", "SEGMENT": "STAFF BUS", "PO": "88% of Payin", "REMARKS": "NIL"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
#     {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-5%", "REMARKS": "Payin Above 50%"},
#     {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "PO": "88% of Payin", "REMARKS": "NIL"}
# ]

# # ------------------- STATE MAPPING -------------------
# STATE_MAPPING = {
#     "DELHI": "DELHI", "MUMBAI": "MAHARASHTRA", "PUNE": "MAHARASHTRA", "GOA": "GOA",
#     "KOLKATA": "WEST BENGAL", "HYDERABAD": "TELANGANA", "AHMEDABAD": "GUJARAT",
#     "TAMIL NADU": "TAMIL NADU", "TN": "TAMIL NADU", "CHENNAI": "TAMIL NADU",
#     "KERALA": "KERALA", "KARNATAKA": "KARNATAKA", "BANGALORE": "KARNATAKA",
#     "GUJARAT": "GUJARAT", "RAJASTHAN": "RAJASTHAN", "PUNJAB": "PUNJAB",
#     "UTTAR PRADESH": "UTTAR PRADESH", "DELHI NCR": "DELHI", "REST OF INDIA": "REST OF INDIA",
#     "GOOD GJ": "GUJARAT", "BAD GJ": "GUJARAT", "ROM1": "REST OF MAHARASHTRA",
#     "ROM2": "REST OF MAHARASHTRA", "GOOD TN": "TAMIL NADU", "GOOD MP": "MADHYA PRADESH"
# }

# # ------------------- PAYOUT LOGIC -------------------
# def get_payin_category(payin: float):
#     if payin <= 20: return "Payin Below 20%"
#     elif payin <= 30: return "Payin 21% to 30%"
#     elif payin <= 50: return "Payin 31% to 50%"
#     else: return "Payin Above 50%"

# def safe_float(value):
#     if pd.isna(value): return None
#     val_str = str(value).strip().upper()
#     if val_str in ["D", "NA", "", "NAN", "NONE", "DECLINE"]: return None
#     try:
#         num = float(val_str.replace('%', '').replace('X', '').strip())
#         return num * 100 if 0 < num < 1 else num
#     except: return None

# def get_formula_from_data(lob: str, segment: str, policy_type: str, payin: float):
#     segment_key = segment.upper()
#     if lob == "TW":
#         segment_key = "TW TP" if policy_type == "TP" else "TW SAOD + COMP"
#     elif lob == "PVT CAR":
#         segment_key = "PVT CAR TP" if policy_type == "TP" else "PVT CAR COMP + SAOD"
#     elif lob in ["TAXI", "CV", "BUS", "MISD"]:
#         segment_key = segment.upper()

#     payin_category = get_payin_category(payin)
#     matching_rule = None
#     for rule in FORMULA_DATA:
#         if rule["LOB"] == lob and rule["SEGMENT"] == segment_key:
#             if rule["REMARKS"] == payin_category or rule["REMARKS"] == "NIL":
#                 matching_rule = rule
#                 break

#     if not matching_rule and payin > 20:
#         for rule in FORMULA_DATA:
#             if rule["LOB"] == lob and rule["SEGMENT"] == segment_key:
#                 if (rule["REMARKS"] == "Payin Above 20%" or
#                     (payin > 30 and rule["REMARKS"] == "Payin Above 30%") or
#                     (payin > 40 and rule["REMARKS"] == "Payin Above 40%") or
#                     (payin > 50 and rule["REMARKS"] == "Payin Above 50%")):
#                     matching_rule = rule
#                     break

#     if not matching_rule:
#         deduction = 2 if payin <= 20 else 3 if payin <= 30 else 4 if payin <= 50 else 5
#         return f"-{deduction}%", round(payin - deduction, 2)

#     formula = matching_rule["PO"]
#     if "% of Payin" in formula:
#         perc_str = formula.split("%")[0].replace("Less ", "").strip()
#         percentage = float(perc_str)
#         if "Less" in formula:
#             payout = round(payin - percentage, 2)
#         else:
#             payout = round(payin * percentage / 100, 2)
#     elif formula.startswith("-"):
#         deduction = float(formula.replace("%", "").replace("-", ""))
#         payout = round(payin - deduction, 2)
#     else:
#         payout = round(payin - 2, 2)

#     return formula, payout

# def calculate_payout_with_formula(lob: str, segment: str, policy_type: str, payin: float):
#     if payin == 0:
#         return 0, "0% (No Payin)", "Payin is 0"
#     formula, payout = get_formula_from_data(lob, segment, policy_type, payin)
#     return payout, formula, f"Match: LOB={lob}, Segment={segment}, Policy={policy_type}, {get_payin_category(payin)}"

# # ------------------- PROCESSORS -------------------
# def process_tw_sheet(df, override_lob, override_segment, override_policy_type):
#     records = []
#     for _, row in df.iterrows():
#         if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "": continue
#         cluster = str(row.iloc[0]).strip()
#         segmentation = str(row.iloc[1]).strip() if len(row) > 1 else ""
#         comp_cd2 = safe_float(row.iloc[3]) if len(row) > 3 else None
#         satp_cd2 = safe_float(row.iloc[4]) if len(row) > 4 else None

#         state = "MAHARASHTRA" if "MH" in cluster.upper() else "UNKNOWN"
#         lob_final = override_lob or "TW"
#         segment_final = override_segment or "TW"

#         if comp_cd2 is not None:
#             policy_type = override_policy_type or "Comp"
#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, comp_cd2)
#             records.append({"State": state, "Location/Cluster": cluster, "Original Segment": f"TW {segmentation}",
#                             "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
#                             "Payin (CD2)": f"{comp_cd2:.2f}%", "Payin Category": get_payin_category(comp_cd2),
#                             "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})

#         if satp_cd2 is not None:
#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, "TP", satp_cd2)
#             records.append({"State": state, "Location/Cluster": cluster, "Original Segment": f"TW {segmentation}",
#                             "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": "TP",
#                             "Payin (CD2)": f"{satp_cd2:.2f}%", "Payin Category": get_payin_category(satp_cd2),
#                             "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
#     return records

# def process_electric_sheet(df, override_lob, override_segment, override_policy_type):
#     records = []
#     for _, row in df.iterrows():
#         if pd.isna(row.iloc[0]): continue
#         city = str(row.iloc[0]).strip()
#         fuel = str(row.iloc[2]).strip() if len(row) > 2 else "Electric"
#         cvod_cd2 = safe_float(row.iloc[6]) if len(row) > 6 else None
#         cvtp_cd2 = safe_float(row.iloc[7]) if len(row) > 7 else None

#         state = next((v for k, v in STATE_MAPPING.items() if k.upper() in city.upper()), "UNKNOWN")
#         lob_final = override_lob or "TAXI"
#         segment_final = override_segment or "TAXI"

#         if cvod_cd2 is not None:
#             policy_type = override_policy_type or "Comp"
#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, cvod_cd2)
#             records.append({"State": state, "Location/Cluster": city, "Original Segment": f"Taxi {fuel}",
#                             "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
#                             "Payin (CD2)": f"{cvod_cd2:.2f}%", "Payin Category": get_payin_category(cvod_cd2),
#                             "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})

#         if cvtp_cd2 is not None:
#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, "TP", cvtp_cd2)
#             records.append({"State": state, "Location/Cluster": city, "Original Segment": f"Taxi {fuel}",
#                             "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": "TP",
#                             "Payin (CD2)": f"{cvtp_cd2:.2f}%", "Payin Category": get_payin_category(cvtp_cd2),
#                             "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
#     return records

# def process_4w_satp_sheet(df, override_lob, override_segment, override_policy_type):
#     records = []
#     for _, row in df.iterrows():
#         if pd.isna(row.get('Cluster')): continue
#         cluster = str(row['Cluster']).strip()
#         payin = safe_float(row.get('CD2'))
#         if payin is None: continue

#         state = next((v for k, v in STATE_MAPPING.items() if k.upper() in cluster.upper()), "UNKNOWN")
#         lob_final = override_lob or "PVT CAR"
#         segment_final = override_segment or "PVT CAR TP"
#         policy_type = override_policy_type or "TP"

#         payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, payin)
#         records.append({"State": state, "Location/Cluster": cluster, "Original Segment": "PVT CAR TP",
#                         "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
#                         "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
#                         "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
#     return records

# def process_school_bus_sheet(df, override_lob, override_segment, override_policy_type):
#     records = []
#     table_start_row = None
#     for i in range(min(30, len(df))):
#         for j in range(len(df.columns)):
#             cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
#             if "school bus" in cell:
#                 table_start_row = i
#                 break
#         if table_start_row is not None: break
#     if table_start_row is None: return []

#     seating_row = None
#     seating_col = -1
#     for i in range(table_start_row + 1, min(table_start_row + 5, len(df))):
#         for j in range(len(df.columns)):
#             cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
#             if "seating capacity" in cell:
#                 seating_row = i
#                 seating_col = j
#                 break
#         if seating_row is not None: break

#     data_start_row = (seating_row + 1) if seating_row is not None else (table_start_row + 2)

#     if seating_col > 0:
#         state_col = 0
#         rto_col = 1
#         payin_start = seating_col + 1
#         contract_types = [str(df.iloc[seating_row, k]).strip() for k in range(payin_start, len(df.columns)) if str(df.iloc[seating_row, k]).strip()]
#         contracts = [(payin_start + idx, ct) for idx, ct in enumerate(contract_types)]
#     else:
#         state_col = 0
#         rto_col = 1
#         contracts = [(2, "In name of School"), (3, "On Contract (Transporter)"), (4, "On Contract (Individual)"), (5, "Contract transporter")]

#     current_state = ""
#     for row_idx in range(data_start_row, len(df)):
#         first_cell = str(df.iloc[row_idx, state_col]).strip().lower() if pd.notna(df.iloc[row_idx, state_col]) else ""
#         if any(kw in first_cell for kw in ["staff bus", "note"]): break

#         state_val = str(df.iloc[row_idx, state_col]).strip() if pd.notna(df.iloc[row_idx, state_col]) else ""
#         if state_val: current_state = state_val

#         rto_cluster = str(df.iloc[row_idx, rto_col]).strip() if pd.notna(df.iloc[row_idx, rto_col]) else ""
#         if not rto_cluster: continue

#         for col_idx, contract_type in contracts:
#             payin = safe_float(df.iloc[row_idx, col_idx])
#             if payin is None: continue

#             state_mapped = next((v for k, v in STATE_MAPPING.items() if k.upper() in current_state.upper()), current_state.upper())
#             lob_final = override_lob or "BUS"
#             segment_final = override_segment or "SCHOOL BUS"
#             policy_type_final = override_policy_type or "Comp"

#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type_final, payin)
#             record = {
#                 "State": state_mapped.upper(), "Location/Cluster": f"{current_state} - {rto_cluster}",
#                 "Original Segment": f"School Bus - {contract_type}", "Mapped Segment": segment_final,
#                 "LOB": lob_final, "Policy Type": policy_type_final,
#                 "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
#                 "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp
#             }
#             if seating_col > 0:
#                 seating = str(df.iloc[row_idx, seating_col]).strip()
#                 if seating: record["Original Segment"] += f" ({seating})"
#             records.append(record)
#     return records

# def process_staff_bus_sheet(df, override_lob, override_segment, override_policy_type):
#     records = []
#     table_start_row = None
#     for i in range(min(30, len(df))):
#         for j in range(len(df.columns)):
#             cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
#             if "staff bus" in cell:
#                 table_start_row = i
#                 break
#         if table_start_row is not None: break
#     if table_start_row is None: return []

#     data_start_row = table_start_row + 2
#     contracts = [(1, "In name of Company"), (2, "Contract (Transport)"), (3, "Contract (Individual)")]

#     for row_idx in range(data_start_row, len(df)):
#         rto_val = str(df.iloc[row_idx, 0]).strip() if pd.notna(df.iloc[row_idx, 0]) else ""
#         if not rto_val or any(kw in rto_val.lower() for kw in ["note", "permit", "validation", "exception", "above grid"]): continue

#         for col_idx, contract_type in contracts:
#             cell_value = str(df.iloc[row_idx, col_idx]).strip()
#             if not cell_value or "decline" in cell_value.lower(): continue

#             payin = None
#             if "CD2" in cell_value.upper():
#                 for part in cell_value.split("/"):
#                     if "CD2" in part.upper():
#                         cd2_cleaned = part.replace("CD2", "").replace("cd2", "").strip()
#                         payin = safe_float(cd2_cleaned)
#                         break
#             if payin is None: continue

#             state_mapped = next((v for k, v in STATE_MAPPING.items() if k.upper() in rto_val.upper()), "UNKNOWN")
#             lob_final = override_lob or "BUS"
#             segment_final = override_segment or "STAFF BUS"
#             policy_type_final = override_policy_type or "Comp"

#             payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type_final, payin)
#             records.append({
#                 "State": state_mapped.upper(), "Location/Cluster": rto_val,
#                 "Original Segment": f"Staff Bus - {contract_type}", "Mapped Segment": segment_final,
#                 "LOB": lob_final, "Policy Type": policy_type_final,
#                 "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
#                 "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp
#             })
#     return records

# def process_bus_sheet(df, override_lob, override_segment, override_policy_type):
#     return process_school_bus_sheet(df, override_lob, override_segment, override_policy_type) + \
#            process_staff_bus_sheet(df, override_lob, override_segment, override_policy_type)

# # ------------------- API ENDPOINTS -------------------
# @app.get("/")
# async def root():
#     return {"message": "Insurance Policy Processing API", "endpoints": ["/bus"]}

# @app.post("/bus")
# async def process_bus(
#     file: UploadFile = File(...),
#     company_name: str = Form("Unknown"),
#     lob: str = Form("BUS"),
#     override_segment: Optional[str] = Form(None),
#     override_policy_type: Optional[str] = Form(None)
# ):
#     try:
#         # Read the uploaded Excel file
#         contents = await file.read()
        
#         # Try to read as Excel
#         try:
#             xls = pd.ExcelFile(io.BytesIO(contents))
#             sheet_names = xls.sheet_names
            
#             # Process all sheets or find the first relevant one
#             all_records = []
#             processor_name = "Unknown"
            
#             for sheet_name in sheet_names:
#                 df = pd.read_excel(io.BytesIO(contents), sheet_name=sheet_name, header=None)
#                 sheet_lower = sheet_name.lower()
                
#                 if "bus" in sheet_lower:
#                     records = process_bus_sheet(df, lob, override_segment, override_policy_type)
#                     processor_name = "Bus (School + Staff)"
#                 elif "tw" in sheet_lower or "2w" in sheet_lower:
#                     records = process_tw_sheet(df, lob, override_segment, override_policy_type)
#                     processor_name = "Two Wheeler"
#                 elif "electric" in sheet_lower or "taxi" in sheet_lower:
#                     records = process_electric_sheet(df, lob, override_segment, override_policy_type)
#                     processor_name = "Taxi / Electric"
#                 elif "satp" in sheet_lower:
#                     records = process_4w_satp_sheet(df, lob, override_segment, override_policy_type)
#                     processor_name = "4W SATP"
#                 else:
#                     continue
                
#                 all_records.extend(records)
            
#             if not all_records:
#                 return JSONResponse(
#                     status_code=400,
#                     content={"error": "No processable data found in the uploaded file"}
#                 )
            
#             # Create result DataFrame
#             result_df = pd.DataFrame(all_records)
            
#             # Calculate statistics
#             payin_values = []
#             for record in all_records:
#                 payin_str = record.get("Payin (CD2)", "0%")
#                 try:
#                     payin_values.append(float(payin_str.replace("%", "")))
#                 except:
#                     pass
            
#             avg_payin = round(sum(payin_values) / len(payin_values), 2) if payin_values else 0
#             unique_segments = len(result_df["Mapped Segment"].unique()) if "Mapped Segment" in result_df.columns else 0
            
#             # Generate Excel file
#             output = io.BytesIO()
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 result_df.to_excel(writer, index=False, sheet_name='Processed Data')
#             output.seek(0)
#             excel_base64 = base64.b64encode(output.read()).decode()
            
#             # Generate CSV
#             csv_output = result_df.to_csv(index=False)
            
#             # Formula summary
#             formula_summary = {}
#             for record in all_records:
#                 formula = record.get("Formula Used", "Unknown")
#                 formula_summary[formula] = formula_summary.get(formula, 0) + 1
            
#             return JSONResponse(content={
#                 "success": True,
#                 "company_name": company_name,
#                 "processor_used": processor_name,
#                 "total_records": len(all_records),
#                 "avg_payin": avg_payin,
#                 "unique_segments": unique_segments,
#                 "calculated_data": all_records,
#                 "formula_data": FORMULA_DATA,
#                 "formula_summary": formula_summary,
#                 "excel_data": excel_base64,
#                 "csv_data": csv_output,
#                 "extracted_text": f"Processed {len(all_records)} records from Excel file",
#                 "parsed_data": all_records[:5]  # First 5 records for preview
#             })
            
#         except Exception as e:
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": f"Error processing Excel file: {str(e)}"}
#             )
    
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"Server error: {str(e)}"}
#         )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import io
import os
from typing import List, Dict, Optional
from datetime import datetime
import traceback
import tempfile

app = FastAPI(title="DIGIT Multi-LOB Processor API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================================================================
# FORMULA DATA AND STATE MAPPING
# ===============================================================================

FORMULA_DATA = [
    {"LOB": "TW", "SEGMENT": "1+5", "PO": "90% of Payin", "REMARKS": "NIL"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "TW", "SEGMENT": "TW SAOD + COMP", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "TW", "SEGMENT": "TW TP", "PO": "-3%", "REMARKS": "Payin Above 50%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR COMP + SAOD", "PO": "90% of Payin", "REMARKS": "NIL"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 20%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 30%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 40%"},
    {"LOB": "PVT CAR", "SEGMENT": "PVT CAR TP", "PO": "-3%", "REMARKS": "Payin Above 50%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "CV", "SEGMENT": "All GVW & PCV 3W, GCV 3W", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "BUS", "SEGMENT": "SCHOOL BUS", "PO": "Less 2% of Payin", "REMARKS": "NIL"},
    {"LOB": "BUS", "SEGMENT": "STAFF BUS", "PO": "88% of Payin", "REMARKS": "NIL"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-2%", "REMARKS": "Payin Below 20%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-3%", "REMARKS": "Payin 21% to 30%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-4%", "REMARKS": "Payin 31% to 50%"},
    {"LOB": "TAXI", "SEGMENT": "TAXI", "PO": "-5%", "REMARKS": "Payin Above 50%"},
    {"LOB": "MISD", "SEGMENT": "Misd, Tractor", "PO": "88% of Payin", "REMARKS": "NIL"}
]

STATE_MAPPING = {
    "DELHI": "DELHI", "MUMBAI": "MAHARASHTRA", "PUNE": "MAHARASHTRA", "GOA": "GOA",
    "KOLKATA": "WEST BENGAL", "HYDERABAD": "TELANGANA", "AHMEDABAD": "GUJARAT",
    "TAMIL NADU": "TAMIL NADU", "TN": "TAMIL NADU", "CHENNAI": "TAMIL NADU",
    "KERALA": "KERALA", "KARNATAKA": "KARNATAKA", "BANGALORE": "KARNATAKA",
    "GUJARAT": "GUJARAT", "RAJASTHAN": "RAJASTHAN", "PUNJAB": "PUNJAB",
    "UTTAR PRADESH": "UTTAR PRADESH", "DELHI NCR": "DELHI", "REST OF INDIA": "REST OF INDIA",
    "GOOD GJ": "GUJARAT", "BAD GJ": "GUJARAT", "ROM1": "REST OF MAHARASHTRA",
    "ROM2": "REST OF MAHARASHTRA", "GOOD TN": "TAMIL NADU", "GOOD MP": "MADHYA PRADESH"
}

uploaded_files = {}

# ===============================================================================
# CORE CALCULATION FUNCTIONS
# ===============================================================================

def get_payin_category(payin: float):
    if payin <= 20: return "Payin Below 20%"
    elif payin <= 30: return "Payin 21% to 30%"
    elif payin <= 50: return "Payin 31% to 50%"
    else: return "Payin Above 50%"

def safe_float(value):
    if pd.isna(value): return None
    val_str = str(value).strip().upper()
    if val_str in ["D", "NA", "", "NAN", "NONE", "DECLINE"]: return None
    try:
        num = float(val_str.replace('%', '').replace('X', '').strip())
        return num * 100 if 0 < num < 1 else num
    except: return None

def get_formula_from_data(lob: str, segment: str, policy_type: str, payin: float):
    segment_key = segment.upper()
    if lob == "TW":
        segment_key = "TW TP" if policy_type == "TP" else "TW SAOD + COMP"
    elif lob == "PVT CAR":
        segment_key = "PVT CAR TP" if policy_type == "TP" else "PVT CAR COMP + SAOD"
    elif lob in ["TAXI", "CV", "BUS", "MISD"]:
        segment_key = segment.upper()

    payin_category = get_payin_category(payin)
    matching_rule = None
    for rule in FORMULA_DATA:
        if rule["LOB"] == lob and rule["SEGMENT"] == segment_key:
            if rule["REMARKS"] == payin_category or rule["REMARKS"] == "NIL":
                matching_rule = rule
                break

    if not matching_rule and payin > 20:
        for rule in FORMULA_DATA:
            if rule["LOB"] == lob and rule["SEGMENT"] == segment_key:
                if (rule["REMARKS"] == "Payin Above 20%" or
                    (payin > 30 and rule["REMARKS"] == "Payin Above 30%") or
                    (payin > 40 and rule["REMARKS"] == "Payin Above 40%") or
                    (payin > 50 and rule["REMARKS"] == "Payin Above 50%")):
                    matching_rule = rule
                    break

    if not matching_rule:
        deduction = 2 if payin <= 20 else 3 if payin <= 30 else 4 if payin <= 50 else 5
        return f"-{deduction}%", round(payin - deduction, 2)

    formula = matching_rule["PO"]
    if "% of Payin" in formula:
        perc_str = formula.split("%")[0].replace("Less ", "").strip()
        percentage = float(perc_str)
        if "Less" in formula:
            payout = round(payin - percentage, 2)
        else:
            payout = round(payin * percentage / 100, 2)
    elif formula.startswith("-"):
        deduction = float(formula.replace("%", "").replace("-", ""))
        payout = round(payin - deduction, 2)
    else:
        payout = round(payin - 2, 2)

    return formula, payout

def calculate_payout_with_formula(lob: str, segment: str, policy_type: str, payin: float):
    if payin == 0:
        return 0, "0% (No Payin)", "Payin is 0"
    formula, payout = get_formula_from_data(lob, segment, policy_type, payin)
    return payout, formula, f"Match: LOB={lob}, Segment={segment}, Policy={policy_type}, {get_payin_category(payin)}"

# ===============================================================================
# SHEET PROCESSORS
# ===============================================================================

def process_tw_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    records = []
    for _, row in df.iterrows():
        if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == "": continue
        cluster = str(row.iloc[0]).strip()
        segmentation = str(row.iloc[1]).strip() if len(row) > 1 else ""
        comp_cd2 = safe_float(row.iloc[3]) if len(row) > 3 else None
        satp_cd2 = safe_float(row.iloc[4]) if len(row) > 4 else None

        state = "MAHARASHTRA" if "MH" in cluster.upper() else "UNKNOWN"
        lob_final = override_lob if override_enabled and override_lob else "TW"
        segment_final = override_segment if override_enabled and override_segment else "TW"

        if comp_cd2 is not None:
            policy_type = override_policy_type or "Comp"
            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, comp_cd2)
            records.append({"State": state, "Location/Cluster": cluster, "Original Segment": f"TW {segmentation}",
                            "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
                            "Payin (CD2)": f"{comp_cd2:.2f}%", "Payin Category": get_payin_category(comp_cd2),
                            "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})

        if satp_cd2 is not None:
            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, "TP", satp_cd2)
            records.append({"State": state, "Location/Cluster": cluster, "Original Segment": f"TW {segmentation}",
                            "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": "TP",
                            "Payin (CD2)": f"{satp_cd2:.2f}%", "Payin Category": get_payin_category(satp_cd2),
                            "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
    return records

def process_electric_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    records = []
    for _, row in df.iterrows():
        if pd.isna(row.iloc[0]): continue
        city = str(row.iloc[0]).strip()
        fuel = str(row.iloc[2]).strip() if len(row) > 2 else "Electric"
        cvod_cd2 = safe_float(row.iloc[6]) if len(row) > 6 else None
        cvtp_cd2 = safe_float(row.iloc[7]) if len(row) > 7 else None

        state = next((v for k, v in STATE_MAPPING.items() if k.upper() in city.upper()), "UNKNOWN")
        lob_final = override_lob if override_enabled and override_lob else "TAXI"
        segment_final = override_segment if override_enabled and override_segment else "TAXI"

        if cvod_cd2 is not None:
            policy_type = override_policy_type or "Comp"
            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, cvod_cd2)
            records.append({"State": state, "Location/Cluster": city, "Original Segment": f"Taxi {fuel}",
                            "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
                            "Payin (CD2)": f"{cvod_cd2:.2f}%", "Payin Category": get_payin_category(cvod_cd2),
                            "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})

        if cvtp_cd2 is not None:
            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, "TP", cvtp_cd2)
            records.append({"State": state, "Location/Cluster": city, "Original Segment": f"Taxi {fuel}",
                            "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": "TP",
                            "Payin (CD2)": f"{cvtp_cd2:.2f}%", "Payin Category": get_payin_category(cvtp_cd2),
                            "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
    return records

def process_4w_satp_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    records = []
    for _, row in df.iterrows():
        if pd.isna(row.get('Cluster')): continue
        cluster = str(row['Cluster']).strip()
        payin = safe_float(row.get('CD2'))
        if payin is None: continue

        state = next((v for k, v in STATE_MAPPING.items() if k.upper() in cluster.upper()), "UNKNOWN")
        lob_final = override_lob if override_enabled and override_lob else "PVT CAR"
        segment_final = override_segment if override_enabled and override_segment else "PVT CAR TP"
        policy_type = override_policy_type or "TP"

        payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type, payin)
        records.append({"State": state, "Location/Cluster": cluster, "Original Segment": "PVT CAR TP",
                        "Mapped Segment": segment_final, "LOB": lob_final, "Policy Type": policy_type,
                        "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
                        "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp})
    return records

def process_school_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    records = []
    table_start_row = None
    for i in range(min(30, len(df))):
        for j in range(len(df.columns)):
            cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
            if "school bus" in cell:
                table_start_row = i
                break
        if table_start_row is not None: break
    if table_start_row is None: return []

    seating_row = None
    seating_col = -1
    for i in range(table_start_row + 1, min(table_start_row + 5, len(df))):
        for j in range(len(df.columns)):
            cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
            if "seating capacity" in cell:
                seating_row = i
                seating_col = j
                break
        if seating_row is not None: break

    data_start_row = (seating_row + 1) if seating_row is not None else (table_start_row + 2)

    if seating_col > 0:
        state_col = 0
        rto_col = 1
        payin_start = seating_col + 1
        contract_types = [str(df.iloc[seating_row, k]).strip() for k in range(payin_start, len(df.columns)) if str(df.iloc[seating_row, k]).strip()]
        contracts = [(payin_start + idx, ct) for idx, ct in enumerate(contract_types)]
    else:
        state_col = 0
        rto_col = 1
        contracts = [(2, "In name of School"), (3, "On Contract (Transporter)"), (4, "On Contract (Individual)"), (5, "Contract transporter")]

    current_state = ""
    for row_idx in range(data_start_row, len(df)):
        first_cell = str(df.iloc[row_idx, state_col]).strip().lower() if pd.notna(df.iloc[row_idx, state_col]) else ""
        if any(kw in first_cell for kw in ["staff bus", "note"]): break

        state_val = str(df.iloc[row_idx, state_col]).strip() if pd.notna(df.iloc[row_idx, state_col]) else ""
        if state_val: current_state = state_val

        rto_cluster = str(df.iloc[row_idx, rto_col]).strip() if pd.notna(df.iloc[row_idx, rto_col]) else ""
        if not rto_cluster: continue

        for col_idx, contract_type in contracts:
            payin = safe_float(df.iloc[row_idx, col_idx])
            if payin is None: continue

            state_mapped = next((v for k, v in STATE_MAPPING.items() if k.upper() in current_state.upper()), current_state.upper())
            lob_final = override_lob if override_enabled and override_lob else "BUS"
            segment_final = override_segment if override_enabled and override_segment else "SCHOOL BUS"
            policy_type_final = override_policy_type or "Comp"

            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type_final, payin)
            record = {
                "State": state_mapped.upper(), "Location/Cluster": f"{current_state} - {rto_cluster}",
                "Original Segment": f"School Bus - {contract_type}", "Mapped Segment": segment_final,
                "LOB": lob_final, "Policy Type": policy_type_final,
                "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
                "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp
            }
            if seating_col > 0:
                seating = str(df.iloc[row_idx, seating_col]).strip()
                if seating: record["Original Segment"] += f" ({seating})"
            records.append(record)
    return records

def process_staff_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    records = []
    table_start_row = None
    for i in range(min(30, len(df))):
        for j in range(len(df.columns)):
            cell = str(df.iloc[i, j]).strip().lower() if pd.notna(df.iloc[i, j]) else ""
            if "staff bus" in cell:
                table_start_row = i
                break
        if table_start_row is not None: break
    if table_start_row is None: return []

    data_start_row = table_start_row + 2
    contracts = [(1, "In name of Company"), (2, "Contract (Transport)"), (3, "Contract (Individual)")]

    for row_idx in range(data_start_row, len(df)):
        rto_val = str(df.iloc[row_idx, 0]).strip() if pd.notna(df.iloc[row_idx, 0]) else ""
        if not rto_val or any(kw in rto_val.lower() for kw in ["note", "permit", "validation", "exception", "above grid"]): continue

        for col_idx, contract_type in contracts:
            cell_value = str(df.iloc[row_idx, col_idx]).strip()
            if not cell_value or "decline" in cell_value.lower(): continue

            payin = None
            if "CD2" in cell_value.upper():
                for part in cell_value.split("/"):
                    if "CD2" in part.upper():
                        cd2_cleaned = part.replace("CD2", "").replace("cd2", "").strip()
                        payin = safe_float(cd2_cleaned)
                        break
            if payin is None: continue

            state_mapped = next((v for k, v in STATE_MAPPING.items() if k.upper() in rto_val.upper()), "UNKNOWN")
            lob_final = override_lob if override_enabled and override_lob else "BUS"
            segment_final = override_segment if override_enabled and override_segment else "STAFF BUS"
            policy_type_final = override_policy_type or "Comp"

            payout, formula, rule_exp = calculate_payout_with_formula(lob_final, segment_final, policy_type_final, payin)
            records.append({
                "State": state_mapped.upper(), "Location/Cluster": rto_val,
                "Original Segment": f"Staff Bus - {contract_type}", "Mapped Segment": segment_final,
                "LOB": lob_final, "Policy Type": policy_type_final,
                "Payin (CD2)": f"{payin:.2f}%", "Payin Category": get_payin_category(payin),
                "Calculated Payout": f"{payout:.2f}%", "Formula Used": formula, "Rule Explanation": rule_exp
            })
    return records

def process_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type):
    return process_school_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type) + \
           process_staff_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type)

def detect_sheet_type(sheet_name: str) -> str:
    """Detect processor type from sheet name."""
    sheet_lower = sheet_name.lower()
    if "bus" in sheet_lower:
        return "bus"
    elif "tw" in sheet_lower or "2w" in sheet_lower:
        return "tw"
    elif "electric" in sheet_lower or "taxi" in sheet_lower:
        return "taxi"
    elif "satp" in sheet_lower:
        return "4w_satp"
    return "unknown"

# ===============================================================================
# API ENDPOINTS
# ===============================================================================

@app.get("/")
async def root():
    return {"message": "DIGIT Multi-LOB Processor API", "version": "1.0"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an Excel file and return available worksheets with detected types."""
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")
        
        content = await file.read()
        xls = pd.ExcelFile(io.BytesIO(content))
        sheets = xls.sheet_names
        
        # Detect sheet types
        sheet_info = []
        for sheet in sheets:
            sheet_type = detect_sheet_type(sheet)
            sheet_info.append({
                "name": sheet,
                "type": sheet_type,
                "icon": {
                    "bus": "🚌",
                    "tw": "🏍️",
                    "taxi": "🚕",
                    "4w_satp": "🚗",
                    "unknown": "📄"
                }.get(sheet_type, "📄")
            })
        
        file_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        uploaded_files[file_id] = {
            "content": content,
            "filename": file.filename,
            "sheets": sheets,
            "sheet_info": sheet_info
        }
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "sheets": sheets,
            "sheet_info": sheet_info,
            "message": f"File uploaded successfully. Found {len(sheets)} worksheet(s)."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/process")
async def process_sheet(
    file_id: str,
    sheet_name: str,
    override_enabled: bool = False,
    override_lob: Optional[str] = None,
    override_segment: Optional[str] = None,
    override_policy_type: Optional[str] = None
):
    """Process a specific worksheet."""
    try:
        if file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="File not found. Please upload the file again.")
        
        file_data = uploaded_files[file_id]
        content = file_data["content"]
        
        if sheet_name not in file_data["sheets"]:
            raise HTTPException(status_code=400, detail=f"Sheet '{sheet_name}' not found in file")
        
        # Load sheet
        df = pd.read_excel(io.BytesIO(content), sheet_name=sheet_name, header=None)
        
        # Detect processor type
        sheet_type = detect_sheet_type(sheet_name)
        
        # Process based on type
        if sheet_type == "bus":
            records = process_bus_sheet(df, override_enabled, override_lob, override_segment, override_policy_type)
            processor_name = "Bus (School + Staff)"
        elif sheet_type == "tw":
            records = process_tw_sheet(df, override_enabled, override_lob, override_segment, override_policy_type)
            processor_name = "Two Wheeler"
        elif sheet_type == "taxi":
            records = process_electric_sheet(df, override_enabled, override_lob, override_segment, override_policy_type)
            processor_name = "Taxi / Electric"
        elif sheet_type == "4w_satp":
            # For SATP, load with headers
            df_header = pd.read_excel(io.BytesIO(content), sheet_name=sheet_name, header=0)
            records = process_4w_satp_sheet(df_header, override_enabled, override_lob, override_segment, override_policy_type)
            processor_name = "4W SATP"
        else:
            return {
                "success": False,
                "message": f"No matching processor found for sheet '{sheet_name}'",
                "records": [],
                "count": 0
            }
        
        if not records:
            return {
                "success": False,
                "message": "No records extracted. Please check the sheet structure.",
                "records": [],
                "count": 0,
                "processor": processor_name
            }
        
        # Calculate summary statistics
        states = {}
        lobs = {}
        policies = {}
        payins = []
        payouts = []
        
        for record in records:
            state = record.get("State", "Unknown")
            states[state] = states.get(state, 0) + 1
            
            lob = record.get("LOB", "Unknown")
            lobs[lob] = lobs.get(lob, 0) + 1
            
            policy = record.get("Policy Type", "Unknown")
            policies[policy] = policies.get(policy, 0) + 1
            
            try:
                payin = float(record.get("Payin (CD2)", "0%").replace('%', ''))
                payout = float(record.get("Calculated Payout", "0%").replace('%', ''))
                if payin > 0:
                    payins.append(payin)
                    payouts.append(payout)
            except:
                pass
        
        avg_payin = sum(payins) / len(payins) if payins else 0
        avg_payout = sum(payouts) / len(payouts) if payouts else 0
        
        summary = {
            "total_records": len(records),
            "states": dict(sorted(states.items(), key=lambda x: x[1], reverse=True)[:10]),
            "lobs": lobs,
            "policies": policies,
            "average_payin": round(avg_payin, 2),
            "average_payout": round(avg_payout, 2),
            "processor": processor_name,
            "sheet_type": sheet_type
        }
        
        return {
            "success": True,
            "message": f"Successfully processed {len(records)} records using {processor_name}",
            "records": records,
            "count": len(records),
            "summary": summary
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing sheet: {str(e)}")

@app.post("/export")
async def export_to_excel(file_id: str, sheet_name: str, records: List[Dict]):
    """Export processed records to Excel file."""
    try:
        if not records:
            raise HTTPException(status_code=400, detail="No records to export")
        
        df = pd.DataFrame(records)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MultiLOB_Processed_{sheet_name.replace(' ', '_')}_{timestamp}.xlsx"
        
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, filename)
        
        df.to_excel(output_path, index=False, sheet_name='Processed')
        
        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
