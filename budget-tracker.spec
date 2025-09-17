# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['budget_tracker/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('budget_tracker/*.py', 'budget_tracker'), ('budget_tracker/__init__.py', 'budget_tracker')],
    hiddenimports=['budget_tracker.database', 'budget_tracker.transactions', 'budget_tracker.budgets', 'budget_tracker.reports', 'budget_tracker.settings', 'budget_tracker.utils', 'sqlalchemy', 'rich', 'typer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='budget-tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
