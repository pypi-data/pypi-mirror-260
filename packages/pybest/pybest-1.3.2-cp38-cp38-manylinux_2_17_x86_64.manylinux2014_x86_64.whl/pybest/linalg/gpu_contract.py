# -*- coding: utf-8 -*-
# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --

# Detailed changelog:
#
# 2023: GPU cupy support written by Maximilian Kriebel

"""Contract arrays via NVIDIA GPU using cupy."""

from pybest.log import timer

# a list of hand-optimized CuPy routines, should outperform the generic implementation
# if a contraction is not contained here, a generic algorithm is also supplied
cupy_optimized = [
    "xac,xbd,ecfd->eafb",
    "xac,xbd,ecfd->efab",
    "xac,xbd,edfc->eafb",
    "xac,xbd,efcd->efab",
    "xac,xbd,efcd->efba",
    "xac,xbd,efcd->eafb",
    "xac,xbd,efcd->abef",
    "xac,xbd,cefd->faeb",
    "xac,xbd,cedf->aebf",
    "xac,xbd,cedf->aefb",
    "xac,xbd,cedf->abfe",
    "xac,xbd,ecdf->efab",
    "xac,xbd,efdc->efab",
    "xac,xbd,cfed->afeb",
    "xac,xbd,defc->aefb",
    "xac,xbd,cde->abe",
    "xac,xbd,dce->abe",
    "xac,xbd,ecfd->efba",
]


def cupy_availability_check():
    """Checks if Cupy CUDA is properly installed.

    Returns True or False.

    """

    from pybest.log import log

    try:
        import cupy as cp
    except ImportError:
        log.warn("Warning")
        log.warn("Cupy CUDA not available.")
        log.warn("Defaulting to numpy.tensordot if select=None.")
        return False
    try:
        test_dummy_cupy = cp.zeros(0)
    except Exception:
        log.warn("Warning")
        log.warn("Can not allocate on VRAM.")
        log.warn("Cupy CUDA not properly installed.")
        log.warn("Defaulting to numpy.tensordot if select=None.")
        return False
    test_dummy_cupy += 1.0  # needed to make ruff happy
    del test_dummy_cupy
    cp.get_default_memory_pool().free_all_blocks()
    return True


