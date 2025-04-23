from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

# Conexión a colecciones
pacientes_collection = connect_to_mongodb("SamplePatientService2", "pacientes")
historia_collection = connect_to_mongodb("SamplePatientService2", "historiaMedica")

# Obtener paciente por ID
def GetPatientById(patient_id: str):
    try:
        patient = pacientes_collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return "error", None

# Escribir nuevo paciente
def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    validated_patient_json = pat.model_dump()
    result = pacientes_collection.insert_one(validated_patient_json)
    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None

# Obtener paciente por identificador
def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        patient = pacientes_collection.find_one({
            "identifier.system": patientSystem,
            "identifier.value": patientValue
        })
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"error: {str(e)}", None

# 🔹 NUEVA FUNCIÓN: Obtener historia médica por ID de paciente
def GetHistoriaMedicaPorIdPaciente(patient_id: str):
    try:
        historia = historia_collection.find_one({"patient_id": patient_id})
        if historia:
            historia["_id"] = str(historia["_id"])
            return "success", historia
        return "notFound", None
    except Exception as e:
        return f"error: {str(e)}", None
