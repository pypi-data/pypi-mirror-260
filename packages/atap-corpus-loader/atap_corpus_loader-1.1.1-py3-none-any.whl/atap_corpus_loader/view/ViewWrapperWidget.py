from panel import Tabs

from atap_corpus_loader.controller import Controller
from atap_corpus_loader.view.gui import AbstractWidget, FileLoaderWidget, CorpusInfoWidget


class ViewWrapperWidget(AbstractWidget):
    """
    A wrapper class that holds different loading method interfaces within a Tab
    """
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller: Controller = controller

        self.file_loader: FileLoaderWidget = FileLoaderWidget(self, controller)
        self.corpus_display: CorpusInfoWidget = CorpusInfoWidget(controller)

        self.panel = Tabs(("File Loader", self.file_loader),
                          ("Corpus Overview", self.corpus_display))
        self.corpus_info_idx: int = len(self.panel) - 1
        self.children = [self.file_loader, self.corpus_display]

    def update_display(self):
        pass

    def load_corpus_from_filepaths(self, filepath_ls: list[str], include_hidden: bool) -> bool:
        success = self.controller.load_corpus_from_filepaths(filepath_ls, include_hidden)
        self.update_displays()
        return success

    def load_meta_from_filepaths(self, filepath_ls: list[str], include_hidden: bool) -> bool:
        success = self.controller.load_meta_from_filepaths(filepath_ls, include_hidden)
        self.update_displays()
        return success

    def build_corpus(self, corpus_name: str):
        success: bool = self.controller.build_corpus(corpus_name)
        if success:
            self.update_displays()
            self.panel.active = self.corpus_info_idx
            self.file_loader.unload_all()
