from fastapi import FastAPI, File, UploadFile, HTTPException,Form
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
import uuid
from sam_processor import process_image_with_sam
from fastapi.middleware.cors import CORSMiddleware
from solar_anywhere_api import GetSolarData
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin. Replace "*" with specific domains for security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.).
    allow_headers=["*"],  # Allows all HTTP headers.
)

# Temporary storage for processed reports
TEMP_REPORTS = {}

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...),cityName:str = Form(...)):
    # Check file type
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload JPEG or PNG.")

    # Read image data
    image_data = await image.read()
    print("Image reading complete")
    pil_image = Image.open(BytesIO(image_data))
    print("PIL image created")
    # Process image with SAM
    result = process_image_with_sam(pil_image)

    if(result):
        print("Image processed properly")
    # # Generate a unique filename for the report
    # report_id = str(uuid.uuid4())
    # report_path = f"temp/{report_id}.pdf"

    # # Generate the report
    # generate_report(result, report_path)

    # # Store the report path temporarily
    # TEMP_REPORTS[report_id] = report_path
    Api_data = await GetSolarData(cityName)
    n_panel = 0.15
    n_system = 0.85
    alpha = 0.005
    temp = Api_data["data"]["TEMP"]

    # print(Api_data)

    # print(Api_data["data"]["GHI"])
    usable_area = result["total_area"]*0.83
    Solar_EGP = (Api_data["data"]["GHI"]/365) * usable_area * n_panel * n_system * (1 - alpha*(temp-25))

    score = round((Solar_EGP/usable_area)*10 ,1)


    final_output = {"message": "Image processed successfully",  "potential": Solar_EGP , "aey":Solar_EGP*365 , "monthwise_output":Api_data["data"]["PVOUT"]["total"]["monthly"], "totalArea":result["total_area"], "result_index":score, "dni":Api_data["data"]["DNI"],"ghi":Api_data["data"]["GHI"],"dif":Api_data["data"]["DIF"], "gti_opta":Api_data["data"]["GTI_opta"],"temp":Api_data["data"]["TEMP"],"opta":Api_data["data"]["OPTA"],"ele":Api_data["data"]["ELE"]  }
    print(final_output)
    return final_output


@app.get("/external")
async def CallApi():
    response  = GetSolarData()
    return response

# @app.get("/download/{report_id}")
# async def download_report(report_id: str):
#     # Check if report exists
#     report_path = TEMP_REPORTS.get(report_id)
#     if not report_path:
#         raise HTTPException(status_code=404, detail="Report not found.")

#     # Serve the report file
#     return FileResponse(report_path, media_type="application/pdf", filename="solar_potential_report.pdf")
