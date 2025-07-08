import pathlib

import polib


def compile_translations():
    """
    自动查找并编译 locale 目录下的所有 .po 文件为 .mo 文件。
    """
    # 获取脚本所在的目录，并推导出项目根目录和 locale 目录
    script_path = pathlib.Path(__file__).resolve()
    base_dir = script_path.parent.parent
    # locale 目录
    locale_dir = base_dir / "locale"

    print(f"Searching for .po files in: {locale_dir}")

    # 递归查找 locale 目录下所有的 .po 文件
    po_files = list(locale_dir.rglob("*.po"))

    if not po_files:
        print("No .po files were found to compile.")
        return

    compiled_count = 0
    # 遍历所有找到的 .po 文件
    for po_path in po_files:
        # 将文件扩展名从 .po 替换为 .mo，生成输出路径
        mo_path = po_path.with_suffix(".mo")

        try:
            # 使用 polib 加载 .po 文件
            po_file = polib.pofile(str(po_path), encoding="utf-8")
            # 将其另存为 .mo 文件
            po_file.save_as_mofile(str(mo_path))
            print(f"✅ Compiled: {po_path.relative_to(base_dir)} -> {mo_path.relative_to(base_dir)}")
            compiled_count += 1
        except Exception as e:
            print(f"❌ Error compiling {po_path.relative_to(base_dir)}: {e}")

    print(f"\nCompilation complete. {compiled_count} file(s) compiled.")


if __name__ == "__main__":
    compile_translations()
