import requests, os, json, binascii, time, urllib3, base64, datetime, re, socket, ssl, asyncio, aiohttp, random, traceback
from protobuf_decoder.protobuf_decoder import Parser
from xDL import *
from autoup import *
from datetime import datetime
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- GLOBAL CONFIG ---
online_writer = None
login_url, ob, version = AuToUpDaTE()
# URL sesuai request lu
CLIENT_BP_URL = "https://clientbp.ggblueshark.com"

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

# --- PACKET GENERATORS ---
async def send_move_forward(key, iv, region):
    fields = {1: 15000, 2: 15000, 3: 1}
    pkt_type = '0514' if region.lower() == "ind" else '0515'
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), pkt_type, key, iv)

async def use_homer_skill(key, iv, region):
    # Homer Item ID: 102000037
    fields = {1: 102000037, 2: 1}
    pkt_type = '0514' if region.lower() == "ind" else '0515'
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), pkt_type, key, iv)

async def SEndPacKeT(OnLinE, PacKeT):
    if OnLinE:
        OnLinE.write(PacKeT)
        await OnLinE.drain()

# --- ENCRYPTION LOGIC ---
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    return cipher.encrypt(padded_message)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = version
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

# --- GAMEPLAY LOOP ---
async def start_the_grind(key, iv, region):
    print("🚀 [SYSTEM] Auto Clash Squad Mode: ACTIVE")
    while True:
        try:
            # 1. Bikin Lobby
            p1 = await OpEnSq(key, iv, region)
            await SEndPacKeT(online_writer, p1)
            await asyncio.sleep(2)

            # 2. Start CS
            p2 = await start_auto_packet(key, iv, region)
            await SEndPacKeT(online_writer, p2)
            
            # 3. Match Simulation (Maju + Homer)
            match_timeout = time.time() + 180
            while time.time() < match_timeout:
                move = await send_move_forward(key, iv, region)
                await SEndPacKeT(online_writer, move)
                
                if int(time.time()) % 5 == 0:
                    homer = await use_homer_skill(key, iv, region)
                    await SEndPacKeT(online_writer, homer)
                await asyncio.sleep(1.3)

            # 4. Selesai Match
            p3 = await leave_squad_packet(key, iv, region)
            await SEndPacKeT(online_writer, p3)
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)

# --- MAIN ENGINE ---
async def MaiiiinE():
    global online_writer
    if not os.path.exists("bot.txt"): return
    
    with open("bot.txt", "r") as f:
        creds = json.load(f)
    uid, password = list(creds.items())[0]

    # Step 1: Oauth Access
    url_auth = "https://100067.connect.garena.com/oauth/guest/token/grant"
    auth_data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url_auth, data=auth_data) as resp:
            token_json = await resp.json()
            open_id = token_json.get("open_id")
            access_token = token_json.get("access_token")

        if not open_id: return

        # Step 2: Major Login
        payload = await EncRypTMajoRLoGin(open_id, access_token)
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        
        async with session.post(f"{login_url}MajorLogin", data=payload, headers=Hr, ssl=ssl_ctx) as resp:
            auth_res = MajoRLoGinrEs_pb2.MajorLoginRes()
            auth_res.ParseFromString(await resp.read())

        # Step 3: Get Login Data (FIX PAKE CLIENTBP)
        Hr['Authorization'] = f"Bearer {auth_res.token}"
        async with session.post(f"{CLIENT_BP_URL}/GetLoginData", data=payload, headers=Hr, ssl=ssl_ctx) as resp:
            ports_res = PorTs_pb2.GetLoginData()
            ports_res.ParseFromString(await resp.read())

    # Connection
    online_ip, online_port = ports_res.Online_IP_Port.split(":")
    auth_token = await xAuThSTarTuP(int(auth_res.account_uid), auth_res.token, int(auth_res.timestamp), auth_res.key, auth_res.iv)

    # TCP Online Only
    reader, writer = await asyncio.open_connection(online_ip, int(online_port))
    online_writer = writer
    writer.write(bytes.fromhex(auth_token))
    await writer.drain()
    
    print(f"✅ Login Success: {auth_res.account_uid}")
    await asyncio.sleep(2)

    # Start Loop
    await start_the_grind(auth_res.key, auth_res.iv, getattr(auth_res, 'region', 'ID'))

if __name__ == '__main__':
    asyncio.run(MaiiiinE())
