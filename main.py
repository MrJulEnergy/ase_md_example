from zntrack import Node, zn
import ase
import ase_md.simulator as asemd
import typing

#TODO Mark Outputs

class GetAtoms(Node):
    """Generate Atoms for Simulation"""

    size: int = zn.params()

    def generate(self):
        self.atoms = asemd.generate_atoms(self.size)


class RunMD(Node):
    """Run Simulation"""

    atoms: ase.Atoms = zn.deps()
    temperature: float = zn.params()
    timestep: float = zn.params()
    dump_interval: int = zn.params()
    steps: int = zn.params()

    def run_md(self):
        atoms_list = asemd.run_simulation(
            atoms=self.atoms,
            temperature=self.temperature,
            timestep=self.timestep,
            dump_interval=self.dump_interval,
            steps=self.steps,
        )


class ComputeRDF(Node):
    """Calculate RDF whatever that means..."""

    atoms_list: typing.List[ase.Atoms] = zn.deps()
    rmax: float = zn.params()
    nbins: int = zn.params()

    def calc_rfd(self):
        rfd = asemd.compute_rdf(
            atoms_list=self.atoms_list, 
            rmax=self.rmas, 
            nbins=self.nbins, 
            elements="Cu"
        )
