import ase_md.simulator as ase

atoms = ase.generate_atoms(size=2)

atoms_list = ase.run_simulation(
    atoms=atoms, temperature=300, timestep=1.0, dump_interval=5, steps=20)

rfd = ase.compute_rdf(atoms_list=atoms_list, rmax=1.0, nbins=50, elements="Cu")
