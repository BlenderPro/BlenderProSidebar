import bpy
import os
from . import assembly_props
from . import assembly_ops
from . import assembly_ui
from . import data_assembly

assembly_props.register()

LIBRARY_PATH = os.path.join(os.path.dirname(__file__),"library")
PANEL_ID = 'Room_PT_library_settings'