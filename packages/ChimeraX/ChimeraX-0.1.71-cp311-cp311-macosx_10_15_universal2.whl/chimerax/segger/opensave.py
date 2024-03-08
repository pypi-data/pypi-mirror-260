class SaveFileDialog:
    def __init__(self, title = 'Save', filters = [], initialdir = None, initialfile = None, command = None):
        from os import path
        if initialdir and initialfile:
            ipath = path.join(initialdir, initialfile)
        elif initialdir:
            ipath = initialdir
        elif initialfile:
            ipath = initialfile
        else:
            ipath = ''
        filter = ';;'.join('%s (%s)' % (name, path) for name, pat, suffix in filters)
        from Qt.QtWidgets import QFileDialog
        save_path, type = QFileDialog.getSaveFileName(caption = title, directory = ipath, filter = filter)
        if save_path:
            command(save_path)
