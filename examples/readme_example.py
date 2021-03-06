import sys

import ctl
import numpy as np
from matplotlib import pyplot as plt

def main():
    # create a volume of size 128x128x128px with a voxel size of 1x1x1mm
    volume = ctl.VoxelVolumeF((128, 128, 128), (1.0, 1.0, 1.0))
    volume.fill(1.0)

    # alternatively:
    # volume = ctl.VoxelVolumeF.from_numpy(np.ones((128, 128, 128)))
    # volume.set_voxel_size((1.0, 1.0, 1.0))

    # use of a predefined system from ctl.blueprints
    system = ctl.CTSystemBuilder.create_from_blueprint(ctl.blueprints.GenericCarmCT())

    # create an acquisition setup
    nb_views = 100
    my_carm_setup = ctl.AcquisitionSetup(system, nb_views)

    # add a predefined trajectory to the setup from ctl.protocols
    angle_span = np.deg2rad(200.0) # rad is the standard unit for angles
    source_to_isocenter = 750.0 # mm is the standard unit for length dimensions
    my_carm_setup.apply_preparation_protocol(ctl.protocols.WobbleTrajectory(angle_span,
                                                                            source_to_isocenter))

    if not my_carm_setup.is_valid():
        sys.exit(-1)

    # configure a projector and project volume
    my_projector = ctl.ocl.RayCasterProjector()      # the projector (uses its default settings)
    my_projector.configure(my_carm_setup)            # configure the projector
    projections = my_projector.project(volume)       # project

    # show the 20th projection of detector module 0
    proj20 = projections.to_numpy()[20, 0]
    # alternatively: proj20 = projections.view(20).module(0).to_numpy()
    _ = plt.imshow(proj20, cmap='gray'), plt.show()

if __name__ == '__main__':
    main()
