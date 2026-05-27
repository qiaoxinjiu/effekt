-- 创建文档源表 document_source
-- 用于存储PRD文档（PDF）和飞书链接

BEGIN;

-- 创建文档源表
CREATE TABLE IF NOT EXISTS public.document_source (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    project_id BIGINT NOT NULL,
    type SMALLINT NOT NULL DEFAULT 1,
    source VARCHAR(512) NOT NULL,
    content TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    status SMALLINT NOT NULL DEFAULT 0,
    ai_model VARCHAR(64),
    created_by BIGINT,
    is_delete INTEGER NOT NULL DEFAULT 0,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_document_source_source UNIQUE (source, is_delete)
);

COMMENT ON TABLE public.document_source IS '文档源表 - 存储PRD文档和飞书链接';
COMMENT ON COLUMN public.document_source.id IS '主键ID';
COMMENT ON COLUMN public.document_source.product_id IS '产品ID';
COMMENT ON COLUMN public.document_source.project_id IS '项目ID';
COMMENT ON COLUMN public.document_source.type IS '类型：1-PDF文件，2-飞书链接';
COMMENT ON COLUMN public.document_source.source IS '文件路径或飞书链接';
COMMENT ON COLUMN public.document_source.content IS '解析后的文本内容（缓存）';
COMMENT ON COLUMN public.document_source.version IS '版本号';
COMMENT ON COLUMN public.document_source.status IS '状态：0-待解析，1-已解析，2-已生成用例';
COMMENT ON COLUMN public.document_source.ai_model IS '使用的AI模型';
COMMENT ON COLUMN public.document_source.created_by IS '创建人ID';
COMMENT ON COLUMN public.document_source.is_delete IS '0：未删除；1：已删除';
COMMENT ON COLUMN public.document_source.created_time IS '创建时间';
COMMENT ON COLUMN public.document_source.updated_time IS '更新时间';

-- 为 test_case 表添加字段
ALTER TABLE public.test_case ADD COLUMN IF NOT EXISTS document_id BIGINT;
COMMENT ON COLUMN public.test_case.document_id IS '关联的文档源ID';

ALTER TABLE public.test_case ADD COLUMN IF NOT EXISTS document_version INTEGER;
COMMENT ON COLUMN public.test_case.document_version IS '关联的文档版本';

-- 添加外键约束
ALTER TABLE public.test_case ADD CONSTRAINT fk_test_case_document_id FOREIGN KEY (document_id) REFERENCES public.document_source(id);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_document_source_product_id ON public.document_source(product_id);
CREATE INDEX IF NOT EXISTS idx_document_source_project_id ON public.document_source(project_id);
CREATE INDEX IF NOT EXISTS idx_document_source_type ON public.document_source(type);
CREATE INDEX IF NOT EXISTS idx_document_source_status ON public.document_source(status);
CREATE INDEX IF NOT EXISTS idx_test_case_document_id ON public.test_case(document_id);

COMMIT;
