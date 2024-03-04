import os
from pwdata.calculators.const import elements

def save_to_extxyz(image_data_all: list, output_path: str, output_file: str, write_patthen='w'):
    output_file = open(os.path.join(output_path, output_file), write_patthen)
    for i in range(len(image_data_all)):
        image_data = image_data_all[i]
        if not image_data.cartesian:
            image_data._set_cartesian()
        output_file.write("%d\n" % image_data.atom_nums)
        # output_file.write("Iteration: %s\n" % image_data.iteration)
        output_head = 'Lattice="%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f" Properties=species:S:1:pos:R:3:force:R:3:local_energy:R:1 pbc="T T T" energy={}\n'.format(image_data.Ep)
        output_extended = (image_data.lattice[0][0], image_data.lattice[0][1], image_data.lattice[0][2], 
                                image_data.lattice[1][0], image_data.lattice[1][1], image_data.lattice[1][2], 
                                image_data.lattice[2][0], image_data.lattice[2][1], image_data.lattice[2][2])
        output_file.write(output_head % output_extended)
        for j in range(image_data.atom_nums):
            properties_format = "%s %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f\n"
            properties = (elements[image_data.atom_types_image[j]], image_data.position[j][0], image_data.position[j][1], image_data.position[j][2], 
                            image_data.force[j][0], image_data.force[j][1], image_data.force[j][2], 
                            image_data.atomic_energy[j])
            output_file.write(properties_format % properties)
    output_file.close()
    print("Convert to %s successfully!" % output_file)
