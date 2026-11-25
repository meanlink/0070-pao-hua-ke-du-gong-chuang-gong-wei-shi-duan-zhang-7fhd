def seed(cx):
    cx.execute("""
      INSERT INTO machines VALUES ('SAW-01','东台推锯','A 切割区'),('SAND-02','长带砂磨机','B 整形区'),
      ('LATHE-03','短床车床','C 车削区') ON CONFLICT DO NOTHING;
      INSERT INTO shop_hours VALUES ('SAW-01','2026-11-20',540,900),('SAND-02','2026-11-20',540,900),
      ('LATHE-03','2026-11-20',600,840) ON CONFLICT DO NOTHING;
      INSERT INTO maintenance_blocks VALUES
      ('SVC-20','SAW-01','2026-11-20','集尘箱维保',630,685),
      ('SVC-21','SAW-01','2026-11-20','防护检查补时',675,690),
      ('SVC-22','LATHE-03','2026-11-20','全日工位整改',600,840)
      ON CONFLICT DO NOTHING;
      INSERT INTO bench_sessions VALUES
      ('JOB-201','SAW-01','薄板架组','2026-11-20',560,660,'counted','reviewer@demo.local'),
      ('JOB-202','SAW-01','共创课一组','2026-11-20',590,710,'counted','reviewer@demo.local'),
      ('JOB-203','SAW-01','试开机','2026-11-20',640,670,'logged',null),
      ('JOB-204','SAND-02','展架饰面组','2026-11-20',550,625,'counted','reviewer@demo.local'),
      ('JOB-205','SAND-02','边框整理组','2026-11-20',610,655,'counted','reviewer@demo.local')
      ON CONFLICT DO NOTHING;
    """)
