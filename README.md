# 刨花刻度 · 共创工位时段账

松灯木工共创社由 12 名值班会员维护切割、整形、车削三区。班前用日历排开放时间，团队用纸单记录实际占用，维护人单独登记停机。手工汇总会重复叠加共用流水、重复扣维护分钟、把全天停机设备误写为 0% 使用。台账给排班召集人发布日公报。

| 角色 | 权限 |
|---|---|
| operator | 登记工位使用单、维护窗 |
| reviewer | 复核或冲销使用单、发布公报 |
| viewer | 查看工位平面、维护条、使用单和公报 |

1. 09:00 东台推锯 SAW-01 开放，车削区 10:00 开门。
2. 09:20 薄板架组提交 JOB-201 使用单。
3. 09:50 共创课一组提交 JOB-202，与上笔重叠。
4. 10:30—11:30 合并 SVC-20、SVC-21 两段维护。
5. 10:40 试开机 JOB-203 全段处于停机窗，复核人冲销。
6. 15:10 查验推锯占用 90 分钟 / 可用 300 分钟；LATHE-03 全日不可用，占用率为空。
7. 15:15 签发日公报；worker 汇总各设备分子分母，供排班人查阅。

可用分钟由开放区间减去停机区间并集。确认单合并后与可用区间求交得到占用分钟。分母为 0 时比例为空。发布前签审所有使用单。维护记录不得把已确认使用单整个覆盖。

```sh
cp -n .env.example .env
docker compose up -d --build --wait
docker compose exec backend python -m scripts.seed_demo
docker compose down -v --remove-orphans
```

本机前端端口与 API 端口分别为 FRONTEND_PORT、BACKEND_PORT。DB_PORT 设定 PostgreSQL 映射。演示账号为 operator@demo.local、reviewer@demo.local、viewer@demo.local，默认密码 Demo2026!，DEMO_PASSWORD 可覆盖。SEED_DEMO 控制种子，POSTGRES_PASSWORD、JWT_SECRET 是本机配置。原生 HTML/CSS/ES modules + Nginx、FastAPI、PostgreSQL、Redis 登录限速与 Python worker。后端本地开发安装 backend/requirements.txt，配置容器同名 DATABASE_URL、REDIS_URL、JWT_SECRET，运行 `uvicorn app:app --reload` 和 `python worker.py`。backend/bench 存放时段、维护和公报逻辑，frontend/shop 为工位、流水、公报页面。角色和任务枚举位于 backend/core.py 与 frontend/base.js；工单判定枚举位于 backend/schema.sql、backend/bench/models.py、frontend/shop/time.js。MIT 许可证。

前端地址为 http://127.0.0.1:18464，API 为 http://127.0.0.1:19464，数据库本机映射端口为 17964。
