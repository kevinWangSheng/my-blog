#!/usr/bin/env python3
"""
Notion to Hugo Markdown Sync Script
同步 Notion 数据库内容到 Hugo 博客
"""

import os
import re
from datetime import datetime
from pathlib import Path
from notion_client import Client

# 从环境变量获取配置
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
OUTPUT_DIR = Path("content/posts")

def sanitize_filename(text):
    """将文本转换为安全的文件名"""
    # 移除特殊字符，保留中文、字母、数字、连字符和下划线
    text = re.sub(r'[^\w\s-]', '', text)
    # 将空格替换为连字符
    text = re.sub(r'[\s]+', '-', text)
    # 转换为小写
    return text.lower()

def get_plain_text(rich_text_array):
    """从 Notion rich text 数组中提取纯文本"""
    if not rich_text_array:
        return ""
    return "".join([text.get("plain_text", "") for text in rich_text_array])

def get_property_value(properties, prop_name, default=""):
    """安全地获取 Notion 属性值"""
    if prop_name not in properties:
        return default

    prop = properties[prop_name]
    prop_type = prop.get("type")

    if prop_type == "title":
        return get_plain_text(prop.get("title", []))
    elif prop_type == "rich_text":
        return get_plain_text(prop.get("rich_text", []))
    elif prop_type == "select":
        select = prop.get("select")
        return select.get("name", default) if select else default
    elif prop_type == "multi_select":
        return [item.get("name", "") for item in prop.get("multi_select", [])]
    elif prop_type == "date":
        date = prop.get("date")
        return date.get("start", default) if date else default
    elif prop_type == "checkbox":
        return prop.get("checkbox", False)
    else:
        return default

def page_to_markdown(page, blocks_content):
    """将 Notion 页面转换为 Hugo Markdown 格式"""
    properties = page.get("properties", {})

    # 尝试获取标题（可能的字段名）
    title = (get_property_value(properties, "Title") or
             get_property_value(properties, "Name") or
             get_property_value(properties, "标题") or
             "Untitled")

    # 尝试获取其他常见属性
    date = (get_property_value(properties, "Date") or
            get_property_value(properties, "PublishedAt") or
            get_property_value(properties, "发布日期") or
            datetime.now().strftime("%Y-%m-%d"))

    tags = (get_property_value(properties, "Tags") or
            get_property_value(properties, "标签") or
            [])

    description = (get_property_value(properties, "Description") or
                   get_property_value(properties, "简介") or
                   "")

    # 构建 Hugo Front Matter
    front_matter = f"""---
title: "{title}"
date: {date}
draft: false
"""

    if tags:
        front_matter += f"tags: {tags}\n"

    if description:
        front_matter += f"description: \"{description}\"\n"

    front_matter += "---\n\n"

    return front_matter + blocks_content

def block_to_markdown(block):
    """将 Notion block 转换为 Markdown"""
    block_type = block.get("type")

    if block_type == "paragraph":
        text = get_plain_text(block["paragraph"].get("rich_text", []))
        return text + "\n\n"

    elif block_type == "heading_1":
        text = get_plain_text(block["heading_1"].get("rich_text", []))
        return f"# {text}\n\n"

    elif block_type == "heading_2":
        text = get_plain_text(block["heading_2"].get("rich_text", []))
        return f"## {text}\n\n"

    elif block_type == "heading_3":
        text = get_plain_text(block["heading_3"].get("rich_text", []))
        return f"### {text}\n\n"

    elif block_type == "bulleted_list_item":
        text = get_plain_text(block["bulleted_list_item"].get("rich_text", []))
        return f"- {text}\n"

    elif block_type == "numbered_list_item":
        text = get_plain_text(block["numbered_list_item"].get("rich_text", []))
        return f"1. {text}\n"

    elif block_type == "code":
        code_block = block["code"]
        language = code_block.get("language", "")
        text = get_plain_text(code_block.get("rich_text", []))
        return f"```{language}\n{text}\n```\n\n"

    elif block_type == "quote":
        text = get_plain_text(block["quote"].get("rich_text", []))
        return f"> {text}\n\n"

    elif block_type == "divider":
        return "---\n\n"

    return ""

def sync_notion_to_hugo():
    """主同步函数"""
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("错误: 请设置 NOTION_TOKEN 和 NOTION_DATABASE_ID 环境变量")
        return

    # 初始化 Notion 客户端
    notion = Client(auth=NOTION_TOKEN)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"开始从 Notion 同步内容...")
    print(f"数据库 ID: {NOTION_DATABASE_ID}")

    try:
        # 查询数据库
        response = notion.databases.query(
            **{
                "database_id": NOTION_DATABASE_ID
            }
        )
        pages = response.get("results", [])

        print(f"找到 {len(pages)} 篇文章")

        for page in pages:
            page_id = page["id"]
            properties = page.get("properties", {})

            # 获取标题
            title = (get_property_value(properties, "Title") or
                     get_property_value(properties, "Name") or
                     get_property_value(properties, "标题") or
                     "untitled")

            print(f"处理: {title}")

            # 获取页面内容
            blocks = notion.blocks.children.list(block_id=page_id)
            blocks_content = ""

            for block in blocks.get("results", []):
                blocks_content += block_to_markdown(block)

            # 转换为 Markdown
            markdown_content = page_to_markdown(page, blocks_content)

            # 生成文件名
            filename = sanitize_filename(title) + ".md"
            filepath = OUTPUT_DIR / filename

            # 写入文件
            filepath.write_text(markdown_content, encoding="utf-8")
            print(f"  ✓ 已保存: {filepath}")

        print(f"\n同步完成! 共处理 {len(pages)} 篇文章")

    except Exception as e:
        print(f"错误: {e}")
        raise

if __name__ == "__main__":
    sync_notion_to_hugo()
