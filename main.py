import asyncio
import os

from pocketbase import PocketBase
from pocketbase.models.dtos import RealtimeEvent

from uploadFile import modify_record_pdf
from generate import generatePDF

from dotenv import load_dotenv
load_dotenv()

async def get_record_changes(col, record_id: str):
    """Retrieves and prints record changes, incorporating timeout handling."""

    async def handle_event(event: RealtimeEvent) -> None:
        if event["action"] == "update" and event["record"]["id"] == record_id:
            print("------Updated record------")
            lang = event["record"]["lang"]
            generatePDF(event["record"]["json"],lang)
            if lang == "fr":
                id = os.getenv("CV_FR_ID")
            else:
                id = os.getenv("CV_EN_ID")
            await modify_record_pdf(
                os.getenv("POCKET_BASE_URL"),
                "CV",
                id,
                "./build/output"+lang+".pdf",
                os.getenv("POCKET_BASE_EMAIL_AUTH"),
                os.getenv("POCKET_BASE_PASSWORD_AUTH"),
            )

    # Get the initial record data
    try:
        record = await col.get_one(record_id)
        print("------Initial record------")
        lang = record["lang"]
        generatePDF(record["json"],lang)

        if lang == "fr":
            id = os.getenv("CV_FR_ID")
        else:
            id = os.getenv("CV_EN_ID")
        await modify_record_pdf(
            os.getenv("POCKET_BASE_URL"),
            os.getenv("POCKET_BASE_CV_COLLECTION"),
            id,
            "./build/output"+record["lang"]+".pdf",
            os.getenv("POCKET_BASE_EMAIL_AUTH"),
            os.getenv("POCKET_BASE_PASSWORD_AUTH"),
        )
    except Exception as e:
        print(f"Error retrieving initial record: {e}")

    while True:
        try:
            unsub = await col.subscribe(handle_event, record_id)
            await asyncio.sleep(60)  # Adjust timeout as needed
        except asyncio.TimeoutError:
            print("** Timeout detected, restarting... **")
        except Exception as e:  # Catch other potential errors
            print(f"Unexpected error: {e}")
        finally:
            if unsub:  # Unsubscribe if still active
                try:
                    await unsub()
                except Exception as e:
                    print(f"Error unsubscribing: {e}")

async def main():

    client = PocketBase(os.getenv("POCKET_BASE_URL"))
    col = client.collection(os.getenv("POCKET_BASE_AutoLatexCv_COLLECTION"))

    try:
        tasks = [
            get_record_changes(col, os.getenv("POCKET_BASE_AutoLatexCv_RECORD_ID_FR")),
            get_record_changes(col, os.getenv("POCKET_BASE_AutoLatexCv_RECORD_ID_EN")),
        ]

        await asyncio.gather(*tasks)  # Unpack tasks into the function call

    except asyncio.CancelledError:
        pass

asyncio.run(main())
