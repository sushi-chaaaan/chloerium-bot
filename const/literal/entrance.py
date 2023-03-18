JOIN_LOG = """
時刻: {joined}
参加メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""


def join_log(joined: str, name: str, id: int, mention: str, created: str, count: int) -> str:
    return JOIN_LOG.format(
        joined=joined,
        name=name,
        id=str(id),
        mention=mention,
        created=created,
        count=str(count),
    )


LEAVE_LOG = """
時刻: {left}
退出メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""


def leave_log(left: str, name: str, id: int, mention: str, created: str, count: int) -> str:
    return LEAVE_LOG.format(
        left=left,
        name=name,
        id=str(id),
        mention=mention,
        created=created,
        count=str(count),
    )
