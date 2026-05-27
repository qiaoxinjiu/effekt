-- 为module表添加status字段，默认0（待确认），1（正常），2（弃用）
ALTER TABLE module ADD COLUMN IF NOT EXISTS status INTEGER DEFAULT 0 COMMENT '0：待确认；1：正常；2：弃用';

-- 将历史数据的status设置为1
UPDATE module SET status = 1 WHERE status IS NULL OR status = 0;