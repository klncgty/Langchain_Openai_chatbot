import aiohttp
import asyncio
from discord import File
from easyocr import Reader
from PIL import Image
import io
import numpy as np
from anahtar_kelimeler import A

class DiscordService:
    def __init__(self, client, assistant):
        self.client = client
        self.assistant = assistant
        self.reader = Reader(['en'])

    async def on_message(self, message):
        await self.handle_message(message)

    async def handle_ready(self):
        print(f'{self.client.user.name} has connected to Discord!')

    async def handle_message(self, message):
        channel = message.channel
        content = message.content.lower()

        if message.author == self.client.user:
            return

        elif any(keyword in content for keyword in ["fiyat", "ücret", "miuul"]):
            await channel.send("Miuul Eğitimleri ile ilgili mentorlerimize direkt mesaj yoluyla danışabilirsiniz :)")
            await channel.send("Detaylı bilgi için Miuul Bootcamp kataloğunu inceleyebilirsiniz: [Miuul Katalog](https://miuul.com/katalog?tur=bootcamp)")

        elif "path" in content and "bootcamp" in content:
            await channel.send("Bootcamp programında program öncesi ön hazırlık eğitimi, canlı mentor desteği, Vahit Keskin ile birlikte haftalık recap, takım çalışması ve IK ve teknik mülakatlar gibi içerikler mevcuttur.")
            await channel.send("[MIUUL](https://www.miuul.com/)'a tıklayarak tüm detaylara ulaşabilirsiniz. Daha detaylı bilgiler için mentorlerimizden de destek alabilirsiniz :)")

        elif "bootcamp" in content:
            await channel.send("Bootcamp programında program öncesi ön hazırlık eğitimi, canlı mentor desteği, Vahit Keskin ile birlikte haftalık recap, takım çalışması ve IK ve teknik mülakatlar gibi içerikler mevcuttur.")
            await channel.send("Miuul Bootcamp kataloğunu inceleyebilirsiniz: [Miuul Bootcamp Kataloğu](https://miuul.com/katalog?tur=bootcamp)")

        elif "path" in content:
            await channel.send("Path programında eğitimler tekildir ve kendi öğrenme hızınıza göre takip ediyor olacaksınız. Tüm içeriklere 1 yıl erişim hakkınız bulunmaktadır. Sorularınız olması durumunda da mentorlarımız ile 7/24 iletişim kurarak süreci ilerletiyor olacaksınız.")
            await channel.send("Bu linkten Miuul Path kataloğunu inceleyebilirsiniz: [Miuul Path Kataloğu](https://www.miuul.com/katalog?tur=kariyer&gclid=CjwKCAjw9-6oBhBaEiwAHv1QvKewPIfjJ78iUKuZGDVMbO5MZDFINlIG62Yssx8rcEmw0jiqH1Tv1RoC24QQAvD_BwE)")

        elif "teşekkür" in content:
            await channel.send("Ne demek, rica ederim. İyi çalışmalar! :)")

        elif "selam" in content or "naber" in content or "merhaba" in content:
            await channel.send("Merhaba! Ben Miuul yapay zeka botuyum. Size nasıl yardımcı olabilirim :) ")

        elif any(kelime.lower() in content for kelime in A):
            await channel.send('Cevabınızı düşünüyorum!')
            gpt_answer = self.assistant.process_message(message)
            await channel.send(gpt_answer)

        elif message.attachments and any(attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')) for attachment in message.attachments):
            image_url = message.attachments[0].url
            image_bytes = await self.fetch_image_data(image_url)
            text_result = self.extract_text_from_image(image_bytes)
            content = f"{content} Bu hatayı şu adımlarla çözebiliriz."
            gpt_answer_combined = self.assistant.process_message(content, image_text=text_result)
            await channel.send(gpt_answer_combined)
            #await channel.send(f"Metin içeren görselde bulunan metin: {text_result}")
            
        else:
            await channel.send("Ben Miuul path yapay zeka botuyum. Bu konularda sorunuz varsa size yardımcı olmayı çok isterim. Başka konularda yardımcı")

    async def fetch_image_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    def extract_text_from_image(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes))
        result = self.reader.readtext(np.array(img))
        extracted_text = " ".join(entry[1] for entry in result)
        return extracted_text
