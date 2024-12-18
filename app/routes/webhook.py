from fastapi import Request, APIRouter
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import tomllib
import httpx
import logging
from typing import Literal
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


class AlertMsg(BaseModel):
    receiver: str
    status: str
    alerts: list[dict]


@router.post('/test2')
async def test2(alert: AlertMsg) -> None:
    logger.info(alert)


@router.post('/test', status_code=200)
async def get_grafana_alert_msg_template(request: Request) -> None:
    # 读取请求体内容
    body = await request.json()
    # 打印请求体内容
    logger.info(json.dumps(body))
"""
    {
  "receiver": "test",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "TestAlert",
        "instance": "Grafana"
      },
      "annotations": {
        "summary": "Notification test"
      },
      "startsAt": "2024-11-27T15:39:47.65149303Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "",
      "fingerprint": "57c6d9296de2ad39",
      "silenceURL": "http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana",
      "dashboardURL": "",
      "panelURL": "",
      "values": null,
      "valueString": "[ metric='foo' labels={instance=bar} value=10 ]"
    }
  ],
  "groupLabels": {
    "alertname": "TestAlert",
    "instance": "Grafana"
  },
  "commonLabels": {
    "alertname": "TestAlert",
    "instance": "Grafana"
  },
  "commonAnnotations": {
    "summary": "Notification test"
  },
  "externalURL": "http://localhost:3000/",
  "version": "1",
  "groupKey": "test-57c6d9296de2ad39-1732721987",
  "truncatedAlerts": 0,
  "orgId": 1,
  "title": "[FIRING:1] TestAlert Grafana ",
  "state": "alerting",
  "message": "**Firing**\n\nValue: [no value]\nLabels:\n - alertname = TestAlert\n - instance = Grafana\nAnnotations:\n - summary = Notification test\nSilence: http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DTestAlert&matcher=instance%3DGrafana\n"
}
"""


