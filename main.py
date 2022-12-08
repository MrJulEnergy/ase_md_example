from zntrack import Node, zn
import ase
import ase_md.simulator as asemd
import typing


#TODO Add default parameter
#TODO look up zn.deps()


class GetAtoms(Node):
    """Generate Atoms for Simulation"""
    #Inputs:
    size: int = zn.params()
    #Outputs:
    atoms: ase.Atoms = zn.metrics()
    #Default Values:
    def __post_init__(self):
        """ default arguments for attributes """
        pass
    #Function:
    def generate(self):
        self.atoms = asemd.generate_atoms(self.size)


class RunMD(Node):
    """Run Simulation"""
    #Inputs:
    atoms: ase.Atoms = zn.deps()
    temperature: float = zn.params()
    timestep: float = zn.params()
    dump_interval: int = zn.params()
    steps: int = zn.params()
    #Outputs:
    atoms_list: typing.List[ase.Atoms] = zn.metrics()
    #Functions:
    def run_md(self):
        self.atoms_list = asemd.run_simulation(
            atoms=self.atoms,
            temperature=self.temperature,
            timestep=self.timestep,
            dump_interval=self.dump_interval,
            steps=self.steps,
        )


class ComputeRDF(Node):
    """Calculate RDF whatever that means..."""
    #Inputs:
    atoms_list: typing.List[ase.Atoms] = zn.deps()
    rmax: float = zn.params()
    nbins: int = zn.params()
    #Outputs:
    rfd: dict = zn.metrics()
    #Function:
    def calc_rfd(self):
        self.rfd = asemd.compute_rdf(
            atoms_list=self.atoms_list, 
            rmax=self.rmas, 
            nbins=self.nbins, 
            elements="Cu"
        )
