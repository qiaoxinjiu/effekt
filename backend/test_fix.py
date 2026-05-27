import sys
sys.path.insert(0, '.')
from const import sparkatp_sql_uri
from sqlalchemy import create_engine, text

engine = create_engine(sparkatp_sql_uri)

print('=== 测试前：角色5的project_hook权限 ===')
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT p.code, p.name 
        FROM role_permission rp 
        JOIN permission p ON rp.permission_id = p.id 
        WHERE rp.role_id = 5 AND rp.is_delete = 0 AND p.code LIKE 'project_hook:%'
    """))
    rows = result.fetchall()
    if rows:
        for row in rows:
            print(f'  {row[0]} - {row[1]}')
    else:
        print('  没有project_hook权限')

print('\n=== 手动删除角色5的project_hook权限 ===')
with engine.begin() as conn:
    conn.execute(text("""
        UPDATE role_permission 
        SET is_delete = 1 
        WHERE role_id = 5 AND permission_id IN (
            SELECT id FROM permission WHERE code LIKE 'project_hook:%'
        ) AND is_delete = 0
    """))
    print('删除完成')

print('\n=== 测试后：角色5的project_hook权限 ===')
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT p.code, p.name 
        FROM role_permission rp 
        JOIN permission p ON rp.permission_id = p.id 
        WHERE rp.role_id = 5 AND rp.is_delete = 0 AND p.code LIKE 'project_hook:%'
    """))
    rows = result.fetchall()
    if rows:
        for row in rows:
            print(f'  {row[0]} - {row[1]}')
    else:
        print('  没有project_hook权限（已成功删除）')