@router.post('/grafana/dingtalk', status_code=204)
async def send_to_dingtalk(alert_msg: AlertMsg, request: Request) -> None:
    """
    {
  "receiver": "tets",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "StarRocks Connections",
        "at": "17712345678,18812345678",
        "grafana_folder": "测试",
        "group": "fe",
        "instance": "172.20.3.24:8030",
        "job": "StarRocks",
        "告警级别": "一般"
      },
      "annotations": {
        "description": "超过1",
        "summary": "连接数过多"
      },
      "startsAt": "2024-11-27T15:45:30Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://localhost:3000/alerting/grafana/be2cl3h0jeqdca/view?orgId=1",
      "fingerprint": "d947522847756ba9",
      "silenceURL": "http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DStarRocks+Connections&matcher=at%3D17712345678%2C18812345678&matcher=grafana_folder%3D%E6%B5%8B%E8%AF%95&matcher=group%3Dfe&matcher=instance%3D172.20.3.24%3A8030&matcher=job%3DStarRocks&matcher=%E5%91%8A%E8%AD%A6%E7%BA%A7%E5%88%AB%3D%E4%B8%80%E8%88%AC&orgId=1",
      "dashboardURL": "http://localhost:3000/d/YJZ7BBj4z?orgId=1",
      "panelURL": "http://localhost:3000/d/YJZ7BBj4z?orgId=1&viewPanel=34",
      "values": {
        "current_connections_num": 2,
        "触发值": 1
      },
      "valueString": "[ var='current_connections_num' labels={__name__=starrocks_fe_connection_total, group=fe, instance=172.20.3.24:8030, job=StarRocks} value=2 ], [ var='触发值' labels={__name__=starrocks_fe_connection_total, group=fe, instance=172.20.3.24:8030, job=StarRocks} value=1 ]"
    }
  ],
  "groupLabels": {
    "alertname": "StarRocks Connections",
    "grafana_folder": "测试"
  },
  "commonLabels": {
    "alertname": "StarRocks Connections",
    "at": "17712345678,18812345678",
    "grafana_folder": "测试",
    "group": "fe",
    "instance": "172.20.3.24:8030",
    "job": "StarRocks",
    "告警级别": "一般"
  },
  "commonAnnotations": {
    "description": "超过1",
    "summary": "连接数过多"
  },
  "externalURL": "http://localhost:3000/",
  "version": "1",
  "groupKey": "{}/{__grafana_autogenerated__=\"true\"}/{__grafana_receiver__=\"tets\"}:{alertname=\"StarRocks Connections\", grafana_folder=\"测试\"}",
  "truncatedAlerts": 0,
  "orgId": 1,
  "title": "[FIRING:1] StarRocks Connections 测试 (17712345678,18812345678 fe 172.20.3.24:8030 StarRocks 一般)",
  "state": "alerting",
  "message": "**Firing**\n\nValue: current_connections_num=2, 触发值=1\nLabels:\n - alertname = StarRocks Connections\n - at = 17712345678,18812345678\n - grafana_folder = 测试\n - group = fe\n - instance = 172.20.3.24:8030\n - job = StarRocks\n - 告警级别 = 一般\nAnnotations:\n - description = 超过1\n - summary = 连接数过多\nSource: http://localhost:3000/alerting/grafana/be2cl3h0jeqdca/view?orgId=1\nSilence: http://localhost:3000/alerting/silence/new?alertmanager=grafana&matcher=alertname%3DStarRocks+Connections&matcher=at%3D17712345678%2C18812345678&matcher=grafana_folder%3D%E6%B5%8B%E8%AF%95&matcher=group%3Dfe&matcher=instance%3D172.20.3.24%3A8030&matcher=job%3DStarRocks&matcher=%E5%91%8A%E8%AD%A6%E7%BA%A7%E5%88%AB%3D%E4%B8%80%E8%88%AC&orgId=1\nDashboard: http://localhost:3000/d/YJZ7BBj4z?orgId=1\nPanel: http://localhost:3000/d/YJZ7BBj4z?orgId=1&viewPanel=34\n"
}
"""
    # 读取请求体内容
    received_data = await request.json()
    logger.info(json.dumps(received_data))
    
    # 获取配置
    cfg = tomllib.load(open('app.toml', 'rb'))
    at_mobiles = cfg['grafana-dingtalk']['at_mobiles']
    token = cfg['grafana-dingtalk']['token']
    grafana_tz = cfg['grafana']['timezone']

    for alert in alert_msg.alerts:
        annotations = alert['annotations']
        labels: dict = alert['labels']
        status = alert['status']
        startsAt = alert['startsAt'][:19]
        values = alert['values']

        summary = annotations['summary']
        description = annotations['description'] if 'annotations' in annotations else ''

        start_time = datetime.strptime(startsAt, "%Y-%m-%dT%H:%M:%S") \
            .replace(tzinfo=ZoneInfo(grafana_tz)) \
            .astimezone(ZoneInfo('Asia/Shanghai')) \
            .strftime("%Y-%m-%d %H:%M:%S")

        instance = None
        atMobiles = at_mobiles
        alert_rule_name = ''
        user_labels = {}
        job = None
        for k, v in labels.items():
            match k:
                case 'instance':
                    instance = v
                case 'at':
                    atMobiles = [x.strip() for x in v.split(',')]
                case 'alertname' | 'rulename':
                    alert_rule_name = v 
                case 'grafana_folder':
                    pass
                case 'job':
                    job = v
                case _:
                    user_labels.setdefault(k, v)

        color: Literal['info', 'red'] = 'info'
        status_ch = ''
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
        md_text = f"""### {summary} <font color={color}>【{status_ch}】</font>
**告警规则名称**: {alert_rule_name}
**来源(job)**: {job}
**系统/服务**: {instance}
**触发时间**: {start_time}
**告警详情**: 
- **告警描述**: {description}
- **触发值**: {values}
- **自定义标签**: {user_labels}
**告警来源**: Grafana alert
"""
        logger.info(md_text)

        markdown.setdefault('text', md_text)

        dingtalk_msg.setdefault('at', at)
        dingtalk_msg.setdefault('msgtype', 'markdown')
        dingtalk_msg.setdefault('markdown', markdown)
        
        # send to dingtalk
        dingtalk_webhook_url = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
        res = httpx.post(dingtalk_webhook_url, data=dingtalk_msg)

        if res.status_code == 200:
            logger.info("Success!")
        else:
            logger.error(f"An error occurred: {res.status_code}")
        
        logger.info(res.text)
