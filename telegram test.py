import asyncio
from telegram import Bot
import mysql.connector
import phpserialize



# Telegram bot configuration
BOT_TOKEN = "7592753226:AAEARI60OqXGPEFknxcTaG2ZoAPWXYHaRE0"
CHANNEL_USERNAME = "-1002402189186"  # Replace with your channel username

# Database connection configuration
db_config = {
    "host": "192.168.10.135",
    "user": "ken",
    "password": "247asap!@#",
    "database": "wordpress"
}

# Dictionary mapping metadata keys to questions
questions_map = {
    # Have Better Sex Questions
    "_havebettersex_0": "1. 您目前是否正在服用下列藥物？\n"
                        "止血劑：如氨甲環酸、依沙唑嗪\n"
                        "生理鹽水溶液：例如生理鹽水\n"
                        "三環抗憂鬱劑 (TCA)：例如阿米替林、去甲替林、氯米帕明、多巴胺\n"
                        "曲美布汀 (曲馬多)\n"
                        "多塞平氫溴酸鹽\n"
                        "更年期藥物：如共轭雌激素\n"
                        "抗憂鬱劑：如氟西汀、舍曲林、帕羅西汀\n"
                        "止痛劑：如氫可酮、奧施康定\n"
                        "抗焦慮藥物：如 Xanax (alprazolam)、Valium (diazepam)\n"
                        "其他治療藥物：如鋰、氯氮平",
    "_havebettersex_1": "2. 您是否對 Priligy 或 Dapoxetine 過敏？",
    "_havebettersex_2": "3. 您會喝酒嗎？ ",
    "_havebettersex_3": "4. 您是否正在服用任何與排尿症狀有關的藥物或補充劑？",
    "_havebettersex_4": "5. 您在排尿時是否有任何異常的症狀或不適？ ",
    "_havebettersex_5": "6. 您是否曾經服用必利勁 30mg 至少4次沒有任何副作用？",
    "_havebettersex_6": "7. 您暴露在輻射中的時間是否超過 2 小時？",
    "_havebettersex_7": "8. 您出現任何症狀的時間是否已超過 6 個月？",
    "_havebettersex_8": "9. 您是否有低血壓（低於 90/50）？ ",
    "_havebettersex_9": "10. 當您從臥姿起身時，是否有暈厥或頭暈的傾向？",
    "_havebettersex_10": "11. 精神健康狀況，例如憂鬱症、躁狂症、躁郁症或精神分裂症？",
    "_havebettersex_11": "12. 您是否曾有下列問題？\n"
                        "心臟病\n"
                        "肝病\n"
                        "腎臟疾病\n"
                        "抽搐或癲癇\n",

    # Emergency Contraception Questions
    "_emergency-contraception_0": "1. 您是否瞭解您必須在未採取安全措施的性行為發生後 72 小時（3 天）內接受此治療？",
    "_emergency-contraception_1": "2. 您是否打算在同一個月經週期中多次使用此藥，或您是否可能懷孕？",
    "_emergency-contraception_2": "3. 您是否知道，如果您在上次月經來潮後 (3 天前) 有過無保護措施的性行為，則不應接受此治療？",
    "_emergency-contraception_3": "4. 如果您的末次月經延遲、量少/短或有任何異常，您是否打算接受此治療？",
    "_emergency-contraception_4": "5. 您是否已懷孕或正在哺乳，或打算在服藥期間懷孕或開始哺乳？",
    "_emergency-contraception_5": "6. 您是否對左炔诺孕酮或其任何成分過敏（包括您過去可能使用過的其他荷爾蒙避孕藥）？",
    "_emergency-contraception_6": "7. 您是否被診斷出患有下列疾病？\n"
                        "注意事項：\n"
                        "曾有子宮外孕\n"
                        "嚴重的腸道吸收不良疾病，如克隆氏症、潰瘍性結腸炎或其他相關疾病\n"
                        "活動性滋養細胞疾病\n"
                        "急性卟啉症\n"
                        "輸精管切除術\n"
                        "盆腔炎\n"
                        "肝臟問題\n"
                        "半乳糖不耐症、Lapp 乳糖酶缺乏症或葡萄糖-半乳糖吸收不良\n",
    "_emergency-contraception_7": "8. 您能確認您的 BMI 不超過 26 且您的體重不超過 70 公斤嗎？",
    "_emergency-contraception_8": "9. 請確認您沒有服用下列任何藥物\n"
                        "注意事項：\n"
                        "利福平和利福布汀\n"
                        "香豆素或苯二酮\n"
                        "聖約翰草\n"
                        "抗癲癇藥，如 Carbamazepine、Eslicarbazepine、Oxcarbazepine、Phenobarbital、Phenytoin、Primidone、Rufinamide、 托吡酯和苯妥英。魯非那胺、托吡酯等。\n"
                        "抗病毒藥物，如 Efavirenz、Nevirapine、Ritonavir 等。\n"
                        "阿瑞匹坦\n"
                        "波生坦\n"
                        "細胞毒性藥物，例如 Ritonitinib、Vemurafenib、Dabrafenib\n"
                        "環孢菌素\n"
                        "福沙匹坦\n"
                        "格列喹酮\n"
                        "莫達非尼\n"
                        "西地那非\n"
                        "烏利司他\n",
    "_emergency-contraception_9": "10. 協議與確認\n"
                        "請確認您知道藥效會在前三天內大幅降低，而且您同意在性交後 72 小時內（最好在 12 小時內）服藥。\n"
                        "我不同意\n",
    "_emergency-contraception_10": "11. 重要資訊\n"
                        "此藥應儘快服用，最好在無防護措施的性行為發生後 12 小時內服用，最遲不得超過 72 小時（3 天）。此藥並非 100%有效，不應延遲服用。此藥並非 100%有效，應儘快服用，不可延遲。\n"
                        "如果您在服藥後 3 小時內嘔吐，應立即服用另一劑。\n"
                        "緊急避孕藥可能會中斷您的月經週期，這表示您的下次月經可能會提早或延遲\n"
                        "您需要在下次月經來臨前使用屏障避孕法來避孕。\n"
                        "如果您已經使用常規的荷爾蒙避孕法，您可以照常服用。\n"
                        "如果您出現任何異常的下腹疼痛，您需要立即就醫。\n"
                        "緊急避孕並不保護您免於性傳播疾病的風險。如果您有骨盆疼痛、陰道分泌物異常、發燒或任何其他相關問題，您必須尋求醫療建議。\n"
                        "如果您下次月經來得異常少、異常多、異常短或異常不規律，或是您擔心月經不正常，您必須在 3-4 週內去看您的 GP。如果您對自己是否有月經有任何懷疑，您應該在無保護措施的性行為後至少 3 週做懷孕檢測。如果您的下次月經遲來超過 5 天，或異常的量少或量多，您應該立即接受懷孕檢測並與您的 GP 聯絡。\n"
                        "緊急避孕不能取代長期避孕。請諮詢您的家庭醫師，討論可靠的長期避孕方法。\n",
    # Lose Weight Questions
    "_lose-weight_0": "1. 您的身體質量指數 (BMI) 是否超過 28？",
    "_lose-weight_1": "2. 您是否患有下列疾病：糖尿病、心臟病、高血壓或高膽固醇？",
    "_lose-weight_2": "3. 您對 Orlistat 過敏嗎？",
    "_lose-weight_3": "4. 您是否已懷孕、正在哺乳、或計畫在治療期間懷孕或開始哺乳？",
    "_lose-weight_4": "5. 您是否被診斷出患有以下任何一種疾病？\n"
                        "注意事項：\n"
                        "慢性吸收不良症候群（食物吸收問題）\n"
                        "肝臟問題\n"
                        "腎臟問題\n"
                        "甲狀腺問題\n"
                        "膽囊切除術 (膽囊切除)\n"
                        "膽汁淤積症（膽汁從肝臟流出受阻的情況）\n"
                        "任何可能需要立即住院的嚴重醫療狀況\n",
    "_lose-weight_5": "6. 您是否正在服用治療高膽固醇、糖尿病或高血壓的藥物？",
    "_lose-weight_6": "7. 您是否使用口服避孕藥？",
    "_lose-weight_7": "8. 您是否正在服用下列藥物？\n"
                        "注意事項：\n"
                        "其他抗肥胖症藥物\n"
                        "愛滋病藥物\n"
                        "脂溶性維生素\n"
                        "口服抗凝血劑用於稀釋血液，例如華法林（「血液稀釋丸」）\n"
                        "環孢素 (Cyclosporine)，用於器官移植後或治療嚴重的類風濕關節炎和某些嚴重的皮膚病\n"
                        "甲狀腺藥物 (Levothyroxine)\n"
                        "碘（碘鹽）\n"
                        "胺碘酮（Amiodarone），用於治療心律問題\n"
                        "阿卡波糖，一種用於治療 2 型糖尿病的抗糖尿病藥物\n"
                        "抗驚厥/抗癲癇藥物\n"
                        "抗精神病藥物，包括鋰\n"
                        "苯二氮卓（苯並二氮卓），包括地西泮\n",
    "_lose-weight_8": "9. 重要資訊\n"
                        "一旦您的 BMI 低於 28，您就必須停止治療。\n"
                        "如果您在開始治療的 3 個月內體重沒有減輕，就不能繼續治療。\n"
                        "建議您在服用奧利司他（Orlistat）之前或之後（如睡前）至少2小時服用含有維生素D、E、K和β-胡蘿蔔素的複合維生素。\n"
                        "在治療的同時，還應該保持均衡、熱量可控的飲食，約 30% 的熱量應來自脂肪。此外，也建議多吃水果和蔬菜。\n",
    "_lose-weight_9": "10. 協議與確認\n"
                        "透過確認，您聲明您已獲得相關醫療狀況的專業診斷，且狀況穩定，並證明所提供的資訊正確無誤。\n"
                        "我同意\n",

    "_age": "體重 (kg)",
    "_weight": "年齡",


    # Regrow Hair Questions
    "_regrowhair_0": "1. 您有脫髮問題嗎？",
    "_regrowhair_1": "2. 任何藥物、飲食問題或疾病是否可能導致您脫髮？",
    "_regrowhair_2": "3. 您有健康的頭皮嗎？\n"
                        "注意事項：\n"
                        "頭皮沒有發炎\n"
                        "頭皮無紅腫\n"
                        "頭皮上沒有舊敷料\n"
                        "頭皮上沒有剃鬚痕跡\n",
    "_regrowhair_3": "4. 您是否有大片脫髮、頭皮痕癢或疼痛的現象？",
    "_regrowhair_4": "5. 您是否突然或完全脫髮？",
    "_regrowhair_5": "6. 您的脫髮是否僅限於太陽穴部位？",
    "_regrowhair_6": "7. 您有憂鬱症或其他心理健康問題的病史嗎？",
    "_regrowhair_7": "8. 您是否曾被斷出患有下列疾病？\n"
                        "注意事項：\n"
                        "心臟病（包括胸痛、心絞痛、心臟病發作或任何心血管事件史）\n"
                        "高血壓\n"
                        "男性乳癌\n"
                        "急性卟啉症（一種影響血紅蛋白的罕見遺傳病）\n"
                        "前列腺問題 (前列腺腫大、前列腺腺癌等)\n",
    "_regrowhair_8": "9. 您是否正在服用下列藥物？\n"
                        "注意事項：\n"
                        "地塞米松（治療牛皮癬）\n"
                        "維他命 A 酸 (針對暗瘡或其他皮膚問題)\n"
                        "皮質類固醇（如氫化可的松或二丙酸倍氟米松）\n"
                        "月桂醇、鬍蠟或髮膠的常見成分\n",

    # Have Longer Sex Questions
    "_havelongersex_0": "1. 您吸煙或喝酒嗎？",
    "_havelongersex_1": "2. 您之前是否至少服用過四次 Viagra (Sildenafil)、Levitra (Vardenafil)、Nipatra、Spedra 或 Cialis (Tadalafil) 而沒有任何副作用？",
    "_havelongersex_2": "3. 您是否曾有勃起或維持勃起的困難？",
    "_havelongersex_3": "4. 您是否有高血壓（160/90 或更高）或目前正在接受高血壓治療？",
    "_havelongersex_4": "5. 您是否有低血壓（低於 90/50）？",
    "_havelongersex_5": "6. 是否有人建議您避免劇烈運動？",
    "_havelongersex_6": "7. 您有憂鬱症或其他心理健康問題的病史嗎？",
    "_havelongersex_7": "8. 您是否曾被診斷出患有下列疾病？\n"
                        "心臟問題，例如心絞痛、胸痛或心臟病發作（心肌梗塞）\n"
                        "中風\n"
                        "腎臟問題\n"
                        "肝臟問題\n"
                        "血友病或鐮狀細胞貧血等血液疾病\n"
                        "血液循環不良導致視力衰退\n",
    "_havelongersex_8": "9. 協議與確認\n"
                        "確認即表示您聲明：\n"
                        "您對勃起功能障礙藥物沒有已知的過敏反應。\n"
                        "您沒有可能在治療期間造成風險的潛在健康問題。\n"
                        "您同意在治療期間告知您的 GP 任何副作用或健康變化。\n"
                        "我同意:\n",
}

