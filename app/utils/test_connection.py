from db import IrisDB

def test_connection():
    try:
        db = IrisDB()
        # Test insert
        test_doc = {"test": "connection"}
        result = db.iris_collection.insert_one(test_doc)
        print("✅ Database verbinding succesvol!")
        # Verwijder test document
        db.iris_collection.delete_one({"_id": result.inserted_id})
    except Exception as e:
        print(f"❌ Database verbinding mislukt: {str(e)}")

if __name__ == "__main__":
    test_connection() 