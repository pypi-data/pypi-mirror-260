from chimerax.core.toolshed import BundleAPI

class _SeggerAPI(BundleAPI):

    @staticmethod
    def start_tool(session, tool_name):
        if tool_name == 'Segment Map':
            from .segment_dialog import VolumeSegmentationDialog
            d = VolumeSegmentationDialog.get_singleton(session)
        elif tool_name == 'Fit to Segments':
            from .fit_dialog import FitSegmentsDialog
            d = FitSegmentsDialog.get_singleton(session)
        return d

    @staticmethod
    def register_command(command_name, logger):
        # 'register_command' is lazily called when the command is referenced
        if command_name == 'segger':
            from . import segcmd
            segcmd.register_segger_command(logger)

    @staticmethod
    def get_class(class_name):
        # 'get_class' is called by session code to get class saved in a session
        from .regions import Segmentation, Region
        from .segment_dialog import VolumeSegmentationDialog
        from .fit_dialog import FitSegmentsDialog, Fit
        ct = {
            'Segmentation': Segmentation,
            'Region': Region,
            'VolumeSegmentationDialog': VolumeSegmentationDialog,
            'FitSegmentsDialog': FitSegmentsDialog,
            'Fit': Fit,
        }
        return ct.get(class_name)

    @staticmethod
    def run_provider(session, name, mgr, **kw):
        '''Handle open and save of segmentation files.'''
        if mgr == session.open_command:
            from chimerax.open_command import OpenerInfo
            class OpenSegmentationInfo(OpenerInfo):
                def open(self, session, path, file_name, **kw):
                    from .segfile import open_segmentation
                    return open_segmentation(session, path, file_name)
            return OpenSegmentationInfo()
        elif mgr == session.save_command:
            from chimerax.save_command import SaverInfo
            class SaveSegmentationInfo(SaverInfo):
                def save(self, session, path, models=None):
                    from .segfile import save_segmentation
                    save_segmentation(session, path, models = models)
                @property
                def save_args(self):
                    from chimerax.core.commands import ModelsArg
                    return { 'models': ModelsArg }
                def save_args_widget(self, session):
                    from chimerax.save_command.widgets import SaveModelOptionWidget
                    return SaveModelOptionWidget(session, 'Segmentation', Segmentation)
                def save_args_string_from_widget(self, widget):
                    return widget.options_string()

            return SaveSegmentationInfo()
        
        return None

bundle_api = _SeggerAPI()

# ------------------------------------------------------------------------------
#
dev_menus = False       # Include under-development menus.
timing = False          # Report execution times for optimizing code.
seggerVersion = '2.3'
debug = False		# Whether to output debugging messages

from .regions import Segmentation, Region, SelectedRegions