async def send_telegram_message(bot_token, channel_username, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=channel_username, text=message)
    print("Message sent successfully to Telegram!")

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to fetch the latest order
    order_query = """
        SELECT * FROM custom_orders
        ORDER BY created_at DESC
        LIMIT 1;
    """
    cursor.execute(order_query)
    order = cursor.fetchone()

    if order:
        # Prepare the message for Telegram
        message = f"Latest Order Details:\n"
        message += f"Order ID: {order['order_id']}\n"
        message += f"Customer Name: {order['customer_name']}\n"
        message += f"Email: {order['email']}\n"
        message += f"Total: {order['total']}\n"
        message += f"Billing Name: {order['billing_name']}\n"
        message += f"Billing Address: {order['billing_address']}\n"
        message += f"Billing Email: {order['billing_email']}\n"
        message += f"Billing Phone: {order['billing_phone']}\n"
        message += f"Shipping Name: {order['shipping_name']}\n"
        message += f"Shipping Address: {order['shipping_address']}\n"
        message += f"Shipping Country: {order['shipping_country']}\n"
        message += f"Shipping Postcode: {order['shipping_postcode']}\n"

        # Deserialize metadata
        metadata = order['metadata']
        if metadata:
            try:
                parsed_metadata = phpserialize.loads(metadata.encode('utf-8'), decode_strings=True)
                message += "\n問卷:\n"
                for key, value in parsed_metadata.items():
                    question = questions_map.get(key, key)  # Use the mapped question or default to the key
                    if value and str(value).strip():
                        message += f"{question}: {value}\n"
            except Exception as e:
                message += f"Error parsing metadata: {e}\n"
        else:
            message += "No additional metadata found.\n"

        # Query to fetch specific meta_value from wp_postmeta
        postmeta_query = """
            SELECT pm.meta_value
            FROM wp_postmeta pm
            JOIN custom_orders co ON pm.post_id = co.id_card_link
            WHERE pm.meta_key = '_wp_attached_file'
            ORDER BY pm.meta_id DESC
            LIMIT 1;

        """
        cursor.execute(postmeta_query)
        postmeta = cursor.fetchone()

        if postmeta:
            base_url = "https://www.247asap.com/wp-content/uploads/"
            full_url = base_url + postmeta['meta_value']
            message += f"\nID Card URL:\n{full_url}\n"
        else:
            message += "No meta value found in the wp_postmeta table.\n"

        # Send the message to Telegram
        asyncio.run(send_telegram_message(BOT_TOKEN, CHANNEL_USERNAME, message))
    else:
        print("No orders found in the custom_orders table.")

except mysql.connector.Error as e:
    print(f"Database error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed.")