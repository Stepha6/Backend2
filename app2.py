from fastapi import APIRouter, Depends, HTTPException
from app.auth import verificar_farmaceutico
from app.controllers.historia_medica_controller import GetHistoriaMedicaByPatientId

from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById,WritePatient,GetPatientByIdentifier
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

router = APIRouter()

@router.get("/historia-medica/{patient_id}")
def obtener_historia_medica(patient_id: str, usuario=Depends(verificar_farmaceutico)):
    status, historia = GetHistoriaMedicaByPatientId(patient_id)
    if status == "success":
        return historia
    raise HTTPException(status_code=404, detail="Historia médica no encontrada")


@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    status,patient = GetPatientById(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")
@app.get("/patient", response_model=dict)
async def get_patient_by_identifier(system: str, value: str):
    status,patient = GetPatientByIdentifier(system,value)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")
@app.post("/patient", response_model=dict)
async def add_patient(request: Request):
    new_patient_dict = dict(await request.json())
    status,patient_id = WritePatient(new_patient_dict)
    if status=='success':
        return {"_id":patient_id}  # Return patient id
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
