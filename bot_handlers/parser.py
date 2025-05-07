import os
import tempfile
import pdfplumber
from aiogram.types import Message
from aiogram.filters import Command

from bot_handlers.states import ParsePDFState


def parse_handlers(dp):
    @dp.message(Command("parse"))
    async def ask_for_pdf(message: Message, state):
        await message.answer("Please send the PDF file you want to parse.")
        await state.set_state(ParsePDFState.waiting_for_pdf)

    @dp.message(ParsePDFState.waiting_for_pdf, lambda msg: msg.document and msg.document.mime_type == "application/pdf")
    async def handle_pdf(message: Message, bot, state):
        file = message.document
        telegram_file = await bot.get_file(file.file_id)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, file.file_name)
            with open(file_path, "wb") as f:
                await bot.download(file=telegram_file, destination=f)

            extracted_data = parse_pdf(file_path)
            response = format_extracted_data(extracted_data)
            await message.answer(response)
            await state.clear()

    def parse_pdf(pdf_path):
        extracted_data = {
            "Name": "",
            "Registry Code": "",
            "Location": "",
            "Phone": "",
            "Email": "",
            "Banks": []
        }

        field_map = {
            "Name:": "Name",
            "Registry code:": "Registry Code",
            "Location:": "Location",
            "Phone:": "Phone",
            "E-mail:": "Email"
        }

        bank_names = {"LHV", "Swedbank", "SEB"}

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.splitlines():
                    line = line.strip()

                    for prefix, key in field_map.items():
                        if line.startswith(prefix):
                            extracted_data[key] = line[len(prefix):].strip()

                    for bank in bank_names:
                        if line.startswith(bank):
                            parts = line.split()
                            if len(parts) >= 4:
                                extracted_data["Banks"].append({
                                    "bank": parts[0],
                                    "iban": parts[1],
                                    "swift": parts[3]
                                })

        return extracted_data

    def format_extracted_data(data: dict) -> str:
        result = (
            f"📄 <b>Parsed Data:</b>\n"
            f"<b>Name:</b> {data['Name']}\n"
            f"<b>Registry Code:</b> {data['Registry Code']}\n"
            f"<b>Location:</b> {data['Location']}\n"
            f"<b>Phone:</b> {data['Phone']}\n"
            f"<b>Email:</b> {data['Email']}\n"
        )
        if data["Banks"]:
            result += "\n🏦 <b>Bank Accounts:</b>\n"
            for bank in data["Banks"]:
                result += (
                    f"- <b>{bank['bank']}</b>\n"
                    f"   IBAN: <code>{bank['iban']}</code>\n"
                    f"   SWIFT: <code>{bank['swift']}</code>\n"
                )
        return result
