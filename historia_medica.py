from connection import connect_to_mongodb

collection = connect_to_mongodb("EntregaDeMedicamentos", "historiaMedica")

def GetHistoriaMedicaPorIdPaciente(patient_id: str):
    try:
        historia = collection.find_one({"patient_id": patient_id})
        if historia:
            historia["_id"] = str(historia["_id"])
            return "success", historia
        return "notFound", None
    except Exception as e:
        return f"error: {str(e)}", None
