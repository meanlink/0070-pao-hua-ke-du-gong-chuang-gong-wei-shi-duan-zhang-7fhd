def maintenance(cx):
    return cx.execute("SELECT * FROM maintenance_blocks ORDER BY service_day,open_minute,code").fetchall()

def insert_block(cx, body):
    return cx.execute("""
        INSERT INTO maintenance_blocks(code,machine,reason,service_day,open_minute,end_minute)
        VALUES (%(code)s,%(machine)s,%(reason)s,%(service_day)s,%(open_minute)s,%(end_minute)s)
        RETURNING *
    """,body.model_dump()).fetchone()
