import uvicorn
from fastapi import FastAPI,UploadFile,File,Body
from models.models import File_entity
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
import os
import json
from typing import List
import uuid
import boto3
import supabase

app = FastAPI()

# Initialize Supabase client
supabase_url = "https://zeqeckzogqdxaugnhnqa.supabase.co"
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InplcWVja3pvZ3FkeGF1Z25obnFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU3MjgxNTMsImV4cCI6MjAxMTMwNDE1M30.A_8F1DysbYYu7ydeWuR7yAKKIL_8Ir3jeDz-mBQDSGk'
supabase_client = supabase.Client(supabase_url, supabase_key)


# Define the table name you want to perform the upsert on
TABLE_NAME = 'File'


# def insert_file_data(file_path, file_type, file_language, user_id):
#     try: 
#         data_to_insert = [
#             {
#                 "file_path": file_path,
#                 "file_type": file_type,
#                 "file_language": file_language,
#                 "user_id": user_id
#             },
#         ]
#         response_insert = supabase.from_("FILE").upsert(data_to_insert).execute()

#         extraction_d = [record for record in response_insert.data]
#         response_i = json.dumps(extraction_d)
#         file_response = json.loads(response_i)
#         file_id = file_response[0]['file_id']

#         #logger.info("inserted file data done")

#         return {"file_id", file_id}
#     except Exception as e:
#         #logger.error(e)
#         return {"error": e}
    

@app.post("/brand_guidelines_asset/", response_model=dict())
async def create_file(File:File_entity):
    # Insert a new File into the Supabase database
    File = File.dict()
    response = supabase_client.table(TABLE_NAME).upsert([File]).execute()
    if response:
        created_file = response.data[0]
        return {'file':created_file}
    else:
        raise HTTPException(status_code=500, detail="Failed to create file record")
    

@app.get("/brand_guidelines_asset/{file_id}", response_model=File_entity)
async def read_file(file_name:str,user_id:str):
    # Fetch a file by ID from the Supabase database
    response = dict(supabase_client.table(TABLE_NAME).select("*").match({'file_name':file_name, 'user_id':user_id}).execute())
    if response:
        return response['data'][0]
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch file")

@app.get("/brand_guidelines_asset/", response_model=List[File_entity])
async def read_files(user_id:str):
    # Fetch all todos from the Supabase database
    response =  supabase_client.table(TABLE_NAME).select('*').eq("user_id",user_id).execute()
    if response:
        return response.data
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch files")

@app.put("/brand_guidelines_asset/{file_id}", response_model=File_entity)
async def update_file(file_id: int, updated_file: File_entity):
    # Update a file in the Supabase database
    response =  supabase_client.table(TABLE_NAME).update([updated_file.dict()]).eq("file_id", file_id).execute()
    if response:
        updated_record = response.data[0]
        if updated_record:
            return updated_record
        else:
            raise HTTPException(status_code=404, detail="file id not found")
    else:
        raise HTTPException(status_code=500, detail="Failed to update file")

@app.delete("/brand_guidelines_asset/{file_id}", response_model=dict())
async def delete_file(file_name:str,user_id:str):
    # Delete a todo from the Supabase database
    response =  dict(supabase_client.table(TABLE_NAME).delete().match({'file_name':file_name, 'user_id':user_id}).execute())
    if response:
        deleted_file = response['data']
        if deleted_file:
            return deleted_file
        else:
            raise HTTPException(status_code=404, detail="File not found")
    else:
        raise HTTPException(status_code=500, detail="Failed to delete file")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)