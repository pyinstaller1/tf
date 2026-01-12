import asyncio
import json
from datetime import datetime

# 캐시: 종목별 호가
real_hoga_cache = {}

# 예시 실시간 데이터 수신 콜백
async def receive_real_data(queue):
    while True:
        msg = await queue.get()  # LS에서 보내는 실시간 메시지 가정
        data = json.loads(msg)
        shcode = data["shcode"]
        real_hoga_cache[shcode] = data["outblock"]
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {shcode} 실시간 호가:", data["outblock"])

# 예시 실시간 데이터 생성 (LS 서버 대신)
async def fake_ls_real_sender(queue, shcodes):
    import random, time
    while True:
        for sh in shcodes:
            outblock = {f"ask{i}": random.randint(1000, 1100) for i in range(1, 11)}
            outblock.update({f"bid{i}": random.randint(900, 999) for i in range(1, 11)})
            await queue.put(json.dumps({"shcode": sh, "outblock": outblock}))
        await asyncio.sleep(1)  # LS 실시간 데이터 간격 가정

async def main():
    TARGET_SHCODES = ["005930", "000660"]
    queue = asyncio.Queue()
    await asyncio.gather(
        receive_real_data(queue),
        fake_ls_real_sender(queue, TARGET_SHCODES)
    )

if __name__ == "__main__":
    asyncio.run(main())
