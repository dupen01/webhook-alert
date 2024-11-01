from fastapi import FastAPI, Request
import uvicorn
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import tomllib
import httpx


app = FastAPI()


@app.get('/')
def hello():
    return "Hello Alert!2"


@app.post('/test', status_code=200)
async def test(request: Request):
    # 读取请求体内容
    body = await request.json()
    # 打印请求体内容
    print(datetime.now(), json.dumps(body))
    """
    {
    'receiver': 'test', 
    'status': 'firing', 
    'alerts': 
        [{
        'status': 'firing', 
        'labels': {
            'alertname': 'TestAlert', 
            'instance': 'Grafana'
            }, 
        'annotations': {
            'summary': 'Notification test'
            }, 
        'startsAt': '2024-10-30T03:02:57.378011729Z', 
        'endsAt': '0001-01-01T00:00:00Z', 
        'generatorURL': '', 
        'fingerprint': '57c6d9296de2ad39', 
        'silenceURL': 'http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana', 
        'dashboardURL': '', 
        'panelURL': '', 
        'values': None, 
        'valueString': "[ metric='foo' labels={instance=bar} value=10 ]"}], 
        'groupLabels': {
            'alertname': 'TestAlert', 
            'instance': 'Grafana'
            }, 
        'commonLabels': {
            'alertname': 'TestAlert', 
            'instance': 'Grafana'
            }, 
        'commonAnnotations': {
            'summary': 'Notification test'
            }, 
        'externalURL': 'http://localhost:3000/', 
        'version': '1', 
        'groupKey': 'test-57c6d9296de2ad39-1730257377', 
        'truncatedAlerts': 0, 
        'orgId': 1, 
        'title': '[FIRING:1] TestAlert Grafana ', 
        'state': 'alerting', 
        'message': '**Firing**\n\nValue: [no value]\nLabels:\n - alertname = TestAlert\n - instance = Grafana\nAnnotations:\n - summary = Notification test\nSilence: http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana\n'
        }
    """
    return {'code': 200, 'msg': 'ok'}


@app.post('/grafana/dingtalk', status_code=204)
async def test(request: Request):
    # 读取请求体内容
    received_data = await request.json()

    # 获取配置
    cfg = tomllib.load(open('app.toml', 'rb'))
    at_mobiles = cfg['grafana-dingtalk']['at_mobiles']
    token = cfg['grafana-dingtalk']['token']
    grafana_tz = cfg['grafana']['timezone']

    for alert in received_data['alerts']:
        annotations = alert['annotations']
        labels = alert['labels']
        status = alert['status']
        startsAt = alert['startsAt'][:19]
        values = alert['values']

        summary = annotations['summary']
        description = annotations['description'] if 'annotations' in annotations else ''

        start_time = datetime.strptime(startsAt, "%Y-%m-%dT%H:%M:%S") \
            .replace(tzinfo=ZoneInfo(grafana_tz)) \
            .astimezone(ZoneInfo('Asia/Shanghai')) \
            .strftime("%Y-%m-%d %H:%M:%S")

        instance = labels['instance']
        if 'at' in labels:
            atMobiles = [x.strip() for x in labels['at'].split(',')]
        else:
            atMobiles = at_mobiles
        
        level = labels['level'] if 'level' in labels else '一般'

        if status == 'resolved':
            color = 'info'
            status_ch = '已解决'
        elif status == 'firing':
            color = 'red'
            status_ch = '告警'

        dingtalk_msg = {}
        at = {}
        at.setdefault('atMobiles', atMobiles)
        markdown = {}
        md_text = f"""### {summary}
**告警级别**: {level}
**触发时间**: {start_time}
**系统/服务**: {instance}
**告警详情**: 
- **当前状态**: <font color={color}>{status_ch}</font>
- **告警描述**: {description}
- **触发值**: {values}
**告警来源**: Grafana alert
"""
        print(md_text)

        markdown.setdefault('text', md_text)

        dingtalk_msg.setdefault('at', at)
        dingtalk_msg.setdefault('msgtype', 'markdown')
        dingtalk_msg.setdefault('markdown', markdown)
        
        # print(json.dumps(dingtalk_msg))
        
        # send to dingtalk
        dingtalk_webhook_url = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
        res = httpx.post(dingtalk_webhook_url, data=dingtalk_msg)

        if res.status_code == 200:
            print("Success!")
        else:
            print(f"An error occurred: {res.status_code}")
        
        print(res.text)
        
    return None


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
