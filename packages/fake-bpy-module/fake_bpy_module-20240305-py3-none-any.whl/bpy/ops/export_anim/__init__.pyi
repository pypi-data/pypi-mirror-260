import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def bvh(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Optional[typing.Union[bool, typing.Any]] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.bvh",
    global_scale: typing.Optional[typing.Any] = 1.0,
    frame_start: typing.Optional[typing.Any] = 0,
    frame_end: typing.Optional[typing.Any] = 0,
    rotate_mode: typing.Optional[typing.Any] = "NATIVE",
    root_transform_only: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Save a BVH motion capture file from an armature

        :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
        :type execution_context: typing.Optional[typing.Union[int, str]]
        :type undo: typing.Optional[bool]
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Optional[typing.Union[bool, typing.Any]]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
        :param global_scale: Scale, Scale the BVH by this value
        :type global_scale: typing.Optional[typing.Any]
        :param frame_start: Start Frame, Starting frame to export
        :type frame_start: typing.Optional[typing.Any]
        :param frame_end: End Frame, End frame to export
        :type frame_end: typing.Optional[typing.Any]
        :param rotate_mode: Rotation, Rotation conversion

    NATIVE
    Euler (Native) -- Use the rotation order defined in the BVH file.

    XYZ
    Euler (XYZ) -- Convert rotations to euler XYZ.

    XZY
    Euler (XZY) -- Convert rotations to euler XZY.

    YXZ
    Euler (YXZ) -- Convert rotations to euler YXZ.

    YZX
    Euler (YZX) -- Convert rotations to euler YZX.

    ZXY
    Euler (ZXY) -- Convert rotations to euler ZXY.

    ZYX
    Euler (ZYX) -- Convert rotations to euler ZYX.
        :type rotate_mode: typing.Optional[typing.Any]
        :param root_transform_only: Root Translation Only, Only write out translation channels for the root bone
        :type root_transform_only: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
