import time 
import httpx
from fastapi import APIRouter, HTTPException
from enum import Enum


class Domain(Enum):
    baidu = 'baidu'
    jd = 'jd'
    taobao = 'taobao'
    github = 'github'
    google = 'google'
    x = 'x'


router = APIRouter()


def __get_latency(url) -> int:
    start_time = time.time() * 1000
    with httpx.Client(verify=False, timeout=2.) as client:
        client.get(url=url)
    end_time = time.time() * 1000
    return int(end_time - start_time)
    

@router.get('/ltc/{domain}')
async def get_latency(domain: str) -> dict[str, int]:
    """获取各网址的请求延时
    """
    url = f"https://www.{domain}.com"
    if domain in Domain:
        try:
            ltc = __get_latency(url)
            return {
                domain: ltc
            }
        except httpx.TimeoutException:
            raise HTTPException(status_code=408)
    else:
        raise HTTPException(status_code=403, detail='参数非法')

