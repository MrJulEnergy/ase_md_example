from zntrack import Node, zn
import ase
import ase_md.simulator as asemd
import typing
import matplotlib.pyplot as plt
import pandas as pd

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
    """runs MD (time expensive)"""

    # Inputs:
    atoms: GetAtoms = zn.deps()
    temperature = zn.params()
    timestep = zn.params()
    steps = zn.params()
    dump_interval = zn.params()
    # Outputs:
    atoms_list = zn.outs()
    # Function
    def run(self):
        self.atoms_list = asemd.run_simulation(
            atoms=self.atoms.atoms,
            temperature=self.temperature,
            timestep=self.timestep,
            steps=self.steps,
            dump_interval=self.dump_interval,
        )


class ComputeRDF(Node):
    """Calculate RDF whatever that means..."""

    # Inputs:
    atoms_list: RunMD = zn.deps()
    rmax: float = zn.params()
    nbins: int = zn.params()
    # Outputs:
    rdf: dict = zn.outs()
    nice_plot = zn.plots(x_label="r", y_label="amp")
    # Function:
    def run(self):
        self.rdf = asemd.compute_rdf(
            atoms_list=self.atoms_list.atoms_list,
            rmax=self.rmax,
            nbins=self.nbins,
            elements="Cu",
        )
        x_data = self.rdf["x"]
        y_data = self.rdf["y"]
        df = pd.DataFrame({"y": y_data, "x": x_data})
        self.nice_plot = df
        self.nice_plot.index.name=("x")


if __name__ == "__main__":
    atoms = GetAtoms(size=3)
    atoms.write_graph()
    atoms_list = RunMD(
        atoms=atoms, temperature=300, timestep=1.0, steps=20, dump_interval=5
    )
    atoms_list.write_graph()
    rdf = ComputeRDF(atoms_list=atoms_list, rmax=3.6, nbins=50)
    rdf.write_graph()

