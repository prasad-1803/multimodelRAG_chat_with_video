
from mm_rag.embeddings.bridgetower_embeddings import BridgeTowerEmbeddings  
from mm_rag.vectorstores.multimodel_lancedb import MultimodalLanceDB
import lancedb  # For connecting to LanceDB
import json  # For handling JSON data
import os  # For working with file paths and directories
from PIL import Image  # For image handling
from utils import load_json_file, display_retrieved_results  # Utility functions for loading JSON and displaying results
import pyarrow as pa  # Import pyarrow for schema definition



# declare host file
LANCEDB_HOST_FILE = "./shared_data/.lancedb"
# declare table name
TBL_NAME = "test_tbl"
# initialize vectorstore
# Connect to LanceDB
db = lancedb.connect(LANCEDB_HOST_FILE)
print(dir(db))  # This will list all available methods on the `db` object


# List available tables
available_tables = db.table_names()  # Use table_names() instead of list_tables()
print("Available tables:", available_tables)

# Check if the specific table exists
if TBL_NAME in available_tables:
    print(f"Table '{TBL_NAME}' is available.")
else:
    print(f"Table '{TBL_NAME}' does not exist.")

    # Define a schema for the table (e.g., text, image path, metadata)
    schema = pa.schema([
        ("transcript", pa.string()),  # Transcript stored as string
        ("image_path", pa.string()),  # Image path stored as string
        ("metadata", pa.string())     # Metadata stored as string (JSON)
    ])

    # Create the table in LanceDB
    table = db.create_table(TBL_NAME, schema=schema)
    print(f"Table '{TBL_NAME}' created successfully!")

# load metadata files
vid1_metadata_path = './data/video1/metadatas.json'

vid1_metadata = load_json_file(vid1_metadata_path)


# collect transcripts and image paths
vid1_trans = [vid['transcript'] for vid in vid1_metadata]
vid1_img_path = [vid['extracted_frame_path'] for vid in vid1_metadata]

# for video1, we pick n = 7
n = 7
updated_vid1_trans = [
 ' '.join(vid1_trans[i-int(n/2) : i+int(n/2)]) if i-int(n/2) >= 0 else
 ' '.join(vid1_trans[0 : i + int(n/2)]) for i in range(len(vid1_trans))
]

# also need to update the updated transcripts in metadata
for i in range(len(updated_vid1_trans)):
    vid1_metadata[i]['transcript'] = updated_vid1_trans[i]

    # initialize an BridgeTower embedder 
embedder = BridgeTowerEmbeddings()


# you can pass in mode="append" 
# to add more entries to the vector store
# in case you want to start with a fresh vector store,
# you can pass in mode="overwrite" instead 

_ = MultimodalLanceDB.from_text_image_pairs(
    texts=updated_vid1_trans,
    image_paths=vid1_img_path,
    embedding=embedder,
    metadatas=vid1_metadata,
    connection=db,
    table_name=TBL_NAME,
    mode="overwrite", 
)