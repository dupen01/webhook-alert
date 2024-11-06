import time 
import httpx
from fastapi import APIRouter

router = APIRouter()



def get_latency(url):
    start_time = time.time() * 1000
    try:
        httpx.get(url=url, timeout=3)
        end_time = time.time() * 1000
        return int(end_time - start_time)
    except httpx.TimeoutException:
        return 'timeout'
    

@router.get('/ltc')
async def ltc():
    urls = {
        'baidu': 'https://www.baidu.com',
        'jd': 'https://www.jd.com',
        'douyin': 'https://www.douyin.com',
        'github': 'https://www.github.com',
        'google': 'https://www.google.com',
    }

    res = {}
    for k, v in urls.items():
        ltc = get_latency(v)
        res.setdefault(k, ltc)

    return res

