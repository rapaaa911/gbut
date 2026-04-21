import requests, os, json, binascii, time, urllib3, base64, datetime, re, socket, ssl, asyncio, aiohttp, random, traceback
from protobuf_decoder.protobuf_decoder import Parser
from xDL import *
from autoup import *
from datetime import datetime
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIG ---
CLIENT_BP_URL = "https://clientbp.ggblueshark.com"
login_url, ob, version = AuToUpDaTE()
online_writer = None
# Set bd = id sesuai request
REGION_MODE = "BD"

# --- HELPER FUNCTIONS (Biar gak NameError) ---
async def DecodE_HeX(ts):
    # Simulasi decode timestamp ke hex, pastikan fungsi aslinya ada di xDL
    # Kalau xDL gak punya, ini fallback-nya
    return hex(int(ts))[2:]

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    
    # Header logic berdasarkan panjang UID
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# --- IN-GAME PACKETS ---
async def send_move_forward(key, iv, region):
    fields = {1: 15000, 2: 15000, 3: 1}
    pkt_type = '0519' if region.lower() == "bd" else '0514'
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), pkt_type, key, iv)

async def use_homer_skill(key, iv, region):
    # Homer ID: 102000037
    fields = {1: 102000037, 2: 1}
    pkt_type = '0519' if region.lower() == "bd" else '0514'
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), pkt_type, key, iv)

# --- AUTO CS LOOP ---
async def start_the_grind(key, iv, region):
    print(f"🔥 [AUTO] Mode CS Aktif (Region: {region})")
    while True:
        try:
            # 1. Open Squad
            p1 = await OpEnSq(key, iv, region)
            if online_writer:
                online_writer.write(p1)
                await online_writer.drain()
            await asyncio.sleep(2)

            # 2. Start
            p2 = await start_auto_packet(key, iv, region)
            if online_writer:
                online_writer.write(p2)
                await online_writer.drain()
            
            # 3. In-Game Maju + Homer
            match_end = time.time() + 180
            while time.time() < match_end:
                move = await send_move_forward(key, iv, region)
                if online_writer:
                    online_writer.write(move)
                    await online_writer.drain()
                
                if int(time.time()) % 6 == 0:
                    homer = await use_homer_skill(key, iv, region)
                    if online_writer:
                        online_writer.write(homer)
                        await online_writer.drain()
                await asyncio.sleep(1.5)

            # 4. Selesai
            p3 = await leave_squad_packet(key, iv, region)
            if online_writer:
                online_writer.write(p3)
                await online_writer.drain()
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Loop Error: {e}")
            await asyncio.sleep(5)

# --- MAIN PROCESS ---
async def MaiiiinE():
    global online_writer
    with open("bot.txt", "r") as f:
        creds = json.load(f)
    uid, password = list(creds.items())[0]

    async with aiohttp.ClientSession() as session:
        # Get Access Token
        url_auth = "https://100067.connect.garena.com/oauth/guest/token/grant"
        auth_data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
        async with session.post(url_auth, data=auth_data) as resp:
            token_json = await resp.json()
            open_id, access_token = token_json.get("open_id"), token_json.get("access_token")

        # Full Major Login
        payload = await EncRypTMajoRLoGin(open_id, access_token)
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        async with session.post(f"{login_url}MajorLogin", data=payload, headers=Hr, ssl=ssl_ctx) as resp:
            auth_res = MajoRLoGinrEs_pb2.MajorLoginRes()
            auth_res.ParseFromString(await resp.read())

        # Get Ports pake CLIENTBP
        Hr['Authorization'] = f"Bearer {auth_res.token}"
        async with session.post(f"{CLIENT_BP_URL}/GetLoginData", data=payload, headers=Hr, ssl=ssl_ctx) as resp:
            ports_res = PorTs_pb2.GetLoginData()
            ports_res.ParseFromString(await resp.read())

    online_ip, online_port = ports_res.Online_IP_Port.split(":")
    auth_token = await xAuThSTarTuP(int(auth_res.account_uid), auth_res.token, int(auth_res.timestamp), auth_res.key, auth_res.iv)

    # TCP Connect
    reader, writer = await asyncio.open_connection(online_ip, int(online_port))
    online_writer = writer
    writer.write(bytes.fromhex(auth_token))
    await writer.drain()
    
    print(f"✅ Login Berhasil! Server: {REGION_MODE.upper()}")
    await asyncio.sleep(2)

    # LANGSUNG GRIND
    await start_the_grind(auth_res.key, auth_res.iv, REGION_MODE)

if __name__ == '__main__':
    asyncio.run(MaiiiinE())
