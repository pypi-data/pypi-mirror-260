from afeng_tools.fastapi_tool.common.enum import IconTypeEnum


def get_icon_code(icon_type: IconTypeEnum, icon_value: str, alt: str = '') -> str | None:
    """获取icon代码"""
    if icon_type == IconTypeEnum.svg_icon:
        return icon_value
    elif icon_type == IconTypeEnum.resource_icon:
        if icon_value:
            return f'<img data-src="/resource/public/{icon_value}" alt="{alt}"/>'
        else:
            return None
    else:
        return f'<img data-src="{icon_value}" data-type="image" referrer="no-referrer" referrerpolicy="no-referrer" alt="{alt}" title="{alt}"/>'
