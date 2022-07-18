bl_info = {
    "name": "Add Hyperboloid",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import math
import numpy as np
from mathutils import *
from math import *
from bpy.types import Operator
from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
)


def create_mesh_object(context, verts, edges, faces, name):

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Make a mesh from a list of verts/edges/faces
    mesh.from_pydata(verts, edges, faces)

    # Update mesh geometry after adding stuff
    mesh.update()

    from bpy_extras import object_utils

    return object_utils.object_data_add(context, mesh, operator=None)


class AddHyperboloidSurface(Operator):
    bl_idname = "mesh.primitive_hyperboloid"
    bl_label = "Add Hyperboloid"
    bl_description = "Add a hyperboloid surface"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    a: FloatProperty(
        name="a",
        description="width parameter of hyperboloid",
        min=0.0,
        max=1e6,
        default=1,
    )

    b: FloatProperty(
        name="b",
        description="height parameter of hyperboloid",
        min=-1e6,
        max=1e6,
        default=0,
    )

    u_min: FloatProperty(
        name="U min",
        description="Minimum U value. Lower boundary of U range",
        min=-100.00,
        max=0.00,
        default=0.00,
    )
    u_max: FloatProperty(
        name="U max",
        description="Maximum U value. Upper boundary of U range",
        min=0.00,
        max=100.00,
        default=2 * np.pi,
    )
    u_step: IntProperty(
        name="U step", description="U Subdivisions", min=1, max=1024, default=128
    )

    v_min: FloatProperty(
        name="V min",
        description="Minimum V value. Lower boundary of V range",
        min=-100.00,
        max=0.00,
        default=0.00,
    )
    v_max: FloatProperty(
        name="V max",
        description="Maximum V value. Upper boundary of V range",
        min=0.00,
        max=100.00,
        default=1,
    )
    v_step: IntProperty(
        name="V step", description="V Subdivisions", min=1, max=1024, default=128
    )

    def execute(self, context):
        verts = []
        u = np.arange(self.u_min, self.u_max, (self.u_max - self.u_min) / self.u_step)
        v = np.arange(self.v_min, self.v_max, (self.v_max - self.v_min) / self.v_step)

        v_g, u_g = np.meshgrid(v, u, indexing="ij")

        xyz = np.stack(
            [
                self.a * np.cos(u_g) * np.sinh(v_g),
                self.a * np.sin(u_g) * np.sinh(v_g),
                self.b * np.cosh(v_g),
            ],
            axis=-1,
        )

        verts = xyz.reshape((-1, 3))

        faces = []

        for iu in range(self.u_step):
            u_next = iu + 1

            if u_next == self.u_step:
                u_next = 0

            for iv in range(self.v_step - 1):
                faces.append(
                    [
                        (iv + 1) * self.u_step + (u_next),
                        (iv + 1) * self.u_step + iu,
                        (iv * self.u_step) + iu,
                        (iv * self.u_step) + (u_next),
                    ]
                )

        if verts == []:
            return {"CANCELLED"}

        obj = create_mesh_object(context, verts, [], faces, "hyperboloid")

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(AddHyperboloidSurface.bl_idname)


def register():
    bpy.utils.register_class(AddHyperboloidSurface)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddHyperboloidSurface)


if __name__ == "__main__":
    register()
