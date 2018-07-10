# #####
# This file is part of the RobotDesigner of the Neurorobotics subproject (SP10)
# in the Human Brain Project (HBP).
# It has been forked from the RobotEditor (https://gitlab.com/h2t/roboteditor)
# developed at the Karlsruhe Institute of Technology in the
# High Performance Humanoid Technologies Laboratory (H2T).
# #####

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# #####
#
# Copyright (c) 2018, Technical University Munich
#
#
# #####

# Blender imports
import bpy

# RobotDesigner imports
from ..core import config, PluginManager, Condition, RDOperator

from ..operators.helpers import ModelSelected, ObjectMode

from ..export import sdf

from ..interface.helpers import getSingleSegment


@RDOperator.Preconditions(ObjectMode)
@PluginManager.register_class
class ImportGripper1(RDOperator):
    """
    :term:`Operator<operator>` for importing a gripper from an SDF plain file
    """

    # Obligatory class attributes
    bl_idname = config.OPERATOR_PREFIX + "import_gripper_1_sdf"
    bl_label = "2 finger angular"

    # Requires resources grippers folder to be inside #/Library/Application Support/Blender/2.79/datafiles
    path_to_addons = bpy.utils.user_resource('DATAFILES', create=True)
    filepath = path_to_addons + "grippers/gripper_2_finger_angular/model.sdf/model.sdf"

    @RDOperator.OperatorLogger
    @RDOperator.Postconditions(ModelSelected, ObjectMode)
    def execute(self, context):
        # import os
        importer = sdf.sdf_import.Importer(self, self.filepath)
        importer.import_file()
        return {'FINISHED'}


@RDOperator.Preconditions(ObjectMode)
@PluginManager.register_class
class ImportGripper2(RDOperator):
    """
    :term:`Operator<operator>` for importing a gripper from an SDF plain file
    """

    # Obligatory class attributes
    bl_idname = config.OPERATOR_PREFIX + "import_gripper_2_sdf"
    bl_label = "2 finger angular wrist"

    # Requires resources grippers folder to be inside #/Library/Application Support/Blender/2.79/datafiles
    path_to_addons = bpy.utils.user_resource('DATAFILES', create=True)
    filepath = path_to_addons + "grippers/gripper_2_finger_angular_wrist/model.sdf/model.sdf"

    @RDOperator.OperatorLogger
    @RDOperator.Postconditions(ModelSelected, ObjectMode)
    def execute(self, context):
        import os

        importer = sdf.sdf_import.Importer(self, self.filepath)
        importer.import_file()
        return {'FINISHED'}


@RDOperator.Preconditions(ObjectMode)
@PluginManager.register_class
class ImportGripper3(RDOperator):
    """
    :term:`Operator<operator>` for importing a gripper from an SDF plain file
    """

    # Obligatory class attributes
    bl_idname = config.OPERATOR_PREFIX + "import_gripper_3_sdf"
    bl_label = "4 finger centric"

    # Requires resources grippers folder to be inside #/Library/Application Support/Blender/2.79/datafiles
    path_to_addons = bpy.utils.user_resource('DATAFILES', create=True)
    filepath = path_to_addons + "grippers/gripper_4_finger_centric/model.sdf/model.sdf"

    @RDOperator.OperatorLogger
    @RDOperator.Postconditions(ModelSelected, ObjectMode)
    def execute(self, context):
        import os
        importer = sdf.sdf_import.Importer(self, self.filepath)
        importer.import_file()
        return {'FINISHED'}


@RDOperator.Preconditions(ObjectMode)
@PluginManager.register_class
class ImportGripper4(RDOperator):
    """
    :term:`Operator<operator>` for importing a gripper from an SDF plain file
    """

    # Obligatory class attributes
    bl_idname = config.OPERATOR_PREFIX + "import_gripper_4_sdf"
    bl_label = "Humanoid hand"

    # Requires resources grippers folder to be inside #/Library/Application Support/Blender/2.79/datafiles
    path_to_addons = bpy.utils.user_resource('DATAFILES', create=True)
    filepath = path_to_addons + "grippers/gripper_2_finger_angular/model.sdf/model.sdf"

    @RDOperator.OperatorLogger
    @RDOperator.Postconditions(ModelSelected, ObjectMode)
    def execute(self, context):
        import os
        importer = sdf.sdf_import.Importer(self, self.filepath)
        importer.import_file()
        return {'FINISHED'}


