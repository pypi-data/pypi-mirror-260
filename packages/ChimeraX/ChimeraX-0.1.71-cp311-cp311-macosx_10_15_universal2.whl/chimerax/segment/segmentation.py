from chimerax.map.volume import Volume

class Segmentation(Volume):
    def __init__(self, session, grid_data, rendering_options = None):
        Volume.__init__(self, session, grid_data, rendering_options = rendering_options)
        self.active = False
        self.reference_data = None

    def set_2d_segment_data(self, axis: Axis, slice: int, positions, value: int, min_threshold: Optional[float] = None, max_threshold: Optional[float] = None) -> None:
        for position in positions:
            center_x, center_y, radius = position
            self.set_data_in_puck(axis, slice, round(center_x), round(center_y), radius, value, min_threshold, max_threshold)
        self.data.values_changed()

    def set_sphere_data(self, center: tuple, radius: int, value: int, min_threshold: Optional[float] = None, max_threshold: Optional[float] = None) -> None:
        # Optimization: Mask only subregion containing sphere.
        ijk_min, ijk_max = self._sphere_grid_bounds(center, radius)
        from chimerax.map_data import GridSubregion, zone_mask
        subgrid = GridSubregion(self.data, ijk_min, ijk_max)
        reference_subgrid = GridSubregion(self.data.reference_data, ijk_min, ijk_max)

        if min_threshold and max_threshold:
            mask = zone_mask_clamped_by_referenced_grid(subgrid, reference_subgrid, [center], radius, min_threshold, max_threshold)
        else:
            mask = zone_mask(subgrid, [center], radius)

        dmatrix = subgrid.full_matrix()

        from numpy import putmask
        putmask(dmatrix, mask, value)

        self.data.values_changed()

    def _sphere_grid_bounds(self, center, radius):
        ijk_center = self.data.xyz_to_ijk(center)
        spacings = self.data.plane_spacings()
        ijk_size = [radius/s for s in spacings]
        from math import floor, ceil
        ijk_min = [max(int(floor(c-s)), 0) for c,s in zip(ijk_center,ijk_size)]
        ijk_max = [min(int(ceil(c+s)), m-1) for c, s, m in zip(ijk_center, ijk_size, self.data.size)]
        return ijk_min, ijk_max


    def set_data_in_puck(self, axis: Axis, slice_number: int, left_offset: int, bottom_offset: int, radius: int, value: int, min_threshold: Optional[float] = None, max_threshold: Optional[float] = None) -> None:
        # TODO: if not segmentation, refuse
        # TODO: Preserve the happiest path. If the radius of the segmentation overlay is
        #  less than the radius of one voxel, there's no need to go through all the rigamarole.
        #  grid.data.segment_array[slice][left_offset][bottom_offset] = 1
        x_max, y_max, z_max = self.data.size
        x_step, y_step, z_step = self.data.step
        if not min_threshold:
            min_threshold = float('-inf')
        if not max_threshold:
            max_threshold = float('inf')
        if axis == Axis.AXIAL:
            slice = self.data.pixel_array[slice_number]
            reference_slice = self.data.reference_data.pixel_array[slice_number]
            vertical_max = y_max - 1
            vertical_step = y_step
            horizontal_max = x_max - 1
            horizontal_step = x_step
        elif axis == Axis.CORONAL:
            slice = self.data.pixel_array[:, slice_number, :]
            reference_slice = self.data.reference_data.pixel_array[:, slice_number, :]
            vertical_max = z_max - 1
            vertical_step = z_step
            horizontal_max = x_max - 1
            horizontal_step = x_step
        else:
            slice = self.data.pixel_array[:, :, slice_number]
            reference_slice = self.data.reference_data.pixel_array[:, :, slice_number]
            vertical_max = z_max - 1
            vertical_step = z_step
            horizontal_max = y_max - 1
            horizontal_step = y_step
        scaled_radius = round(radius / horizontal_step)
        x = 0
        y = round(radius)
        d = 1 - y
        while y > x:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            scaled_horiz_x = round(x / horizontal_step)
            scaled_vert_x = round(x / vertical_step)
            scaled_horiz_y = round(y / horizontal_step)
            scaled_vert_y = round(y / vertical_step)
            x_start = round(max(left_offset - scaled_horiz_x, 0))
            x_end = round(min(left_offset + scaled_horiz_x, horizontal_max - 1))
            y_start = round(max(bottom_offset - scaled_vert_y, 0))
            y_end = round(min(bottom_offset + scaled_vert_y, vertical_max))
            mask = np.where(reference_slice[y_start, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_start, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_start][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_start+1, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_start+1, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_start+1][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_end, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_end, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_end][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_end-1, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_end-1, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_end-1][x_start:x_end][np.where(mask == 1)] = value
               #slice[y_end][x_start:x_end][np.where(min_threshold <= reference_slice <= max_threshold)] = value
            #for i in range(x_start, x_end):
            ##    if min_threshold <= reference_slice[y_start][i] <= max_threshold:
            ##        slice[y_start][i] = value
            #    if min_threshold <= reference_slice[y_end][i] <= max_threshold:
            #        slice[y_end][i] = value
            #    # Try to account for the fact that with spacings < 1 some lines get skipped, even if it
            #    # causes redundant writes
            #    if min_threshold <= reference_slice[y_start+1][i] <= max_threshold:
            #        slice[y_start+1][i] = value
            #    if min_threshold <= reference_slice[y_end-1][i] <= max_threshold:
            #        slice[y_end-1][i] = value
            x_start = round(max(left_offset - scaled_horiz_y, 0))
            x_end = round(min(left_offset + scaled_horiz_y, horizontal_max))
            y_start = round(max(bottom_offset - scaled_vert_x, 0))
            y_end = round(min(bottom_offset + scaled_vert_x, vertical_max))
            mask = np.where(reference_slice[y_start, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_start, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_start][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_start+1, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_start+1, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_start+1][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_end, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_end, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_end][x_start:x_end][np.where(mask == 1)] = value
            mask = np.where(reference_slice[y_end-1, x_start:x_end] <= max_threshold, 1, 0)
            mask &= np.where(reference_slice[y_end-1, x_start:x_end] >= min_threshold, 1, 0)
            slice[y_end-1][x_start:x_end][np.where(mask == 1)] = value

            #for i in range(x_start, x_end):
            #    if min_threshold <= reference_slice[y_start][i] <= max_threshold:
            #        slice[y_start][i] = value
            #    if min_threshold <= reference_slice[y_end][i] <= max_threshold:
            #        slice[y_end][i] = value
            #    # Try to account for the fact that with spacings < 1 some lines get skipped, even if it
            #    # causes redundant writes
            #    if min_threshold <= reference_slice[y_start+1][i] <= max_threshold:
            #        slice[y_start+1][i] = value
            #    if min_threshold <= reference_slice[y_end-1][i] <= max_threshold:
            #        slice[y_end-1][i] = value
            #slice[y_start + 1][x_start:x_end] = value
            #slice[y_end - 1][x_start:x_end] = value
        mask = np.where(reference_slice[bottom_offset, left_offset - scaled_radius:left_offset + scaled_radius] <= max_threshold, 1, 0)
        mask &= np.where(reference_slice[bottom_offset, left_offset - scaled_radius:left_offset + scaled_radius] >= min_threshold, 1, 0)
        #for i in range(left_offset - scaled_radius, left_offset + scaled_radius):
        #    if min_threshold <= reference_slice[bottom_offset][i] <= max_threshold:
        #        slice[bottom_offset][i] = value
        slice[bottom_offset][left_offset - scaled_radius:left_offset + scaled_radius][np.where(mask == 1)] = value

    def take_snapshot(self, session, flags):
        return super().take_snapshot(session, flags)

    @staticmethod
    def restore_snapshot(session, data):
        grid_data = data['grid data state'].grid_data
        if grid_data is None:
            return
        dv = Volume(session, grid_data)
        Model.set_state_from_snapshot(dv, session, data['model state'])
        dv._style_when_shown = None
        from chimerax.map.session import set_map_state
        from chimerax.map.volume import show_volume_dialog
        set_map_state(data['volume state'], dv)
        dv._drawings_need_update()
        show_volume_dialog(session)
        return dv
