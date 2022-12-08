from zntrack import Node, zn
import ase
import ase_md.simulator as asemd
import typing


class GetAtoms(Node):
    """Generate Atoms for Simulation"""

    # Inputs:
    size: int = zn.params()
    # Outputs:
    atoms: ase.Atoms = zn.outs()
    # Function:
    def run(self):
        self.atoms = asemd.generate_atoms(self.size)


class RunMD(Node):
    """Run Simulation"""

    # Inputs:
    atoms: ase.Atoms = zn.deps()
    temperature: float = zn.params()
    timestep: float = zn.params()
    dump_interval: int = zn.params()
    steps: int = zn.params()
    # Outputs:
    atom_list: typing.List[ase.Atoms] = zn.outs()
    # Functions:
    def run(self):
        self.atom_list = asemd.run_simulation(
            atoms=self.atoms,
            temperature=self.temperature,
            timestep=self.timestep,
            steps=self.steps,
            dump_interval=self.dump_interval,
        )


class ComputeRDF(Node):
    """Calculate RDF whatever that means..."""
    # Inputs:
    atoms_list: typing.List[ase.Atoms] = zn.deps()
    rmax: float = zn.params()
    nbins: int = zn.params()
    # Outputs:
    rfd: dict = zn.outs()
    # Function:
    def run(self):
        self.rfd = asemd.compute_rdf(
            atoms_list=self.atoms_list, rmax=self.rmas, nbins=self.nbins, elements="Cu"
        )

if __name__ == "__main__":
    cool_atoms = GetAtoms(size=3)
    cool_atoms.write_graph()
    cool_atoms_list = RunMD(
        atoms=cool_atoms, temperature=300, timestep=5.0, steps=20, dump_interval=10
    )
    cool_atoms_list.write_graph()
    res_rdf = ComputeRDF(atoms_list=cool_atoms_list, rmax=1.0, nbins=50)
    res_rdf.write_graph()