class BaseMenu(object):

    from ..core.logfile import gui_logger
    logger = gui_logger

    @classmethod
    def putMenu(cls, layout, context, text="", **kwargs): # todo which kwargs are possible
        layout.menu(cls.bl_idname, text=text)


@PluginManager.register_class
class ModuleMenu(bpy.types.Menu, BaseMenu):
    """
    :ref:`menu` for selecting a module to add to an existing robot
    """

    from ..core.config import OPERATOR_PREFIX
    bl_idname = OPERATOR_PREFIX + "modulemenu"
    bl_label = "Select Model"

    @RDOperator.OperatorLogger
    def draw(self, context):
        from ..operators import model
        layout = self.layout
        # Show all addable modules except the one that has been selected as base robot
        armatures = [obj for obj in context.scene.objects if ((obj.type == 'ARMATURE') & (obj != bpy.context.active_object))]

        for arm in armatures:
            text = arm.name
            model.SelectModuleToAdd.place_button(layout, text=text).module_name = text


@PluginManager.register_class
class AssignParentMenu(bpy.types.Menu, BaseMenu):
    """
    :ref:`menu` for selecting a robot, to which a new module should be added
    """

    from ..core.config import OPERATOR_PREFIX
    bl_idname = OPERATOR_PREFIX + "parentbonemenu"
    bl_label = "Select Parent Bone"

    @RDOperator.OperatorLogger
    def draw(self, context):
        from ..operators import model
        layout = self.layout
        armatures = [obj for obj in context.scene.objects if obj.type == 'ARMATURE']

        for arm in armatures:
            # Place one button for each armature in Scene
            text = arm.name
            model.SelectParentBone.place_button(layout, text=text).parent_segment_name = text


@RDOperator.Preconditions(ObjectMode)
@PluginManager.register_class
class MergeModuleToRobot(RDOperator):
    """
    :term:`Operator<operator>` for merging the selected robot module as child of the selected parent robot bone
    """

    # Obligatory class attributes
    bl_idname = config.OPERATOR_PREFIX + "merge_module_to_robot"
    bl_label = "Assign module to parent robot"

    @RDOperator.OperatorLogger
    @RDOperator.Postconditions(ModelSelected, ObjectMode)
    def execute(self, context):
        # A 'merge' and then 'reassign parent' function in one
        from . import segments
        from . import model
        from ..properties.globals import global_properties

        parentRobotName = context.active_object.name
        single_segment = getSingleSegment(context)
        parentSegmentName = single_segment.name
        selectedModuleBaseName = global_properties.new_module_bone_name.get(context.scene)

        # TODO check if parentSegmentName and selectedModuleBaseName are identical
        # change parentSegmentName if that is the case (to avoid Blender adding .001 to the name)
        # if (parentSegmentName == selectedModuleBaseName):
            # newName = parentSegmentName + "_001"
            # bpy.context.active_bone.name = newName
            # parentSegmentName = newName

        self.logger.debug("Parent robot: " + parentRobotName)
        self.logger.debug("Parent segment: " + parentSegmentName)
        self.logger.debug("Active bone: " + bpy.context.active_bone.name)
        self.logger.debug("Name of selected module's base: " + selectedModuleBaseName)

        model.SelectModel.run(model_name=global_properties.new_module_name.get(context.scene))
        bpy.data.objects[parentRobotName].select = True

        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        segments.AssignParentSegment.run(parent_name=parentSegmentName)
        segments.SelectSegment.run(segment_name=parentSegmentName)
        segments.UpdateSegmentsRigid.run(segment_name=selectedModuleBaseName, recurse=True)  # This function is responsible for moving the merged objects together

        # Merge function swaps the name of the resulting armature (robot)
        # Thus, change the name to the actual root robot and everything should be fine
        segments.SelectSegment.run(segment_name=parentSegmentName)
        model.RenameModel.run(newName=parentRobotName)

        return {'FINISHED'}