@timer.with_section("GPU")
def cupy_helper(subs, *args, **kwargs):
    """Contraction using GPU via cupy

    *** Arguments ***

    * subscript : string
          Specifies the subscripts for summation as comma separated-list
          of subscript labels, for example: 'abcd,efcd->abfe'.

    * operands : DenseNIndex
          These are the other arrays for the operation.
          The last operand is treated as output.

    *** Keyword argument ***

    * parts : positive integer > 0
          If given, an array is split "parts" times and looped over.
          Mostly Cholesky array is split at index "x".
          Option for the user for limited GPU memory.

    """

    import cupy as cp
    import numpy as np

    if subs in (
        "xac,xbd,ecfd->eafb",  # much faster
        "xac,xbd,ecfd->efab",  # much faster
        "xac,xbd,edfc->eafb",  # much faster (~x19)
        "xac,xbd,efcd->efab",
        "xac,xbd,efcd->efba",
        "xac,xbd,efcd->eafb",
        "xac,xbd,efcd->abef",
        "xac,xbd,cefd->faeb",
        "xac,xbd,cedf->aebf",
        "xac,xbd,cedf->aefb",
        "xac,xbd,cedf->abfe",
        "xac,xbd,ecdf->efab",  # much faster (~x17)
        "xac,xbd,efdc->efab",  # much faster (~x10)
        "xac,xbd,cfed->afeb",  # much faster (~x10)
        "xac,xbd,defc->aefb",  # much faster (~x10)
        "xac,xbd,ecfd->efba",  # faster (~x2 numpy.td very efficient)
    ):
        axis_e = str(subs.split("->")[0].split(",")[-1]).rfind("e")
        axis_c = str(subs.split("->")[0].split(",")[-1]).rfind("c")
        axis_f = str(subs.split("->")[0].split(",")[-1]).rfind("f")
        axis_d = str(subs.split("->")[0].split(",")[-1]).rfind("d")

        memhave = cp.cuda.runtime.memGetInfo()[0]

        parts_chol = 1  # how often the cholesky arrays are split
        parts_dense = 1  # how often the dense and result arrays are split.

        # the size of necessery video memory is determined by:
        # number of elements of first dense array (or result of chol*chol)* 16
        # + number of elements of second dense array *16
        # + number of result array *16
        # each one is counted if split
        # in fact this does not really makes sense, because the video memory
        # should be deallocated in between
        # but it works and it crashes if choosen tighter.

        # increase the number how often dense and result array is splitted by 1
        # an upper limit to prevent an endless loop
        # for splitting reasoning, see above
        for parts_dense in range(1, 100):
            memneed = (
                16
                * args[0].shape[1]
                / int(parts_chol)
                * args[0].shape[2]
                * args[1].shape[1]
                / int(parts_chol)
                * args[1].shape[2]
                + 16
                * args[2].shape[axis_e]
                / int(parts_dense)
                * args[2].shape[axis_f]
                * args[0].shape[2]
                * args[1].shape[2]
                + 16
                * args[2].shape[axis_e]
                / int(parts_dense)
                * args[2].shape[axis_f]
                * args[0].shape[1]
                / int(parts_chol)
                * args[1].shape[1]
                / int(parts_chol)
            )

            # if necessary vram < available vram then leave loop and start
            if memhave > memneed:
                break

            # increase the number how often the cholesky are splitted by 1
            parts_chol += 1

            memneed = (
                16
                * args[0].shape[1]
                / int(parts_chol)
                * args[0].shape[2]
                * args[1].shape[1]
                / int(parts_chol)
                * args[1].shape[2]
                + 16
                * args[2].shape[axis_e]
                / int(parts_dense)
                * args[2].shape[axis_f]
                * args[0].shape[2]
                * args[1].shape[2]
                + 16
                * args[2].shape[axis_e]
                / int(parts_dense)
                * args[2].shape[axis_f]
                * args[0].shape[1]
                / int(parts_chol)
                * args[1].shape[1]
                / int(parts_chol)
            )

            if memhave > memneed:
                break

        parts_chol = kwargs.get("parts", parts_chol)
        parts_dense = kwargs.get("parts", parts_dense)

        # get lengths of chunks
        chol_chunk_lengths_1 = []
        for x in range(0, parts_chol):
            chol_chunk_lengths_1.append(
                np.array_split(args[0], parts_chol, axis=1)[x].shape[1]
            )
        chol_chunk_lengths_2 = []
        for x in range(0, parts_chol):
            chol_chunk_lengths_2.append(
                np.array_split(args[1], parts_chol, axis=1)[x].shape[1]
            )
        dense_e_chunk_lengths = []
        for x in range(0, parts_dense):
            dense_e_chunk_lengths.append(
                np.array_split(args[2], parts_dense, axis=axis_e)[x].shape[
                    axis_e
                ]
            )

        if parts_chol == 1 and parts_dense == 1:
            chol1 = cp.array(args[0])
            chol2 = cp.array(args[1])
            # x summation
            result_temp = cp.tensordot(chol1, chol2, axes=(0, 0))
            del chol1, chol2
            cp.get_default_memory_pool().free_all_blocks()
            operand = cp.array(args[2])
            result_part = cp.tensordot(
                result_temp, operand, axes=([1, 3], [axis_c, axis_d])
            )
            del result_temp, operand
            cp.get_default_memory_pool().free_all_blocks()
            if subs in (
                "xac,xbd,ecfd->efab",
                "xac,xbd,efcd->efab",
                "xac,xbd,ecdf->efab",
                "xac,xbd,efdc->efab",
            ):
                result_cp = cp.transpose(result_part, axes=(2, 3, 0, 1))
            elif subs in (
                "xac,xbd,ecfd->eafb",
                "xac,xbd,edfc->eafb",
                "xac,xbd,efcd->eafb",
            ):
                result_cp = cp.transpose(result_part, axes=(2, 0, 3, 1))
            elif subs in (
                "xac,xbd,efcd->efba",
                "xac,xbd,ecfd->efba",
            ):
                result_cp = cp.transpose(result_part, axes=(2, 3, 1, 0))
            elif subs == "xac,xbd,efcd->abef":
                result_cp = result_part
            elif subs == "xac,xbd,cefd->faeb":
                result_cp = cp.transpose(result_part, axes=(3, 0, 2, 1))
            elif subs == "xac,xbd,cedf->aebf":
                result_cp = cp.transpose(result_part, axes=(0, 2, 1, 3))
            elif subs == "xac,xbd,cedf->aefb":
                result_cp = cp.transpose(result_part, axes=(0, 2, 3, 1))
            elif subs == "xac,xbd,cedf->abfe":
                result_cp = cp.transpose(result_part, axes=(0, 1, 3, 2))
            elif subs == "xac,xbd,cfed->afeb":
                result_cp = cp.transpose(result_part, axes=(0, 2, 3, 1))
            elif subs == "xac,xbd,defc->aefb":
                result_cp = cp.transpose(result_part, axes=(0, 2, 3, 1))
            result = result_cp.get()
            del result_part, result_cp
            cp.get_default_memory_pool().free_all_blocks()
        else:
            result = np.zeros(args[3].shape)
            if parts_dense > 1:
                start_e = 0
                end_e = 0
                for e in range(0, parts_dense):
                    end_e += dense_e_chunk_lengths[e]
                    start_a = 0
                    end_a = 0
                    for a in range(0, parts_chol):
                        end_a += chol_chunk_lengths_1[a]
                        start_b = 0
                        end_b = 0
                        for b in range(0, parts_chol):
                            end_b += chol_chunk_lengths_2[b]
                            chol_1 = cp.array(
                                np.array_split(args[0], parts_chol, axis=1)[a]
                            )
                            chol_2 = cp.array(
                                np.array_split(args[1], parts_chol, axis=1)[b]
                            )
                            result_temp = cp.tensordot(
                                chol_1, chol_2, axes=(0, 0)
                            )
                            del chol_1, chol_2
                            cp.get_default_memory_pool().free_all_blocks()
                            operand = cp.array(
                                np.array_split(
                                    args[2],
                                    parts_dense,
                                    axis=axis_e,
                                )[e]
                            )
                            result_temp_2 = cp.tensordot(
                                result_temp,
                                operand,
                                axes=([1, 3], [axis_c, axis_d]),
                            )
                            del operand, result_temp
                            cp.get_default_memory_pool().free_all_blocks()
                            if subs in (
                                "xac,xbd,ecfd->efab",
                                "xac,xbd,efcd->efab",
                                "xac,xbd,ecdf->efab",
                                "xac,xbd,efdc->efab",
                            ):
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 3, 0, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    :,
                                    start_a:end_a,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs in (
                                "xac,xbd,ecfd->eafb",
                                "xac,xbd,edfc->eafb",
                                "xac,xbd,efcd->eafb",
                            ):
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 0, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    start_a:end_a,
                                    :,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs in (
                                "xac,xbd,efcd->efba",
                                "xac,xbd,ecfd->efba",
                            ):
                                result_part = cp.transpose(
                                    result_temp_2, axes=(2, 3, 1, 0)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_e:end_e,
                                    :,
                                    start_b:end_b,
                                    start_a:end_a,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->abfe":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 1, 3, 2)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_b:end_b,
                                    :,
                                    start_e:end_e,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cefd->faeb":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(3, 0, 2, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    :,
                                    start_a:end_a,
                                    start_e:end_e,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->aebf":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 1, 3)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_e:end_e,
                                    start_b:end_b,
                                    :,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cedf->aefb":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_e:end_e,
                                    :,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,efcd->abef":
                                result_part = result_temp_2
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_b:end_b,
                                    start_e:end_e,
                                    :,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,cfed->afeb":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    :,
                                    start_e:end_e,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            elif subs == "xac,xbd,defc->aefb":
                                result_part = cp.transpose(
                                    result_temp_2, axes=(0, 2, 3, 1)
                                )
                                del result_temp_2
                                cp.get_default_memory_pool().free_all_blocks()
                                result[
                                    start_a:end_a,
                                    start_e:end_e,
                                    :,
                                    start_b:end_b,
                                ] = result_part.get()
                                del result_part
                            cp.get_default_memory_pool().free_all_blocks()
                            start_b = end_b
                        start_a = end_a
                    start_e = end_e
            else:
                start_a = 0
                end_a = 0
                for a in range(0, parts_chol):
                    end_a += chol_chunk_lengths_1[a]
                    start_b = 0
                    end_b = 0
                    for b in range(0, parts_chol):
                        end_b += chol_chunk_lengths_2[b]
                        chol_1 = cp.array(
                            np.array_split(args[0], parts_chol, axis=1)[a]
                        )
                        chol_2 = cp.array(
                            np.array_split(args[1], parts_chol, axis=1)[b]
                        )
                        result_temp = cp.tensordot(chol_1, chol_2, axes=(0, 0))
                        del chol_1, chol_2
                        cp.get_default_memory_pool().free_all_blocks()
                        operand = cp.array(args[2])
                        result_temp_2 = cp.tensordot(
                            result_temp,
                            operand,
                            axes=([1, 3], [axis_c, axis_d]),
                        )
                        del operand, result_temp
                        cp.get_default_memory_pool().free_all_blocks()
                        if subs in (
                            "xac,xbd,ecfd->efab",
                            "xac,xbd,efcd->efab",
                            "xac,xbd,ecdf->efab",
                            "xac,xbd,efdc->efab",
                        ):
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 3, 0, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, :, start_a:end_a, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs in (
                            "xac,xbd,ecfd->eafb",
                            "xac,xbd,edfc->eafb",
                            "xac,xbd,efcd->eafb",
                        ):
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 0, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, start_a:end_a, :, start_b:end_b
                            ] = result_part.get()
                            del result_part

                        elif subs in (
                            "xac,xbd,efcd->efba",
                            "xac,xbd,ecfd->efba",
                        ):
                            result_part = cp.transpose(
                                result_temp_2, axes=(2, 3, 1, 0)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, :, start_b:end_b, start_a:end_a
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->abfe":
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 1, 3, 2)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, start_b:end_b, :, :
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cefd->faeb":
                            result_part = cp.transpose(
                                result_temp_2, axes=(3, 0, 2, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                :, start_a:end_a, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->aebf":
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 1, 3)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, start_b:end_b, :
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cedf->aefb":
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,efcd->abef":
                            result_part = result_temp_2
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, start_b:end_b, :, :
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,cfed->afeb":
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        elif subs == "xac,xbd,defc->aefb":
                            result_part = cp.transpose(
                                result_temp_2, axes=(0, 2, 3, 1)
                            )
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, :, :, start_b:end_b
                            ] = result_part.get()
                            del result_part
                        cp.get_default_memory_pool().free_all_blocks()
                        start_b = end_b
                    start_a = end_a

    elif subs in (
        "xac,xbd,cde->abe",
        "xac,xbd,dce->abe",
    ):
        axis_e = str(subs.split("->")[0].split(",")[-1]).rfind("e")
        axis_c = str(subs.split("->")[0].split(",")[-1]).rfind("c")
        axis_d = str(subs.split("->")[0].split(",")[-1]).rfind("d")
        memhave = cp.cuda.runtime.memGetInfo()[0]

        parts_chol = 1
        parts_dense = 1
        # an upper limit to prevent an endless loop
        for parts_dense in range(1, 100):
            memneed = (
                16  # dense
                * args[0].shape[1]
                / int(parts_chol)
                * args[0].shape[2]
                * args[1].shape[1]
                / int(parts_chol)
                * args[1].shape[2]
                + 8 * args[2].size / int(parts_dense)  # intermediate
                + 8
                * args[3].size  # result
                / int(parts_dense)
                / int(parts_chol)
                / int(parts_chol)
            )
            if memhave > memneed:
                break

            parts_chol += 1
            memneed = (
                16  # dense
                * args[0].shape[1]
                / int(parts_chol)
                * args[0].shape[2]
                * args[1].shape[1]
                / int(parts_chol)
                * args[1].shape[2]
                + 8 * args[2].size / int(parts_dense)  # intermediate
                + 8
                * args[3].size  # result
                / int(parts_dense)
                / int(parts_chol)
                / int(parts_chol)
            )
            if memhave > memneed:
                break

        # get lengths of chunks
        chol_chunk_lengths_1 = []  # a
        for x in range(0, parts_chol):
            chol_chunk_lengths_1.append(
                np.array_split(args[0], parts_chol, axis=1)[x].shape[1]
            )
        chol_chunk_lengths_2 = []  # b
        for x in range(0, parts_chol):
            chol_chunk_lengths_2.append(
                np.array_split(args[1], parts_chol, axis=1)[x].shape[1]
            )
        dense_e_chunk_lengths = []
        for x in range(0, parts_dense):
            dense_e_chunk_lengths.append(
                np.array_split(args[2], parts_dense, axis=axis_e)[x].shape[
                    axis_e
                ]
            )

        if parts_chol == 1 and parts_dense == 1:
            # xac,abd - > acbd
            chol1 = cp.array(args[0])
            chol2 = cp.array(args[1])
            # x summation
            result_temp = cp.tensordot(chol1, chol2, axes=(0, 0))
            del chol1, chol2
            cp.get_default_memory_pool().free_all_blocks()
            operand = cp.array(args[2])
            # acbd,cde - > abe
            result_cp = cp.tensordot(
                result_temp, operand, axes=([1, 3], [axis_c, axis_d])
            )
            del result_temp, operand
            cp.get_default_memory_pool().free_all_blocks()
            result = result_cp.get()
        else:
            result = np.zeros(args[3].shape)
            if parts_dense > 1:
                start_e = 0
                end_e = 0
                for e in range(0, parts_dense):
                    end_e += dense_e_chunk_lengths[e]
                    start_a = 0
                    end_a = 0
                    for a in range(0, parts_chol):
                        end_a += chol_chunk_lengths_1[a]
                        start_b = 0
                        end_b = 0
                        for b in range(0, parts_chol):
                            end_b += chol_chunk_lengths_2[b]
                            chol_1 = cp.array(
                                np.array_split(args[0], parts_chol, axis=1)[a]
                            )
                            chol_2 = cp.array(
                                np.array_split(args[1], parts_chol, axis=1)[b]
                            )
                            # xac,xbd->acbd
                            result_temp = cp.tensordot(
                                chol_1, chol_2, axes=(0, 0)
                            )
                            del chol_1, chol_2
                            cp.get_default_memory_pool().free_all_blocks()
                            operand = cp.array(
                                np.array_split(
                                    args[2],
                                    parts_dense,
                                    axis=axis_e,
                                )[e]
                            )
                            result_temp_2 = cp.tensordot(
                                result_temp,
                                operand,
                                axes=([1, 3], [axis_c, axis_d]),
                            )
                            del operand, result_temp
                            cp.get_default_memory_pool().free_all_blocks()
                            result[
                                start_a:end_a, start_b:end_b, start_e:end_e
                            ] = result_temp_2.get()
                            del result_temp_2
                            cp.get_default_memory_pool().free_all_blocks()
                            start_b = end_b
                        start_a = end_a
                    start_e = end_e
            else:
                start_a = 0
                end_a = 0
                for a in range(0, parts_chol):
                    end_a += chol_chunk_lengths_1[a]
                    start_b = 0
                    end_b = 0
                    for b in range(0, parts_chol):
                        end_b += chol_chunk_lengths_2[b]
                        chol_1 = cp.array(
                            np.array_split(args[0], parts_chol, axis=1)[a]
                        )
                        chol_2 = cp.array(
                            np.array_split(args[1], parts_chol, axis=1)[b]
                        )
                        result_temp = cp.tensordot(chol_1, chol_2, axes=(0, 0))
                        del chol_1, chol_2
                        cp.get_default_memory_pool().free_all_blocks()
                        operand = cp.array(args[2])
                        result_temp_2 = cp.tensordot(
                            result_temp,
                            operand,
                            axes=([1, 3], [axis_c, axis_d]),
                        )
                        del operand, result_temp
                        cp.get_default_memory_pool().free_all_blocks()
                        result[
                            start_a:end_a, start_b:end_b, :
                        ] = result_temp_2.get()

                        del result_temp_2
                        cp.get_default_memory_pool().free_all_blocks()
                        start_b = end_b
                    start_a = end_a

    # generic
    else:
        # the index x is reserved for Cholesky vectors
        # if an x is contained in a contraction subscript, we assume Cholesky vectors
        operands_cp = []
        # first operand cholesky decomposed
        if "x" == subs[0]:
            chol1 = cp.array(args[0])
            chol2 = cp.array(args[1])
            # xac,xbd -> acbd
            result_temp_cp = cp.tensordot(chol1, chol2, axes=(0, 0))
            del chol1, chol2
            cp.get_default_memory_pool().free_all_blocks()
            # adds the other operands to operands_cp array
            # while leaving out the 2 cholesky arrays
            # Input operands are copied to GPU Memory (VRAM).
            for num in range(2, len(subs.split("->")[0].split(","))):
                operands_cp.append(cp.asarray(args[num]))
            # changes subscripts from e.g.: xac,xbd,...->... to: acbd,...->...
            subs = subs[1:3] + subs[5:]
            # acbd , ... -> ....
            # calculation on GPU
            result_cp = cp.einsum(subs, result_temp_cp, *operands_cp)
            del result_temp_cp
        # first operand dense representation
        else:
            for num in range(0, len(subs.split("->")[0].split(","))):
                # Input operands are copied to GPU Memory (VRAM).
                operands_cp.append(cp.asarray(args[num]))
            # calculation on GPU
            result_cp = cp.einsum(subs, *operands_cp)
        # Result is copied back to RAM
        result = result_cp.get()
        # VRAM deallocation
        del result_cp, operands_cp

    cp.get_default_memory_pool().free_all_blocks()
    # Result is returned
    return result
