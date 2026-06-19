from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例配置数据
SAMPLE_URL = "https://webs-bqqueen.com"
SAMPLE_KEYWORD = "赏金女王"

# 格式化时间戳
def _format_timestamp(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class KeywordNote:
    """单个关键词笔记的数据模型"""
    keyword: str
    source_url: str
    content: str
    tags: List[str] = field(default_factory=list)
    priority: int = 0
    created_at: str = field(default_factory=_format_timestamp)
    updated_at: str = field(default_factory=_format_timestamp)

    def update_content(self, new_content: str) -> None:
        """更新笔记内容并记录时间"""
        self.content = new_content
        self.updated_at = _format_timestamp()

    def add_tag(self, tag: str) -> None:
        """添加标签（去重）"""
        if tag not in self.tags:
            self.tags.append(tag)

@dataclass
class KeywordNotesCollection:
    """管理一组关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sort_by_priority(self, reverse: bool = True) -> None:
        self.notes.sort(key=lambda n: n.priority, reverse=reverse)

# 格式化输出函数
def format_note_as_text(note: KeywordNote) -> str:
    """将单条笔记格式化为可读文本"""
    lines = [
        f"【{note.keyword}】",
        f"  来源：{note.source_url}",
        f"  内容：{note.content[:60]}{'...' if len(note.content) > 60 else ''}",
        f"  标签：{', '.join(note.tags) if note.tags else '无'}",
        f"  优先级：{note.priority}",
        f"  创建：{note.created_at}",
        f"  更新：{note.updated_at}",
    ]
    return "\n".join(lines)

def format_notes_brief(notes: List[KeywordNote]) -> str:
    """将多条笔记格式化为简要列表"""
    if not notes:
        return "暂无笔记记录。"
    result_parts = []
    for i, note in enumerate(notes, 1):
        result_parts.append(f"{i}. [{note.keyword}] {note.content[:50]}")
    return "\n".join(result_parts)

def format_note_as_html(note: KeywordNote) -> str:
    """将单条笔记格式化为简单的HTML片段（适合展示）"""
    content_safe = note.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    keyword_safe = note.keyword.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    url_safe = note.source_url.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tags_safe = ", ".join(t.replace("&", "&amp;").replace("<", "&lt;") for t in note.tags)
    return (
        f"<div class='keyword-note'>\n"
        f"  <h3>{keyword_safe}</h3>\n"
        f"  <p><strong>来源：</strong><a href='{url_safe}'>{url_safe}</a></p>\n"
        f"  <p><strong>内容：</strong>{content_safe}</p>\n"
        f"  <p><strong>标签：</strong>{tags_safe if tags_safe else '无'}</p>\n"
        f"  <p><strong>优先级：</strong>{note.priority}</p>\n"
        f"  <p><strong>更新时间：</strong>{note.updated_at}</p>\n"
        f"</div>"
    )

# 示例运行（可直接执行）
if __name__ == "__main__":
    # 创建示例笔记
    note1 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        source_url=SAMPLE_URL,
        content="赏金女王是一款热门游戏，拥有独特奖励机制与丰富角色设计。",
        tags=["游戏", "热门", "奖励"],
        priority=5,
    )
    note2 = KeywordNote(
        keyword="赏金女王攻略",
        source_url=f"{SAMPLE_URL}/guide",
        content="这篇攻略详细介绍了赏金女王的角色技能与通关技巧。",
        tags=["攻略", "技巧"],
        priority=3,
    )
    note3 = KeywordNote(
        keyword="赏金女王评测",
        source_url=f"{SAMPLE_URL}/review",
        content="玩家社区对赏金女王的综合评价较高，画面精美。",
        tags=["评测", "社区"],
        priority=4,
    )

    # 创建集合并添加笔记
    collection = KeywordNotesCollection()
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    # 输出格式化结果
    print("=== 全部笔记（文本格式） ===")
    print(format_notes_brief(collection.notes))
    print("\n=== 第一条笔记详情 ===")
    print(format_note_as_text(collection.notes[0]))
    print("\n=== 第一条笔记（HTML格式） ===")
    print(format_note_as_html(collection.notes[0]))

    # 按优先级排序
    collection.sort_by_priority()
    print("\n=== 按优先级排序后（降序） ===")
    for note in collection.notes:
        print(f"  [{note.priority}] {note.keyword}")