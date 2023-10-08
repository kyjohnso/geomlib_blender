#!/usr/bin/env python

import numpy as np
import bpy
import mathutils

def create_3d_ellipsoid_from_covariance(covariance,subdivisions=2,factor=1):
    """
    Creates a blender 3d ellipsoid from a 3d covariance matrix rotating and scaling
    it in the scene appropriately.

    Arguments:
        covariance: a np.ndarray of shape 3x3 representing the covariance of an ellipsoid
        factor: a scale factor to multiply the size of the ellipse by
    """
    val, vec = np.linalg.eig(covariance)

    mat = np.eye(4)
    mat[:3,:3] = vec*np.sqrt(val[np.newaxis,:])*factor
    mat = mathutils.Matrix(mat)

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3,
        radius=1,
        enter_editmode=False,
        align="WORLD",
        location=(0,0,0),
        scale = (1,1,1),
    )
    bpy.context.object.matrix_world = mat

    return bpy.context.object