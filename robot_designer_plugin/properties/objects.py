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
# Copyright (c) 2015, Karlsruhe Institute of Technology (KIT)
# Copyright (c) 2016, FZI Forschungszentrum Informatik
#
# Changes:
#
#   2015-01-16: Stefan Ulbrich (FZI), Major refactoring. Integrated into complex plugin framework.
#   2017-06:    Benedikt Feldotto (TUM): Model Meta Data
#   2017-07:    Benedikt Feldotto (TUM): Full Inertia Support
#   2017-09:    Benedikt Feldotto (TUM), Muscle Support

#
# ######

# Blender imports
from glob import glob

import bpy
from bpy.props import FloatProperty, StringProperty, \
    EnumProperty, FloatVectorProperty, PointerProperty, IntProperty, CollectionProperty, BoolProperty, IntVectorProperty

# RobotDesigner imports
from ..core import PluginManager
from ..properties.globals import global_properties


# from .globals import global_properties

@PluginManager.register_property_group()
class RDDynamics(bpy.types.PropertyGroup):
    '''
    Property group that contains dynamics values
    '''
    # from mathutils import Vector
    # def updateCoM(self, context):
    #    frame = bpy.data.objects[bpy.context.scene.RobotEditor.physicsFrameName]
    #    position = Vector((frame.RobotEditor.dynamics.CoM[0],frame.RobotEditor.dynamics.CoM[1],
    # frame.RobotEditor.dynamics.CoM[2]))
    #    frame.location = position

    # CoM = FloatVectorProperty(name = "Center of Mass", update=updateCoM, subtype = 'XYZ')
    mass = FloatProperty(name="Mass (kg)", precision=4, step=0.1, default=1.0)

    # add inertia pose here
    inertiaTrans = FloatVectorProperty(name="Translation", precision=4, step=0.1, default=[0.0, 0.0, 0.0])
    inertiaRot = FloatVectorProperty(name="Rotation", precision=4, step=0.1, default=[0.0, 0.0, 0.0])

    # new inertia tensor
    inertiaXX = FloatProperty(name="", precision=4, step=0.1, default=1.0)
    inertiaXY = FloatProperty(name="", precision=4, step=0.1, default=1.0)
    inertiaXZ = FloatProperty(name="", precision=4, step=0.1, default=1.0)
    inertiaYY = FloatProperty(name="", precision=4, step=0.1, default=1.0)
    inertiaYZ = FloatProperty(name="", precision=4, step=0.1, default=1.0)
    inertiaZZ = FloatProperty(name="", precision=4, step=0.1, default=1.0)



@PluginManager.register_property_group()
class RDCamera(bpy.types.PropertyGroup):
    width = IntProperty(default=320, min=1)
    height = IntProperty(default=240, min=1)
    format = EnumProperty(items=[('L8', 'L8', 'L8'),
                                 ('R8G8B8', 'R8G8B8', 'R8G8B8'),
                                 ('B8G8R8', 'B8G8R8', 'B8G8R8'),
                                 ('BAYER_RGGB8', 'BAYER_RGGB8', 'BAYER_RGGB8'),
                                 ('BAYER_BGGR8', 'BAYER_BGGR8', 'BAYER_BGGR8'),
                                 ('BAYER_GBRG8', 'BAYER_GBRG8', 'BAYER_GBRG8'),
                                 ('BAYER_GRBG8', 'BAYER_GRBG8', 'BAYER_GRBG8')
                                 ])
    location = FloatVectorProperty(name="Location")

@PluginManager.register_property_group()
class RDContactSensor(bpy.types.PropertyGroup):
    collision = StringProperty(name="collision", default="__default_topic__")

@PluginManager.register_property_group()
class RDForceTorqueSensor(bpy.types.PropertyGroup):
    frame = StringProperty(name="frame", default="child")
    measure_direction = StringProperty(name="measure_direction", default="child_to_parent")

@PluginManager.register_property_group()
class RDDepthCameraSensor(bpy.types.PropertyGroup):
    output = StringProperty(name="output", default="depths")

#@PluginManager.register_property_group()
#class RDAltimeterSensor(bpy.types.PropertyGroup):

#@PluginManager.register_property_group()
#class RDIMUSensor(bpy.types.PropertyGroup):


@PluginManager.register_property_group()
class RDLaser(bpy.types.PropertyGroup):
    horizontal_samples = IntProperty(name="horizontal samples", default=320, min=1)
    vertical_samples = IntProperty(name="vertical samples", default=240, min=1)
    resolution = EnumProperty(items=[('8-Bit', '8-Bit', '8-Bit'),
                                     ('16-Bit', '16-Bit', '16-Bit')
                                     ])



class SceneSettingItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Test Prop", default="Unknown")
    value = bpy.props.IntProperty(name="Test Prop", default=22)


class RDMusclePoints(bpy.types.PropertyGroup):
    '''
    Property group that contains muscle attachment point specifications
    '''
    # x = FloatProperty(name="X", precision=4, step=0.1, default=1.0)
    # y = FloatProperty(name="Y", precision=4, step=0.1, default=1.0)
    # z = FloatProperty(name="Z", precision=4, step=0.1, default=1.0)

    coordFrame = StringProperty(default="Select Segment")


@PluginManager.register_property_group()
class RDMuscle(bpy.types.PropertyGroup):
    '''
    Property group that contains muscle values
    '''

    def muscle_type_update(self, context):
        active_muscle = global_properties.active_muscle.get(bpy.context.scene)

        # if bpy.data.objects[active_muscle].RobotEditor.muscles.muscleType == 'MYOROBOTICS':
        #    color = (1.0,0.0,0.0)
        if bpy.data.objects[active_muscle].RobotEditor.muscles.muscleType == 'MILLARD_EQUIL':
            color = (0.8, 0.3, 0.0)
        elif bpy.data.objects[active_muscle].RobotEditor.muscles.muscleType == 'MILLARD_ACCEL':
            color = (0.3, 0.8, 0.0)
        elif bpy.data.objects[active_muscle].RobotEditor.muscles.muscleType == 'THELEN':
            color = (1.0, 0.0, 0.0)
        elif bpy.data.objects[active_muscle].RobotEditor.muscles.muscleType == 'RIGID_TENDON':
            color = (0.0, 0.0, 1.0)

        bpy.data.objects[active_muscle].data.materials[active_muscle + '_vis'].diffuse_color = color

    muscleType = EnumProperty(
        items=[#('MYOROBOTICS', 'Myorobotics', 'Myorobotics Muscle'),
               ('MILLARD_EQUIL', 'Millard Equilibrium 2012', 'Millard Equilibrium 2012 Muscle'),
               ('MILLARD_ACCEL', 'Millard Acceleration 2012', 'Millard Acceleration 2012 Muscle'),
               ('THELEN', 'Thelen 2003', 'Thelen 2003 Muscle'),
               ('RIGID_TENDON', 'Rigid Tendon', 'Rigid Tendon Muscle')],
        name="Muscle Type:", update=muscle_type_update
    )

    robotName = StringProperty(name="RobotName")
    length = FloatProperty(name="muscle length", default=0.0, precision=2)
    max_isometric_force = FloatProperty(name="Max isometric Force", default=1000)

    bpy.utils.register_class(RDMusclePoints)
    pathPoints = CollectionProperty(type=RDMusclePoints)


@PluginManager.register_property_group()
class RDModelMeta(bpy.types.PropertyGroup):
   '''
   Property group that contains model meta data suc as name, version and description
   '''
   model_version = StringProperty(name='Version', default="1.0")
   model_description = StringProperty(name='Description')

#Update Ricardo
@PluginManager.register_property_group()
class ModelMeta(bpy.types.PropertyGroup):
   '''
   Property group that contains model meta data suc as name, version and description
   '''
   var1 = StringProperty(name='Var1')
   var2 = StringProperty(name='Var2')

@PluginManager.register_property_group()
class RobotSelfCollision(bpy.types.PropertyGroup):
   '''
   Property group that contains information about self collision
   '''
   robot_self_collide = BoolProperty(name='Self Collide')

@PluginManager.register_property_group()
class LinkInfo(bpy.types.PropertyGroup):
   '''
   Property group that contains information about link's gravity and self collision
   '''
   link_self_collide = BoolProperty(name='Self Collide')
   gravity = BoolProperty(name='Gravity')

@PluginManager.register_property_group()
class Ode(bpy.types.PropertyGroup):
   '''
   Property group that contains ODE data
   '''
   cmf_damping = StringProperty(name='CFM Damping')
   i_s_damper = StringProperty(name='Implicit-something-Damper')
   cmf = StringProperty(name='CMF')
   erp = StringProperty(name='ERP')

