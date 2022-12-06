import ase_md.simulator as ase


class GetAtoms(Node):
    """Generate Atoms for Simulation"""

    size: int = zn.params()

    def generate(self):
        self.atoms = ase.generate_atoms(self.size)


class RunMD(Node):
    """Run Simulation"""

    # atoms =
    temperature: float = zn.params()
    timestep: float = zn.params()
    dump_interval: int = zn.params()
    steps: int = zn.params()

    def run_md(self):
        atoms_list = ase.run_simulation(
            atoms=self.atoms,
            temperature=self.temperature,
            timestep=self.timestep,
            dump_interval=self.dump_interval,
            steps=self.steps,
        )


class ComputeRDF(Node):
    """Calculate RDF whatever that means..."""

    # atoms_list =
    rmax: float = zn.params()
    nbins: int = zn.params()

    def calc_rfd(self):
        rfd = ase.compute_rdf(
            atoms_list=self.atoms_list, 
            rmax=self.rmas, 
            nbins=self.nbins, 
            elements="Cu"
        )
