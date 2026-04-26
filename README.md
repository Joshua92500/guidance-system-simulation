Guidance System Simulation
==========================

A compact Python simulation demonstrating guided-interceptor scenarios with 3D visualization.

Summary
-------

This repository contains a simulation of interceptors and targets, including
radar detection and a simple predictive guidance module. It is intended for education,
experimentation, and prototyping of guidance concepts.

<img width="1920" height="1080" alt="guidance_system_thumbnail" src="https://github.com/user-attachments/assets/6e5e9b98-2779-499a-8b9a-1f1ff958ff6b" />

Key components
--------------

- `main.py`: Runner that configures targets, interceptors, and runs a 3D animation.
- `models/`: Core simulation modules:
	- `dot.py` — base drawable object used by targets and interceptors
	- `target.py` — target behavior and state
	- `interceptor.py` — interceptor logic, fuse handling, and guidance integration
	- `radar.py` — simple detection sensor
	- `physics.py` — helper physics (e.g., turn limiting)
	- `plot3d.py` — plotting utilities and animation harness
	- `guidance/predictive.py` — predictive guidance module

Prerequisites
-------------

- Python 3.10+ (or recent 3.x)
- Install dependencies from `requirements.txt` (recommended inside a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Running
-------

Run the simulation with:

```bash
python main.py
```

This opens a Matplotlib 3D animation showing targets and interceptors. The example in `main.py`
configures two targets and one interceptor using the predictive guidance module.
