from pocketbase import FileUpload, PocketBase
import os
import asyncio

async def modify_record_pdf(
    pocketbase_url: str,
    collection_name: str,
    record_id: str,
    pdf_path: str,
    email: str,
    password: str,
):
    """
    Modifies a PDF file in a record.

    Args:
        pocketbase_url (str): The URL of the PocketBase instance.
        collection_name (str): The name of the collection containing the record.
        record_id (str): The ID of the record to modify.
        pdf_path (str): The path to the new PDF file.
        email (str): The email address of the administrator.
        password (str): The password of the administrator.

    Raises:
        ValueError: If the PocketBase URL is invalid.
        Exception: If the authentication fails or the record cannot be modified.
    """

    try:
        pb = PocketBase(pocketbase_url)
    except ValueError as e:
        raise ValueError(f"Invalid PocketBase URL: {pocketbase_url}") from e

    # Authenticate as administrator
    try:
        await pb.admins.auth.with_password(email, password)
    except Exception as e:
        raise Exception("Failed to authenticate as administrator") from e

    collection = pb.collection(collection_name)

    # Get the existing record to avoid overwriting other data
    record = await collection.get_one(record_id)

    # Prepare the new file data
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    # Create a FileUpload object to represent the new PDF
    new_file = FileUpload((os.path.basename(pdf_path), pdf_content, "application/pdf"))

    # Update the record with the new file
    updated_record = {
        "id": record["id"],
        "PDF": new_file,  # Ensure correct field name is used
    }

    try:
        await collection.update(updated_record["id"], updated_record)
        print("PDF file in the record has been successfully modified.")
    except Exception as e:
        print(f"Error modifying PDF: {e}")
