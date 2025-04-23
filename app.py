from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

# Colecciones
patient_collection = connect_to_mongodb("EntregaDeMedicamentos", "medicationRequest")  # Aquí puedes usar otra colección más apropiada
historia_collection = connect_to_mongodb("EntregaDeMedicamentos", "historiaMedica")

# Obtener historia médica por ID de paciente (función para farmacéuticos)
def GetHistoriaMedicaByPatientId(patient_id: str):
    try:
        historia = historia_collection.find_one({"paciente_id": patient_id})
        if historia:
            historia["_id"] = str(historia["_id"])
            return "success", historia
        return "notFound", None
    except Exception as e:
        return f"error: {str(e)}", None
