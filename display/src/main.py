
from numbers import Number
from typing import List
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def read_deltas(path: str, converter = lambda line: int(line)) -> List[Number]:
    """ Read the deltas for a given path """

    with open(path, "r") as file:
        deltas = [converter(line.strip()) for line in file.readlines()]
        return deltas
    
    return []


def build_plot(
    plot: Axes,
    deltas: List[Number],
    title: str,
    y_label: str = "Nano Second Deltas",
    y_max: Number = None,
    color: str = "blue",
) -> None:

    plot.scatter(x=range(len(deltas)), y=deltas, c=color)
    plot.set_title(title)
    plot.set_ylabel(y_label)
    if y_max:
        plot.set_ylim((0, y_max))
    plot.legend()
    

PATH_TO_DELTAS: str = "../../delta_outs/"
    
c_deltas: List[int] = read_deltas(PATH_TO_DELTAS + "c_out.txt")
c_sys_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "c_out_sys.txt", lambda line: float(line))
c_ar_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "c_out_arithmetic.txt", lambda line: float(line))

rust_deltas: List[int] = read_deltas(PATH_TO_DELTAS + "rust_out.txt")
rust_sys_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "rust_out_sys.txt", lambda line: float(line))
rust_ar_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "rust_out_arithmetic.txt", lambda line: float(line))

java_deltas: List[int] = read_deltas(PATH_TO_DELTAS + "java_out.txt")
java_sys_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "java_out_sys.txt", lambda line: float(line))
java_ar_deltas: List[float] = read_deltas(PATH_TO_DELTAS + "java_out_arithmetic.txt", lambda line: float(line))
    
fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(25,20))

build_plot(
    axes[0, 0],
    c_deltas,
    "C Nano Deltas",
)
build_plot(
    axes[1, 0],
    c_sys_deltas,
    "C System Time Deltas",
    "Microsecond Delta",
)

build_plot(
    axes[0, 1],
    rust_deltas,
    "Rust Nano Deltas",
    color="red",
)
build_plot(
    axes[1, 1],
    rust_sys_deltas,
    "Rust System Time Deltas",
    "Microsecond Delta",
    color="red",
)

build_plot(
    axes[0, 2],
    java_deltas,
    "Java Nano Deltas",
    color="green",
)
build_plot(
    axes[1, 2],
    java_sys_deltas,
    "Java System Time Deltas",
    "Microsecond Delta",
    color="green",
    
)
fig.canvas.manager.set_window_title("Sleep Delta Graphs")
fig.suptitle("Sleep Time Delta From Expected")

ar_fig, ar_axes = plt.subplots(ncols=3, nrows=1, figsize=(25,20))

ar_fig.canvas.manager.set_window_title("Arithmetic Delta Graphs")

def get_avg(arr):
    
    return sum(arr) / len(arr)

print("C Avg = ", get_avg(c_ar_deltas))
print("Rust Avg = ", get_avg(rust_ar_deltas))
print("Java Avg = ", get_avg(java_ar_deltas))

ar_fig.suptitle("Arithmetic Time Deltas")
build_plot(
    ar_axes[0],
    c_ar_deltas,
    "C Arithmetic Time Deltas",
    "Nanosecond Delta",
    150,
)
build_plot(
    ar_axes[1],
    rust_ar_deltas,
    "Rust Arithmetic Time Deltas",
    "Nanosecond Delta",
    150,
    "red",
)
build_plot(
    ar_axes[2],
    java_ar_deltas,
    "Java Arithmetic Time Deltas",
    "Nanosecond Delta",
    150,
    "green",
)

# fig.show()
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)  # Decrease margins

fig.savefig(PATH_TO_DELTAS + "sleep_fig.png")
ar_fig.savefig(PATH_TO_DELTAS + "arithmetic_fig.png")

plt.show()