@PluginManager.register_property_group()
class SDFCollisionProperties(bpy.types.PropertyGroup):
   '''
   Property group that contains SDF-Collision-parameters
   '''
   restitution_coeff = IntProperty(name="Restitution Coeff.", default=0, min =0, max=1)
   threshold = IntProperty(name='Threshold', default=0, min=0, max=1000)
   coefficient = IntProperty(name='Coefficient', default=1, min=0, max=1)
   use_patch_radius = BoolProperty(name = "Use patch radius", default=True)
   patch_radius = IntProperty(name = 'Patch Radius', default=0, min=0, max=1000)
   surface_radius = IntProperty(name='Surface Radius', default=0, min=0, max=1000)
   slip = IntProperty(name='Slip', default=0, min=0, max=1)
   mu = IntProperty(name='Mu', default=1, min=0, max=1)
   mu2 = IntProperty(name='Mu2', default=1, min=0, max=1)
   fdir1 = IntVectorProperty(name='FDir1', default=(0,0,0), min=0, max=1)
   slip1 = IntProperty(name='Slip1', default=0, min=0, max=1)
   slip2 = IntProperty(name='Slip2', default=0, min=0, max=1)
   collide_wo_contact = BoolProperty(name="Colide without contact", default=True)
   collide_wo_contact_bitmask = IntProperty(name='Colide without contact bitmask', default=1, min=0, max=1000)
   collide_bitmask = IntProperty(name='Collide bitmask', default=65535, min=0, max=65535)
   category_bitmask = IntProperty(name='Category bitmask', default=655355, min=0, max=65535)
   poissons_ratio = FloatProperty(name='Poissons Ratio', default=0.3, min=-1, max=0.5)
   elastic_modulus = FloatProperty(name='Elastic Modulus', default=-1, min=-1, max=0)
   soft_cfm = FloatProperty(name='Soft CFM', default=0, min=0, max=1)
   soft_erp = FloatProperty(name='Soft ERP', default=0.2, min=0, max=1)
   kp = FloatProperty(name='Kp', default=1000000000000, min=0, max=1000000000000)
   kd = FloatProperty(name='Kd', default=1, min=0, max=1)
   max_vel = FloatProperty(name='Max. Vel.', default=0.01, min=0, max=1)
   min_depth = FloatProperty(name='Min. Depth', default=0, min=0, max=10)
   bone_attachment = FloatProperty(name='Bone Attachment', default=100, min=0, max=1000)
   stiffness = FloatProperty(name='Stiffness', default=100, min=0, max=10000)
   damping = FloatProperty(name='Damping', default=10, min=0, max=100)
   flesh_mass_fraction = FloatProperty(name='Flesh mass fraction', default=0.05, min=0, max=1)


###############

@PluginManager.register_property_group()
class RDAuthor(bpy.types.PropertyGroup):
   '''
   Property group that contains author details such as name and email
   '''
   authorName = StringProperty(name="author name")
   authorEmail = StringProperty(name ="author email")


@PluginManager.register_property_group(bpy.types.Object)
class RDObjects(bpy.types.PropertyGroup):
    '''
    Property group that stores general information for individual Blender
    objects with respect to the RobotEditor
    '''
    fileName = StringProperty(name="Mesh File Name")
    tag = EnumProperty(
        items=[('DEFAULT', 'Default', 'Default'),
               ('MARKER', 'Marker', 'Marker'),
               ('PHYSICS_FRAME', 'Physics Frame', 'Physics Frame'),
               ('ARMATURE', 'Armature', 'Armature'),
               ('COLLISION', 'Collision', 'Collision'),
               ('CAMERA_SENSOR', 'Camera sensor', 'Camera sensor'),
               ('LASER_SENSOR', 'Laser sensor', 'Laser sensor')]
    )

    dynamics = PointerProperty(type=RDDynamics)
    camera = PointerProperty(type=RDCamera)
    contactSensor = PointerProperty(type=RDContactSensor)
    forceTorqueSensor = PointerProperty(type=RDForceTorqueSensor)
    depthCameraSensor = PointerProperty(type=RDDepthCameraSensor)
    altimeterSensor = PointerProperty(type=RDAltimeterSensor)
    #imuSensor = PointerProperty(type=RDIMUSensor)
    #modelMeta = PointerProperty(type=RDModelMeta)
    modelMeta1 = PointerProperty(type=ModelMeta)
    robotSelfCollision = PointerProperty(type=RobotSelfCollision)
    linkInfo = PointerProperty(type=LinkInfo)
    ode = PointerProperty(type=Ode)
    sdfCollisionProps = PointerProperty(type=SDFCollisionProperties)
    author = PointerProperty(type=RDAuthor)
    muscles = PointerProperty(type=RDMuscle)



