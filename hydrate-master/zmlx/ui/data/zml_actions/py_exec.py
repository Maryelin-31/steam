# ** is_sys = True
# ** text = '运行'
# ** on_toolbar = True
# ** tooltip = '运行当前标签页面显示的脚本'
# ** icon = 'begin.png'
# ** name = 'action_exec_current'


from zml import app_data

main_window = app_data.space.get('main_window', None)
if main_window is not None:
    widget = main_window.tab_widget.currentWidget()
    if hasattr(widget, 'console_exec'):
        widget.console_exec()
